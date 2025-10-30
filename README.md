# DocstoTeles

Aplicação RAG (Retrieval-Augmented Generation) simples construída com Streamlit e LangChain para permitir busca e chat sobre coleções de documentos Markdown.

## Descrição

Este projeto permite importar coleções de documentos (arquivos .md) como um índice de vetores e fazer perguntas usando um modelo LLM (via Groq). Foi pensado para experimentação local: scrapping/importação de documentos, criação de embeddings e busca por similaridade para responder perguntas com contexto.

Principais componentes:
- Interface Web: Streamlit (`docstoteles/app.py`).
- Serviço RAG: implementação em `docstoteles/service/rag.py` (carrega coleções, cria embeddings, gera respostas).
- Carregamento de documentos: `langchain_community.document_loaders.DirectoryLoader` (arquivos .md).

## Recursos

- Carregar coleções locais de Markdown (pasta `data/collections/<nome>`).
- Gerar embeddings com HuggingFace (`sentence-transformers`) e armazená-los com FAISS.
- Fazer perguntas (chat) com recuperação de contexto (RetrievalQA).

## Requisitos

- Python 3.11+ (o projeto foi testado com 3.13 em um venv local).
- Windows (instruções com PowerShell). Para Linux/macOS comandos são semelhantes.

Dependências principais (veja também `requirements.txt`):
- streamlit
- langchain-core / langchain-community / langchain-huggingface
- sentence-transformers
- faiss-cpu (ou faiss-gpu se tiver CUDA compatível)
- langchain_groq (para usar a API Groq)

## Instalação (Windows PowerShell)

1. Clone o repositório e entre na pasta do projeto:

```powershell
cd C:\caminho\para\chat_with_rag
```

2. Crie e ative um ambiente virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Atualize pip e instale requisitos:

```powershell
python -m pip install --upgrade pip
# Use o arquivo completo de dependências gerado: `requirements-full.txt`.
# O arquivo `requirements.txt` original pode ser uma versão mínima; prefira o
# `requirements-full.txt` para obter todas as dependências usadas neste projeto.
python -m pip install -r requirements-full.txt
```

4. Pacotes adicionais frequentemente necessários (se não já no requirements):

```powershell
python -m pip install sentence-transformers
python -m pip install faiss-cpu    # se você NÃO tiver GPU/CUDA
# ou para GPU (verifique compatibilidade com sua CUDA/Python):
# python -m pip install faiss-gpu
python -m pip install langchain-huggingface
```

Observação: Instalar `faiss` no Windows pode ser sensível à versão do Python. Se encontrar problemas, veja a documentação do FAISS ou use uma versão de Python compatível (por exemplo 3.10/3.11 dependendo dos binários disponíveis) ou usar contêiner/docker.

## Configuração de variáveis de ambiente

Crie um arquivo `.env` na raiz (ou exporte as variáveis no sistema). Exemplo mínimo em `.env`:

```properties
FIRECRAWL_API_URL=http://localhost:3002
FIRECRAWL_API_KEY=
GROQ_API_KEY=seu_groq_api_key_aqui
```

O `GROQ_API_KEY` é necessário para usar `langchain_groq.ChatGroq`.

Carregue as variáveis com `python-dotenv` se a aplicação fizer isso automaticamente (o projeto já importa `load_dotenv` em alguns lugares).

## Estrutura do projeto

Raiz relevante:

- `docstoteles/app.py` — Streamlit app (ponto de entrada).
- `docstoteles/presentation/chat.py` — interface de chat.
- `docstoteles/presentation/scraping.py` — tela de scrapping/import.
- `docstoteles/service/rag.py` — lógica de RAG, embeddings, FAISS, RetrievalQA.
- `data/collections/` — pastas de coleções contendo arquivos .md.
- `requirements.txt` — dependências do projeto.

Para adicionar uma nova coleção, crie uma pasta em `data/collections/<nome>` e adicione arquivos `.md` com o conteúdo que deseja indexar.

## Como executar (Streamlit)

Depois de ativar o venv e instalar dependências:

```powershell
set -a  # (opcional) exporta variáveis do .env para sessão — PowerShell normalmente usa Set-Item ou dot-source o .env
# método simples: editar .env e garantir que a aplicação carregue com python-dotenv
streamlit run docstoteles/app.py
```

No navegador vá para http://localhost:8501 por padrão.

## Uso

1. Na sidebar escolha o modo: `Chat` ou `Scrapping`.
2. Em `Scrapping` você pode importar / criar coleções (dependendo da UI presente) — certifique-se de que arquivos `.md` estão em `data/collections/<nome>`.
3. Em `Chat` selecione a coleção que quer usar e envie perguntas; o sistema usa o RAG service para recuperar trechos relevantes e gerar respostas.

## Problemas comuns / Troubleshooting

- ImportError: Could not import sentence_transformers
	- Solução: rode `python -m pip install sentence-transformers` no ambiente virtual.

- ImportError: Could not import faiss
	- Para CPU em Windows: `python -m pip install faiss-cpu` (veja compatibilidade com sua versão do Python).
	- Para GPU: `python -m pip install faiss-gpu` (somente se tiver CUDA compatível).
	- Se falhar no Windows, considere instalar em Linux, usar docker, ou usar uma alternativa (por exemplo, `Chroma` como vectorstore) — exigir mudanças de código.

- Deprecation warnings do LangChain
	- Atualize imports conforme mensagens (ex.: `from langchain_huggingface import HuggingFaceEmbeddings`) e troque `chain.run(...)` por `chain.invoke({...})` conforme necessário.

- Erros do modelo Groq (model_decommissioned)
	- Se receber mensagem de modelo descontinuado, troque `model_name` em `docstoteles/service/rag.py` para um modelo ativo listado pela API Groq (ex.: `groq/compound` ou `groq/compound-mini`).

## Testes rápidos

- Verifique se o ambiente está correto e pacotes instalados:

```powershell
python -c "import sentence_transformers, faiss; print('OK')"
```

- Rodar a aplicação e abrir a UI: `streamlit run docstoteles/app.py`.

## Sugestões de melhorias (próximos passos)

- Adicionar scripts de CI para verificar install/testes.
- Incluir testes unitários básicos para `RAGService` (mockando embeddings e vectorstore).
- Suporte opcional a backends alternativos de vectorstore (Chroma, Milvus) para facilitar execução em ambientes sem FAISS.

## Contribuição

1. Fork e branch com feature/bugfix.
2. Abra um Pull Request descrevendo mudanças.

## Licença

Escolha e adicione a sua licença (ex.: MIT) se desejar publicar o repositório.

---

Se quiser, eu posso:
- Atualizar o `requirements.txt` com versões testadas.
- Adicionar um `README` em inglês também.
- Incluir um exemplo de coleção em `data/collections/example` com alguns `.md` de teste.

Diga qual desses extras você quer que eu faça agora.

# docstoteles