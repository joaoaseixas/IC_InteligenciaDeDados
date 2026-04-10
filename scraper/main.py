import re
import sys
import time
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, ".")

from scraper.article_scraper import get_article_links, fetch_all_articles
from scraper.pdf_downloader import download_pdf
from storage.file_manager import save_article, save_index, load_checkpoint, save_checkpoint, clear_checkpoint
from config import REQUEST_DELAY


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_-]+", "_", text)[:80]


def ask_pages() -> int | None:
    """Pergunta o modo de busca. Retorna max_pages ou None (site todo)."""
    print("\n=== Web Scraper - The Conversation BR ===")
    print("\nComo deseja executar a busca?")
    print("  [1] Escanear o site todo")
    print("  [2] Definir número de páginas")

    while True:
        escolha = input("\nEscolha (1 ou 2): ").strip()
        if escolha == "1":
            print("\n[INFO] Modo: site completo\n")
            return None
        elif escolha == "2":
            while True:
                valor = input("Quantas páginas deseja buscar? ").strip()
                if valor.isdigit() and int(valor) > 0:
                    print(f"\n[INFO] Modo: {valor} página(s)\n")
                    return int(valor)
                print("[ERRO] Digite um número válido maior que zero.")
        else:
            print("[ERRO] Digite 1 ou 2.")


def run():
    checkpoint = load_checkpoint()
    start_page = 1
    seen_urls = set()
    collected = []
    max_pages = None

    if checkpoint:
        last_page = checkpoint["last_page"]
        print(f"\n[CHECKPOINT] Última busca parou na página {last_page}.")
        resp = input("Deseja continuar de onde parou? (s/n): ").strip().lower()
        if resp == "s":
            start_page = last_page + 1
            seen_urls = set(checkpoint["seen_urls"])
            collected = checkpoint["collected"]
            max_pages = ask_pages()
            print(f"\n[INFO] Retomando da página {start_page} com {len(collected)} artigos já coletados.\n")
        else:
            clear_checkpoint()
            print("[INFO] Checkpoint descartado.\n")
            max_pages = ask_pages()
    else:
        max_pages = ask_pages()

    # 1. Coleta links por página (com checkpoint automático)
    articles_meta = get_article_links(max_pages=max_pages, start_page=start_page, seen_urls=seen_urls)
    print(f"\n[INFO] {len(articles_meta)} novos artigos relevantes encontrados.\n")

    if not articles_meta:
        print("Nenhum artigo novo para processar.")
        clear_checkpoint()
        return

    # 2. Busca conteúdo em paralelo
    print("[INFO] Buscando conteúdo em paralelo...\n")
    articles = fetch_all_articles(articles_meta)

    # 3. Salva cada artigo
    saved_files = []
    for article in articles:
        print(f"[PROCESSANDO] {article['title']}")

        if article.get("doi"):
            print(f"  [DOI] {article['doi']}")

        if article.get("pdf_link"):
            article["pdf_path"] = download_pdf(article["pdf_link"], slugify(article["title"]))
        else:
            article["pdf_path"] = None

        filepath = save_article(article)
        saved_files.append(filepath)
        collected.append({
            "title": article["title"],
            "url": article["url"],
            "doi": article.get("doi"),
            "pdf_path": article["pdf_path"]
        })

        save_checkpoint(start_page, seen_urls, collected)
        time.sleep(REQUEST_DELAY)

    save_index(collected)
    clear_checkpoint()
    print(f"\n=== Concluído — {len(collected)} artigos salvos ===")
    print(f"\nArquivo gerado: {saved_files[0] if saved_files else ''}")


if __name__ == "__main__":
    run()
