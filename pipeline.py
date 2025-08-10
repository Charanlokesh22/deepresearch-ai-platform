import hashlib
import os
from datetime import datetime
from .es_client import index_document
from .config import settings
from langchain.embeddings import OpenAIEmbeddings
from .config import settings
import random

embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

def make_doc_id(url):
    return hashlib.sha1(url.encode()).hexdigest()

def compute_source_score(text, url):
    # simple heuristics: length, presence of dates, domain trust (placeholder)
    score = 0.5
    if len(text) > 500:
        score += 0.2
    if "journal" in url or "edu" in url:
        score += 0.2
    # random small noise to avoid all ties
    score += random.uniform(0, 0.05)
    return min(score, 1.0)

def process_and_index(docs):
    for d in docs:
        doc_id = make_doc_id(d["url"])
        emb = embeddings.embed_query(d["content"])  # returns list[float]
        body = {
            "title": d["title"],
            "url": d["url"],
            "content": d["content"],
            "embedding": emb,
            "source_score": compute_source_score(d["content"], d["url"]),
            "published_at": datetime.utcnow().isoformat()
        }
        index_document(doc_id, body)
