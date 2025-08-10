import asyncio
import httpx
from bs4 import BeautifulSoup
import tldextract
import hashlib
from urllib.parse import urljoin, urldefrag
from .config import settings

async def fetch(client, url):
    try:
        resp = await client.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.text
    except Exception:
        return None

def normalize_url(base, link):
    try:
        href = urljoin(base, link)
        href, _ = urldefrag(href)
        return href
    except:
        return None

async def crawl(start_urls, max_pages=20):
    seen = set()
    to_visit = list(start_urls)
    results = []

    async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
        while to_visit and len(seen) < max_pages:
            url = to_visit.pop(0)
            if url in seen: continue
            seen.add(url)
            html = await fetch(client, url)
            if not html: continue
            soup = BeautifulSoup(html, "html.parser")
            title_tag = soup.find("title")
            title = title_tag.text.strip() if title_tag else url
            texts = []
            for p in soup.find_all("p"):
                texts.append(p.get_text(separator=" ", strip=True))
            content = "\n\n".join(texts)[:20000]  # limit size

            results.append({"url": url, "title": title, "content": content})

            # find links for same domain
            base_domain = tldextract.extract(url).registered_domain
            for a in soup.find_all("a", href=True):
                new_url = normalize_url(url, a["href"])
                if not new_url: continue
                nd = tldextract.extract(new_url).registered_domain
                if nd == base_domain and new_url not in seen:
                    to_visit.append(new_url)

    return results
