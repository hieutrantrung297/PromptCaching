import os
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv("MONGODB_CONNECTION_STRING")
DB_NAME = "prompt_cache_db"
COLLECTION_NAME = "cache_entries"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

SIM_THRESHOLD = 0.85

model_name_emb = "Alibaba-NLP/gte-multilingual-base"
embedder = SentenceTransformer(model_name_emb, token=os.getenv("HF_API_KEY"), trust_remote_code=True)

def _generate_id(text: str) -> str:
    content = text.strip().lower().encode("utf-8")
    return hashlib.md5(content).hexdigest()

def _get_vector(text: str) -> np.ndarray:
    return embedder.encode(text)

def _similarity_score(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    return float(np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b)))

def retrieve_from_cache(query: str) -> Optional[Dict[str, Any]]:
    query_id = _generate_id(query)
    # Exact match
    entry = collection.find_one({"_id": query_id})
    if entry:
        return entry

    # Semantic search
    input_vector = _get_vector(query)
    top_match = None
    top_score = 0.0

    for item in collection.find({}):
        stored_vector = np.array(item.get("embedding", []))
        if stored_vector.size == 0:
            continue
        score = _similarity_score(input_vector, stored_vector)
        if score >= SIM_THRESHOLD and score > top_score:
            top_match = item
            top_score = score

    return top_match

def store_response(query: str, result: str, extra_info: Optional[Dict[str, Any]] = None) -> None:
    entry_id = _generate_id(query)
    entry = {
        "_id": entry_id,
        "prompt": query,
        "response": result,
        "embedding": _get_vector(query).tolist(),
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": extra_info or {}
    }
    collection.replace_one({"_id": entry_id}, entry, upsert=True)

def purge_cache() -> None:
    collection.delete_many({})