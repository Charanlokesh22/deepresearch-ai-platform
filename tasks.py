import uuid
import asyncio
from .crawler import crawl
from .pipeline import process_and_index
from .es_client import search_semantic
from .report_generator import generate_report
from .config import settings
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from .es_client import INDEX_NAME, es

# simple in-memory task store (replace with DB for production)
TASKS = {}

async def run_research_job(query, start_urls):
    uid = str(uuid.uuid4())
    TASKS[uid] = {"status": "running", "query": query, "result": None}

    # 1) crawl
    crawled = await crawl(start_urls, max_pages=settings.MAX_CRAWL_PAGES)

    # 2) index
    process_and_index(crawled)

    # 3) retrieve top docs for query (semantic + keyword)
    # compute query embedding
    from langchain.embeddings import OpenAIEmbeddings
    emb = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY).embed_query(query)

    resp = search_semantic(emb, top_k=6)
    hits = resp["hits"]["hits"]
    docs = []
    for h in hits:
        src = h["_source"]
        docs.append(Document(page_content=src["content"], metadata={"title": src.get("title"), "url": src.get("url"), "score": src.get("source_score")}))

    # 4) multi-doc summarization using LangChain
    if docs:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        docs_chunks = []
        for d in docs:
            docs_chunks += text_splitter.split_text(d.page_content)
        docs_as_documents = [Document(page_content=chunk) for chunk in docs_chunks[:20]]  # limit chunks

        llm = OpenAI(openai_api_key=settings.OPENAI_API_KEY, temperature=0.2)
        chain = load_summarize_chain(llm, chain_type="map_reduce")  # map_reduce summarization
        summary = chain.run(docs_as_documents)
    else:
        summary = "No sources found."

    # 5) extract key findings (simple prompt with LLM)
    prompt = PromptTemplate(input_variables=["summary"], template="Extract the 5 most important findings from the following summary:\n\n{summary}")
    llm = OpenAI(openai_api_key=settings.OPENAI_API_KEY, temperature=0.2)
    chain2 = LLMChain(llm=llm, prompt=prompt)
    findings_raw = chain2.run({"summary": summary})
    findings = [f.strip() for f in findings_raw.split("\n") if f.strip()][:10]

    # collect top sources with metadata
    sources = []
    for h in hits:
        src = h["_source"]
        sources.append({"url": src["url"], "title": src.get("title", src["url"]), "score": src.get("source_score", 0)})

    # 6) generate report (HTML + PDF)
    report_paths = generate_report(query, summary, findings, sources, uid)

    TASKS[uid]["status"] = "completed"
    TASKS[uid]["result"] = {"summary": summary, "findings": findings, "sources": sources, "report": report_paths}
    return uid

def submit_job_background(loop, query, start_urls):
    return asyncio.run_coroutine_threadsafe(run_research_job(query, start_urls), loop)
