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
├── main.py                  # Ponto de entrada — coleta artigos do site
├── extract_texts.py         # Extrai textos de arquivos já coletados → CSV
├── config.py                # Configurações globais (URLs, keywords, delays)
├── requirements.txt         # Dependências Python
│
├── scraper/
│   ├── article_scraper.py   # Coleta de links e extração de conteúdo
│   └── pdf_downloader.py    # Download e validação de PDFs
│
├── storage/
│   └── file_manager.py      # Persistência em XLSX
│
└── data/
    ├── pdfs/                # PDFs baixados
    └── articles/            # artigos.xlsx + textos_extraidos.csv
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
```

---

### Parte 1 — Coletar artigos do site

```bash
python main.py
```

Ao executar, o sistema pergunta o modo de busca:

```
=== Web Scraper - The Conversation BR ===

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

Para usar outra fonte, altere `BASE_URL` e, se necessário, os seletores CSS em `article_scraper.py` para corresponder à estrutura HTML do novo portal.
