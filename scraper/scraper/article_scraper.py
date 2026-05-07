import time
import unicodedata
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import HEADERS, KEYWORDS_POPULATION, KEYWORDS_TOPIC, KEYWORDS_STANDALONE, REQUEST_DELAY, MAX_WORKERS
from storage.file_manager import save_checkpoint

_JUNK_PDF_PATTERNS = ["Diretrizes", "editorial", "guidelines", "static_files"]


def _get_soup(url: str) -> BeautifulSoup | None:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        print(f"[ERRO] {url}: {e}")
        return None


def _normalize(text: str) -> str:
    return unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode().lower()


# Usa o regex para filtrar artigos relevantes após a busca pelas keywords
def _is_relevant(text: str) -> bool:
    t = _normalize(text)

    if any(p.search(t) for p in PATTERNS_STANDALONE):
        return True

    has_population = any(p.search(t) for p in PATTERNS_POPULATION)
    has_topic = any(p.search(t) for p in PATTERNS_TOPIC)
    return has_population and has_topic


SEARCH_URL = "https://theconversation.com/br/search"


def _search_keyword(query: str, max_pages: int | None, seen_urls: set) -> list[dict]:
    articles = []
    page = 1
    while True:
        if max_pages and page > max_pages:
            break
        soup = _get_soup(f"{SEARCH_URL}?q={requests.utils.quote(query)}&page={page}")
        if not soup:
            break
        art_tags = soup.select("article")
        if not art_tags:
            break
        found_new = False
        for art in art_tags:
            link_tag = art.select_one("h1 a, h2 a, h3 a")
            if not link_tag:
                continue
            href = link_tag["href"]
            url = href if href.startswith("http") else f"https://theconversation.com{href}"
            title = link_tag.get_text(strip=True)
            if url in seen_urls:
                continue
            if not _is_relevant(title):
                continue
            seen_urls.add(url)
            articles.append({"title": title, "url": url})
            print(f"  [+] {title}")
            found_new = True
        if not found_new:
            break
        save_checkpoint(page, seen_urls, [])
        time.sleep(REQUEST_DELAY)
        page += 1
    return articles


def get_article_links(max_pages: int | None = None, start_page: int = 1, seen_urls: set = None) -> list[dict]:
    seen_urls = seen_urls or set()
    articles = []
    queries = list(KEYWORDS_STANDALONE) + [f"{p} {t}" for p in KEYWORDS_POPULATION[:5] for t in KEYWORDS_TOPIC[:5]]
    for query in queries:
        print(f"[BUSCANDO] '{query}'...")
        found = _search_keyword(query, max_pages, seen_urls)
        articles.extend(found)
    return articles


def get_article_content(meta: dict) -> dict:
    url = meta["url"]
    soup = _get_soup(url)
    if not soup:
        return {}

    title = soup.select_one("h1")
    title = title.get_text(strip=True) if title else meta.get("title", "sem_titulo")

    author_tag = soup.select_one("a[rel=author]")
    author = author_tag.get_text(strip=True) if author_tag else ""

    date_tag = soup.select_one("time[datetime]")
    date = date_tag["datetime"][:10] if date_tag else ""

    doi_link = None
    pdf_link = None
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "doi.org" in href and not doi_link:
            doi_link = href
        if href.endswith(".pdf") and not pdf_link:
            if not any(p.lower() in href.lower() for p in _JUNK_PDF_PATTERNS):
                pdf_link = href if href.startswith("http") else f"https://theconversation.com{href}"

    body = soup.select_one("div.content-body, article, div[itemprop='articleBody']")
    text = ""
    if body:
        text = "\n".join(p.get_text(strip=True) for p in body.find_all("p"))

    return {"title": title, "author": author, "date": date, "url": url, "doi": doi_link, "pdf_link": pdf_link, "text": text}


def fetch_all_articles(articles_meta: list[dict]) -> list[dict]:
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(get_article_content, meta): meta for meta in articles_meta}
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    return results
