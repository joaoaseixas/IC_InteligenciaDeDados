# IC — Inteligência de Dados

Sistema de web-scraping para busca e extração de artigos científicos e jornalísticos, com suporte a download de PDFs. Desenvolvido como parte de uma Iniciação Científica, tendo o portal [The Conversation BR](https://theconversation.com/br) como fonte de validação.

---

## Como funciona

O sistema percorre as páginas de listagem do The Conversation BR, filtra artigos cujos títulos contenham palavras-chave relacionadas ao tema da pesquisa e, para cada artigo relevante encontrado:

1. Acessa a página do artigo
2. Tenta localizar e baixar um PDF diretamente vinculado
3. Extrai o texto do corpo do artigo como fallback caso não haja PDF
4. Persiste os dados em arquivos JSON individuais e em um índice geral

---

## Estrutura de pastas

```
scraper/
├── main.py                  # Ponto de entrada da aplicação
├── config.py                # Configurações globais (URLs, keywords, delays)
├── requirements.txt         # Dependências Python
│
├── scraper/
│   ├── article_scraper.py   # Coleta de links e extração de conteúdo
│   └── pdf_downloader.py    # Download e validação de PDFs
│
├── storage/
│   └── file_manager.py      # Persistência em JSON
│
└── data/
    ├── pdfs/                # PDFs baixados
    └── articles/            # JSONs com metadados e texto de cada artigo
```

---

## Papel de cada arquivo

### `main.py`
Orquestra todo o fluxo: coleta os links, processa cada artigo, aciona o download de PDF quando disponível e salva os resultados. É o único arquivo que deve ser executado diretamente.

### `config.py`
Centraliza todas as configurações do sistema:
- `BASE_URL` — URL base do portal alvo
- `KEYWORDS` — lista de termos usados para filtrar artigos relevantes
- `REQUEST_DELAY` — intervalo em segundos entre requisições (evita bloqueio)
- Caminhos dos diretórios de saída (`PDF_DIR`, `ARTICLES_DIR`)

### `scraper/article_scraper.py`
Contém duas funções principais:
- `get_article_links(max_pages)` — varre as páginas de listagem e retorna título e URL dos artigos cujo título bate com alguma keyword
- `get_article_content(url)` — acessa a página de um artigo e extrai título, texto do corpo e link de PDF (se houver)

### `scraper/pdf_downloader.py`
Responsável por baixar PDFs. Valida o `Content-Type` da resposta antes de salvar para garantir que o arquivo recebido é de fato um PDF. Salva os arquivos em `data/pdfs/`.

### `storage/file_manager.py`
Gerencia a persistência dos dados:
- `save_article(article)` — salva os dados de um artigo (título, URL, texto, caminho do PDF) em um arquivo `.json` nomeado pelo slug do título
- `save_index(articles)` — salva um arquivo `_index.json` com o resumo de todos os artigos coletados na execução

---

## Instalação e execução

**Pré-requisito:** Python 3.10+

```bash
# 1. Entrar na pasta do scraper
cd scraper

# 2. (Recomendado) Criar e ativar um ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar
python main.py          # scrapa 3 páginas (padrão)
python main.py 10       # scrapa 10 páginas
```

Os resultados ficam em:
- `data/articles/` — um `.json` por artigo + `_index.json` com o índice geral
- `data/pdfs/` — PDFs baixados (quando disponíveis na página do artigo)

---

## Ajustando para outro tema

Edite a lista `KEYWORDS` em `config.py` para refletir os termos do seu tema de pesquisa:

```python
KEYWORDS = [
    "saúde mental", "ansiedade", "depressão", "bem-estar"
]
```

Para usar outra fonte, altere `BASE_URL` e, se necessário, os seletores CSS em `article_scraper.py` para corresponder à estrutura HTML do novo portal.
