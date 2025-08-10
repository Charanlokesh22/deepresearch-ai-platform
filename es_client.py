from elasticsearch import Elasticsearch
from .config import settings

es = Elasticsearch(
    [settings.ELASTICSEARCH_URL],
    basic_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASS) if settings.ELASTICSEARCH_USER else None,
)

INDEX_NAME = "deepresearch_docs"

def ensure_index():
    if not es.indices.exists(index=INDEX_NAME):
        mapping = {
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "url": {"type": "keyword"},
                    "content": {"type": "text"},
                    "embedding": {"type": "dense_vector", "dims": 768},
                    "source_score": {"type": "float"},
                    "published_at": {"type": "date", "ignore_malformed": True}
                }
            }
        }
        es.indices.create(index=INDEX_NAME, body=mapping)

def index_document(doc_id: str, body: dict):
    es.index(index=INDEX_NAME, id=doc_id, body=body)

def search_semantic(query_vector, top_k=5):
    # requires ES kNN support or script_score; simplified example:
    resp = es.search(
        index=INDEX_NAME,
        body={
            "size": top_k,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.vec, 'embedding') + 1.0",
                        "params": {"vec": query_vector}
                    }
                }
            }
        }
    )
    return resp
