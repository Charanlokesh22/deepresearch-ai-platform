DeepResearch AI – Autonomous AI Research Agent

A production-grade AI platform that can autonomously research any topic end-to-end — from searching and extracting information to summarizing, analyzing, and generating comprehensive reports with citations. Built using Python, LangChain, OpenAI API, Elasticsearch, FastAPI, and React, it demonstrates multi-agent orchestration and advanced NLP capabilities.

How It Works

This system automates the entire research process. The web crawler and API integrations collect relevant data from multiple sources. The NLP engine processes and extracts key facts, while a reliability scoring mechanism filters out low-quality or biased content. A writing agent then compiles the findings into a well-structured PDF or HTML report with proper citations.


The application follows a modular architecture:-


-Search Agent gathers information via web crawling and APIs.
-Analysis Agent performs NLP-based summarization and fact extraction.
-Scoring Agent evaluates the credibility of sources.
-Writer Agent generates final structured reports.
-Frontend provides an interactive interface for initiating research and viewing results.


Features

-Autonomous topic research with minimal human input.
-Multi-source data gathering (web + APIs).
-NLP-based summarization and fact extraction.
-Source reliability scoring for content credibility.
-Auto-generated PDF/HTML research reports with citations.
-FastAPI backend with LangChain-based agent orchestration.
-Full-text search powered by Elasticsearch.
-Responsive React-based frontend.



Installation Steps

Clone the repository:
-git clone https://github.com/Charanlokesh22/deepresearch-ai.git
cd deepresearch-ai

Start all services using Docker Compose:
-docker-compose up --build

Access Points

-Frontend: http://localhost:3000
-Backend API: http://localhost:8000/api
-Elasticsearch: http://localhost:9200



Usage

-Enter a topic in the frontend interface.
-The Search Agent retrieves relevant articles, papers, and data.
-The Analysis Agent processes and summarizes the findings.
-The Writer Agent compiles a professional report.
-Download or view the report in PDF or HTML format.

Security

-API key-based authentication for backend endpoints.
-Restricted crawler behavior to comply with robots.txt guidelines.
-Sanitized data pipelines to prevent injection attacks.


AI Components

The AI pipeline uses multiple agents in LangChain:

-Search Agent: Crawls the web and calls APIs.
-Analysis Agent: Uses NLP to extract facts and summarize.
-Scoring Agent: Assigns credibility scores to sources.
-Writer Agent: Generates final reports with proper formatting.

