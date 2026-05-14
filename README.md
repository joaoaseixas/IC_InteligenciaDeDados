# IC — Inteligência de Dados

Sistema de web-scraping para busca e extração de artigos científicos e jornalísticos, com suporte a download de PDFs. Desenvolvido como parte de uma Iniciação Científica.

Fontes suportadas:
- [The Conversation BR](https://theconversation.com/br) — scraping direto via `requests`
- [ResearchGate](https://www.researchgate.net) — scraping via Selenium (Chrome headless)
- [IEEE Xplore](https://ieeexplore.ieee.org) — scraping via Selenium (Chrome headless)

---

## Como funciona

O sistema busca artigos na fonte selecionada usando as palavras-chave configuradas e, para cada artigo relevante encontrado:

1. Acessa a página do artigo
2. Tenta localizar e baixar um PDF diretamente vinculado
3. Extrai o texto do corpo do artigo como fallback caso não haja PDF
4. Persiste os dados em `artigos.xlsx`

---

## Estrutura de pastas

```
scraper/
├── main.py                       # Ponto de entrada — coleta artigos do site
├── extract_texts.py              # Extrai textos de arquivos já coletados → CSV
├── config.py                     # Configurações globais (URLs, keywords, delays, fontes)
├── requirements.txt              # Dependências Python
│
├── scraper/
│   ├── article_scraper.py        # Coleta de links (The Conversation) e extração de conteúdo
│   ├── selenium_scraper.py       # Coleta de links via Selenium (ResearchGate e IEEE)
│   └── pdf_downloader.py         # Download e validação de PDFs
│
├── storage/
│   └── file_manager.py           # Persistência em XLSX
│
└── data/
    ├── pdfs/                     # PDFs baixados
    └── articles/                 # artigos.xlsx + textos_extraidos.csv
```

---

## Papel de cada arquivo

### `main.py`
Orquestra todo o fluxo: pergunta a fonte e o modo de busca, coleta os links, processa cada artigo, aciona o download de PDF quando disponível e salva os resultados. É o único arquivo que deve ser executado diretamente.

### `config.py`
Centraliza todas as configurações do sistema:
- `SOURCES` — dicionário com as fontes disponíveis e seus IDs
- `BASE_URL` — URL base do The Conversation BR
- `KEYWORDS_*` / `PATTERNS_*` — listas de termos para filtrar artigos relevantes
- `REQUEST_DELAY` — intervalo em segundos entre requisições (evita bloqueio)
- Caminhos dos diretórios de saída (`PDF_DIR`, `ARTICLES_DIR`)

### `scraper/article_scraper.py`
Responsável pela busca no The Conversation BR e pela extração de conteúdo de qualquer fonte:
- `get_article_links(max_pages, source_id)` — despacha para o scraper correto conforme a fonte escolhida
- `get_article_content(url)` — acessa a página de um artigo e extrai título, autor, data, DOI, PDF e texto

### `scraper/selenium_scraper.py`
Scrapers baseados em Selenium (Chrome headless) para sites que bloqueiam `requests` ou usam JavaScript:
- `search_researchgate(...)` — busca publicações no ResearchGate
- `search_ieee(...)` — busca artigos no IEEE Xplore

### `scraper/pdf_downloader.py`
Responsável por baixar PDFs. Valida o `Content-Type` da resposta antes de salvar. Salva os arquivos em `data/pdfs/`.

### `storage/file_manager.py`
Gerencia a persistência dos dados em `artigos.xlsx` e o sistema de checkpoint para retomada de execuções interrompidas.

---

## Instalação e execução

**Pré-requisitos:**
- Python 3.10+
- Google Chrome instalado na máquina (necessário para ResearchGate e IEEE)

```bash
# 1. Entrar na pasta do scraper
cd scraper

# 2. (Recomendado) Criar e ativar um ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# 3. Instalar dependências
pip install -r requirements.txt
```

> Na primeira execução com ResearchGate ou IEEE, o `webdriver-manager` baixa automaticamente o ChromeDriver compatível com a versão do Chrome instalada.

---

### Parte 1 — Coletar artigos do site

```bash
python main.py
```

Ao executar, o sistema primeiro pergunta a fonte:

```
=== Selecione a fonte de busca ===
  [1] The Conversation BR
  [2] ResearchGate
  [3] IEEE Xplore

Escolha:
```

Depois pergunta o modo de busca:

```
=== Web Scraper ===

Como deseja executar a busca?
  [1] Escanear o site todo
  [2] Definir número de páginas
```

- Escolha **1** para varrer o site inteiro (pode demorar bastante)
- Escolha **2** e informe quantas páginas deseja buscar

Se uma execução anterior foi interrompida, o sistema detecta o checkpoint e pergunta se deseja continuar de onde parou.

Resultados salvos em:
- `data/articles/artigos.xlsx` — planilha com título, autor, data, link, DOI e PDF de cada artigo
- `data/pdfs/` — PDFs baixados (quando disponíveis)

---

### Parte 2 — Extrair textos para CSV

Esse script acessa cada artigo coletado, extrai o texto completo e salva em CSV.

**Opção A — usar o `artigos.xlsx` gerado automaticamente:**

```bash
python extract_texts.py
```

Escolha a opção `[1]` no menu.

**Opção B — usar arquivos enviados pelo grupo (xlsx ou csv):**

```bash
python extract_texts.py
```

Escolha a opção `[2]` e informe o caminho de cada arquivo. Pressione Enter em branco para finalizar e iniciar a extração:

```
=== Extrator de Textos ===

Opções:
  [1] Usar artigos.xlsx padrão
  [2] Adicionar arquivos manualmente

Escolha (1 ou 2): 2

Digite o caminho completo de cada arquivo (Enter em branco para finalizar):
  Arquivo 1: C:\Users\voce\Downloads\lista_grupo.xlsx
  [OK] Adicionado: lista_grupo.xlsx
  Arquivo 2: C:\Users\voce\Downloads\outro.csv
  [OK] Adicionado: outro.csv
  Arquivo 3:   ← Enter vazio para iniciar

[INFO] 2 arquivo(s) carregado(s).
  lista_grupo.xlsx: 45 artigos únicos adicionados
  outro.csv: 12 artigos únicos adicionados
```

**Opção C — passar o arquivo direto como argumento:**

```bash
python extract_texts.py caminho/para/arquivo.xlsx
python extract_texts.py caminho/para/arquivo.csv
```

> Os arquivos de entrada precisam ter uma coluna com a URL dos artigos (aceita cabeçalhos: `link`, `url`, `Link`, `URL`, `Link do artigo`).

Resultado salvo em:
- `data/articles/textos_extraidos.csv` — colunas: `titulo, autor, data, url, doi, texto`

---

## Ajustando as palavras-chave

Edite o `config.py` para refletir os termos do seu tema de pesquisa. Há três listas:

- `KEYWORDS_POPULATION` — termos relacionados ao público-alvo (ex: idoso, envelhecimento)
- `KEYWORDS_TOPIC` — termos de tema (ex: saúde mental, demência, qualidade de vida)
- `KEYWORDS_STANDALONE` — termos que sozinhos já indicam artigo relevante (ex: alzheimer, geriatria)

Um artigo é considerado relevante se:
- Contém qualquer termo de `KEYWORDS_STANDALONE`, **ou**
- Contém ao menos um termo de `KEYWORDS_POPULATION` **e** um de `KEYWORDS_TOPIC`

---

## Adicionando novas fontes

1. Adicione a fonte em `SOURCES` no `config.py`
2. Implemente a função de busca em `selenium_scraper.py` (se o site usa JS) ou em `article_scraper.py` (se é HTML estático)
3. Adicione o despacho pelo novo `source_id` em `get_article_links` no `article_scraper.py`
