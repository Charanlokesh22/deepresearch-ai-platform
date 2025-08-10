from jinja2 import Template
import os
from weasyprint import HTML
from datetime import datetime
from .config import settings

REPORT_DIR = os.path.join(settings.BASE_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

REPORT_TEMPLATE = """
<html>
<head><meta charset="utf-8"/><title>DeepResearch Report</title></head>
<body>
<h1>Research Report: {{ query }}</h1>
<p><em>Generated: {{ generated_at }}</em></p>
<h2>Executive Summary</h2>
<p>{{ summary }}</p>
<h2>Key Findings</h2>
<ul>
{% for f in findings %}
  <li>{{ f }}</li>
{% endfor %}
</ul>

<h2>Sources & Citations</h2>
<ol>
{% for s in sources %}
  <li><a href="{{ s.url }}">{{ s.title }}</a> — score: {{ "%.2f"|format(s.score) }}</li>
{% endfor %}
</ol>
</body>
</html>
"""

def generate_report(query, summary, findings, sources, uid):
    rendered = Template(REPORT_TEMPLATE).render(
        query=query,
        generated_at=datetime.utcnow().isoformat(),
        summary=summary,
        findings=findings,
        sources=sources
    )
    html_path = os.path.join(REPORT_DIR, f"{uid}.html")
    pdf_path = os.path.join(REPORT_DIR, f"{uid}.pdf")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    HTML(string=rendered).write_pdf(pdf_path)
    return {"html": html_path, "pdf": pdf_path}
