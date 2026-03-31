import re
import time
import unicodedata
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import BASE_URL, HEADERS, KEYWORDS_POPULATION, KEYWORDS_TOPIC, KEYWORDS_STANDALONE, REQUEST_DELAY, MAX_WORKERS
from storage.file_manager import save_checkpoint

API_URL = "https://theconversation.com/br/articles.json"
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


def _is_relevant(text: str) -> bool:
    t = _normalize(text)
    if any(_normalize(kw) in t for kw in KEYWORDS_STANDALONE):
        return True
    has_population = any(_normalize(kw) in t for kw in KEYWORDS_POPULATION)
    has_topic = any(_normalize(kw) in t for kw in KEYWORDS_TOPIC)
    return has_population and has_topic


def get_article_links(max_pages: int | None = None, start_page: int = 1, seen_urls: set = None) -> list[dict]:
    articles = []
    seen_urls = seen_urls or set()
    page = start_page

    while True:
        if max_pages and page > (start_page - 1 + max_pages):
            print(f"[FIM] Limite de {max_pages} página(s) atingido.")
            break

        print(f"[SCRAPING] Página {page}...")
        try:
            r = requests.get(API_URL, params={"page": page}, headers=HEADERS, timeout=10)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"[ERRO] Página {page}: {e}")
            break

        if not data:
            print(f"[FIM] Sem mais artigos na página {page}. Encerrando.")
            break

        for item in data:
            url = item.get("url", "")
            title = item.get("title", "")
            summary = BeautifulSoup(item.get("summary_html", ""), "lxml").get_text()

            if url in seen_urls:
                continue

            # verifica titulo + resumo + slug da url
            if _is_relevant(title) or _is_relevant(summary) or _is_relevant(url):
                articles.append({"title": title, "url": url})
                seen_urls.add(url)
                print(f"  [+] {title}")

        save_checkpoint(page, seen_urls, [])
        time.sleep(REQUEST_DELAY)
        page += 1

    return articles


def get_article_content(meta: dict) -> dict:
    url = meta["url"]
    soup = _get_soup(url)
    if not soup:
        return {}

    title = soup.select_one("h1")
    title = title.get_text(strip=True) if title else meta.get("title", "sem_titulo")

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

    return {"title": title, "url": url, "doi": doi_link, "pdf_link": pdf_link, "text": text}


def fetch_all_articles(articles_meta: list[dict]) -> list[dict]:
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(get_article_content, meta): meta for meta in articles_meta}
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    return results
