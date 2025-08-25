# PromptCaching: Simple Banking Knowledge Q&A with Caching

This project is a Streamlit web app that answers banking-related questions in simple, easy-to-understand language. It uses LLMs via [CrewAI](https://github.com/joaomdmoura/crewAI) and caches responses for faster future retrieval, including semantic similarity search.

## Features

- Ask any banking question and get a friendly, clear answer.
- Responses are cached for instant retrieval if a similar question is asked again.
- Semantic search: similar questions are matched using sentence embeddings.
- Cache can be purged from the sidebar.
- Chat history is shown in the app.

## Project Structure

- [`app.py`](app.py): Streamlit web app UI and logic.
- [`my_agent.py`](my_agent.py): Defines the LLM agent and handles answering questions with caching.
- [`prompt_caching.py`](prompt_caching.py): Implements caching, semantic search, and cache management.
- [`setup.txt`](setup.txt): Python dependencies.
- `PromptCaching.pdf`: Documentation (not parsed here).
- `run.ipynb`: Colab notebook for running the app with ngrok tunneling.

## Run
- Use the provided Colab notebook ([run.ipynb](run.ipynb)) for remote access.

## Usage

- Enter your banking question in the app.
- The agent will answer using the LLM.
- If your question (or a similar one) was asked before, the cached answer is returned instantly.
- Use the sidebar to clear chat history or purge the cache.

## Caching Details

- Caches responses in `./cache/data_store` as JSON files.
- Uses sentence-transformers for semantic similarity (threshold: 0.85).
- Stores prompt, response, embedding, timestamp, and metadata.

**Authors:**  
Trung Hiếu