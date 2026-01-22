# Banking RAG System – PDF Based (Offline & Free)
## Overview

This project implements a Retrieval-Augmented Generation (RAG) system designed for banking and legal use cases, such as:

- Settlement of death claims
- RBI / bank policy interpretation
- Nominee & legal heir rules
- Compliance-related Q&A
The system does not use OpenAI or any paid APIs and works fully offline using open-source models.

## Key Features

- Reads bank policy PDFs directly from URLs
- Semantic search using vector embeddings
- Retrieves relevant policy sections
- Generates grounded answers only from documents
- No hallucinations (banking-safe)
- Zero cost (no API keys required)
- Modular design (easy to extend to SharePoint, Word, HTML)

  ## Architecture 

<img width="287" height="427" alt="image" src="https://github.com/user-attachments/assets/c2aabd23-3ca2-4af5-829f-870319c8d4f6" />

## Installation
### Clone the repository (or copy files)
```bash
git clone <your-repo-url>
cd banking-rag
```
## Install dependencies
```bash
pip install -r requirements.txt
```


## If using Jupyter Notebook:

```bash
!pip install -r requirements.txt

```
Then restart the kernel.

# Possible Enhancements

- Page number citations
- Multiple PDF ingestion
- SharePoint / OneDrive integration
- Reranking models
- Confidence scoring
- Role-based access
- Azure Databricks deployment
