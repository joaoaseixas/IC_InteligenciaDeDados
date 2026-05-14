import time
import unicodedata
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from config import REQUEST_DELAY
from storage.file_manager import save_checkpoint


def _normalize(text: str) -> str:
    return unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode().lower()


def _make_driver() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)


def _is_relevant(text: str, patterns_standalone, patterns_population, patterns_topic) -> bool:
    t = _normalize(text)
    if any(p.search(t) for p in patterns_standalone):
        return True
    return any(p.search(t) for p in patterns_population) and any(p.search(t) for p in patterns_topic)


# ── ResearchGate ──────────────────────────────────────────────────────────────

def search_researchgate(queries: list[str], max_pages: int | None, seen_urls: set,
                        patterns_standalone, patterns_population, patterns_topic) -> list[dict]:
    articles = []
    driver = _make_driver()
    try:
        for query in queries:
            print(f"[BUSCANDO RG] '{query}'...")
            page = 1
            while True:
                if max_pages and page > max_pages:
                    break
                url = f"https://www.researchgate.net/search/publication?q={query}&page={page}"
                driver.get(url)
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.nova-legacy-o-stack__item, li.search-box__result-item"))
                    )
                except Exception:
                    break

                items = driver.find_elements(By.CSS_SELECTOR,
                    "a.nova-legacy-e-link--theme-bare[href*='/publication/']")
                if not items:
                    break

                found_new = False
                for el in items:
                    href = el.get_attribute("href") or ""
                    title = el.text.strip()
                    if not title or not href or href in seen_urls:
                        continue
                    if not _is_relevant(title, patterns_standalone, patterns_population, patterns_topic):
                        continue
                    seen_urls.add(href)
                    articles.append({"title": title, "url": href})
                    print(f"  [+] {title}")
                    found_new = True

                if not found_new:
                    break
                save_checkpoint(page, seen_urls, [])
                time.sleep(REQUEST_DELAY)
                page += 1
    finally:
        driver.quit()
    return articles


# ── IEEE Xplore ───────────────────────────────────────────────────────────────

def search_ieee(queries: list[str], max_pages: int | None, seen_urls: set,
                patterns_standalone, patterns_population, patterns_topic) -> list[dict]:
    articles = []
    driver = _make_driver()
    try:
        for query in queries:
            print(f"[BUSCANDO IEEE] '{query}'...")
            page = 1
            while True:
                if max_pages and page > max_pages:
                    break
                url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={query}&pageNumber={page}"
                driver.get(url)
                try:
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "xpl-results-item, .List-results-items"))
                    )
                except Exception:
                    break

                items = driver.find_elements(By.CSS_SELECTOR,
                    "xpl-results-item h2 a, .result-item-title a")
                if not items:
                    break

                found_new = False
                for el in items:
                    href = el.get_attribute("href") or ""
                    title = el.text.strip()
                    if not title or not href or href in seen_urls:
                        continue
                    if not _is_relevant(title, patterns_standalone, patterns_population, patterns_topic):
                        continue
                    seen_urls.add(href)
                    articles.append({"title": title, "url": href})
                    print(f"  [+] {title}")
                    found_new = True

                if not found_new:
                    break
                save_checkpoint(page, seen_urls, [])
                time.sleep(REQUEST_DELAY)
                page += 1
    finally:
        driver.quit()
    return articles
