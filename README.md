# PromptCaching

A Streamlit web app for banking Q&A with intelligent caching using MongoDB and semantic search.

## Overview

PromptCaching lets users ask banking-related questions and get simple, clear answers powered by LLMs. The app caches responses in MongoDB for fast retrieval, including semantic similarity matching using sentence embeddings.

## Features

- Ask any banking question and receive a friendly, easy-to-understand answer.
- Caching with MongoDB: instant retrieval for repeated or similar questions.
- Semantic search: matches similar questions using embeddings.
- Option to purge cache and clear chat history from the sidebar.
- Chat history display.

## Project Structure

- `app.py`: Streamlit web app UI and main logic.
- `my_agent.py`: Defines the LLM agent and handles Q&A with caching.
- `prompt_caching.py`: Implements MongoDB caching and semantic search.
- `setup.txt`: Python dependencies.
- `run.ipynb`: Colab notebook for remote app access.
- `PromptCaching.pdf`: Documentation.

## Setup

1. **Install dependencies**
   ```sh
   pip install -r setup.txt
   ```

2. **MongoDB Atlas (recommended for Colab)**
   - Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
   - Whitelist your IP (`0.0.0.0/0` for testing).
   - Create a database user.
   - Copy your connection string.

3. **Environment variables**
   - Create a `.env` file:
     ```
     MONGODB_CONNECTION_STRING=your_mongodb_atlas_connection_string
     HF_API_KEY=your_huggingface_api_key
     MODEL_API_KEY=your_huggingface_api_key
     NGROK_AUTH_TOKEN=your_ngrok_auth_token
     ```

## Usage

- Run the app locally:
  ```sh
  streamlit run app.py
  ```
- Or use `run.ipynb` in Google Colab for remote access.

## Caching Details

- Responses are stored in MongoDB (`prompt_cache_db.cache_entries`).
- Semantic similarity uses sentence-transformers (threshold: 0.85).
- Each cache entry includes: prompt, response, embedding, timestamp, and metadata.

## Authors

Trung Hiếu

---

**Note:**  
If running on Colab, you must use MongoDB Atlas (local MongoDB is not supported).