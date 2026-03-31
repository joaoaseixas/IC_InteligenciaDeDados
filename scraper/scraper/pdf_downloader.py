import requests
from pathlib import Path
from config import HEADERS, PDF_DIR


def download_pdf(url: str, filename: str) -> str | None:
    """Baixa um PDF e salva em PDF_DIR. Retorna o caminho salvo ou None."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15, stream=True)
        response.raise_for_status()

        if "application/pdf" not in response.headers.get("Content-Type", ""):
            print(f"[AVISO] URL não retornou PDF: {url}")
            return None

        Path(PDF_DIR).mkdir(parents=True, exist_ok=True)
        filepath = Path(PDF_DIR) / f"{filename}.pdf"

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[PDF] Salvo: {filepath}")
        return str(filepath)

    except requests.RequestException as e:
        print(f"[ERRO PDF] {url}: {e}")
        return None
