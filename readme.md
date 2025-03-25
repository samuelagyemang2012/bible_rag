# Bible Study RAG Tool

This project is an **experimental** Retrieval-Augmented Generation (RAG) tool designed to interact with the bible and
help generate summaries and bible study questions. It is compatible with <code>openai</code>, <code>ollama</code>
and <code>huggingface</code> for embedding.

**Disclaimer:**

This is an experimental project. The generated answers and insights may not always align with traditional
interpretations. We encourage critical thinking and independent verification. This tool is intended to spark exploration
and discussion, not to provide definitive theological answers.

**Embeddings:**

For the purpose of semantic search and retrieval, the NIV Bible was processed by generating embeddings via <code>
sentence-transformers/all-MiniLM-L6-v2</code> and <code>nomic-ai/nomic-embed-text-v1.5</code>, subsequently persisted
within a <code>chromadb</code> with a <code>chunk_size = 500</code> characters and <code>chunk_overlap = 200</code>.
The chapters of each book of Bible is also embedded to help with chapter summaries and question generation.

| Type               | Vector Store                            |
|--------------------|-----------------------------------------|
| Chapter Embbedings | minilm_l6_v2_chapters_database          |
| Document Embeddings | minilm_l6_v2_database                   |
| Chapter Embbedings | nomic_embed_text_v1.5_chapters_database |
| Document Embeddings | nomic_embed_text_v1.5_database          |

[Download the vector stores here](https://drive.google.com/drive/folders/17ILL-qkbBRCB7oQlS3o8lyCF59pc78ka?usp=sharing)

To use <code>openai</code> models, create a <code>.env</code> file add <code>OPENAI_API_KEY = "YOUR KEY"</code>
This is an open-source, experimental project. We welcome contributions, feedback, and collaboration. Please be aware
that this project is in active development, and changes may occur frequently.

**Run:**

<code>python cli.py</code> for the CLI

<code>python cli.py -m gui</code> for GUI version via <code>streamlit</code>
