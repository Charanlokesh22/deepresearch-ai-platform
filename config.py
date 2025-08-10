from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_USER: str = ""
    ELASTICSEARCH_PASS: str = ""
    BASE_DIR: str = "./data"
    DATABASE_URL: str = "sqlite:///./data/db.sqlite"
    # tune
    MAX_CRAWL_PAGES: int = 20

    class Config:
        env_file = "../.env"  # adjust path when running
        env_file_encoding = "utf-8"

settings = Settings()
