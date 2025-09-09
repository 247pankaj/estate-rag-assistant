import os
import sys
import json
from typing import Dict

from dotenv import load_dotenv
from utils.config_loader import load_config
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from core.estate_exception import EstateRAGException
from logger import LOGGER as log

class ApiKeyManager:
    """
    Manages retrieval and validation of required API keys from environment variables or secrets.
    """
    REQUIRED_KEYS = ["GROQ_API_KEY", "GOOGLE_API_KEY"]

    def __init__(self) -> None:
        self.api_keys: Dict[str, str] = {}
        self._load_api_keys()

    def _load_api_keys(self) -> None:
        raw_keys = os.getenv("API_KEYS")

        if raw_keys:
            try:
                parsed = json.loads(raw_keys)
                if not isinstance(parsed, dict):
                    raise ValueError("API_KEYS must be a JSON object")
                self.api_keys.update(parsed)
                log.info("API keys loaded from ECS secret")
            except Exception as e:
                log.warning("Failed to parse API_KEYS", error=str(e))

        for key in self.REQUIRED_KEYS:
            if key not in self.api_keys:
                env_val = os.getenv(key)
                if env_val:
                    self.api_keys[key] = env_val
                    log.info(f"API key '{key}' loaded from environment variable")

        missing_keys = [k for k in self.REQUIRED_KEYS if k not in self.api_keys]
        if missing_keys:
            log.error("Missing required API keys", missing_keys=missing_keys)
            raise EstateRAGException("Missing API keys", sys)

        # Masked logging for security
        masked_keys = {k: v[:6] + "..." for k, v in self.api_keys.items()}
        log.info("API keys successfully loaded", keys=masked_keys)

    def get(self, key: str) -> str:
        """
        Retrieve a specific API key.
        """
        if key not in self.api_keys:
            raise KeyError(f"API key '{key}' is missing")
        return self.api_keys[key]


class ModelLoader:
    """
    Loads embedding and LLM models based on configuration and environment.
    """

    def __init__(self) -> None:
        self._initialize_environment()
        self.api_key_mgr = ApiKeyManager()
        self.config = load_config()
        log.info("Configuration loaded", config_keys=list(self.config.keys()))

    def _initialize_environment(self) -> None:
        env = os.getenv("ENV", "local").lower()
        if env != "production":
            load_dotenv()
            log.info("Environment: LOCAL (.env loaded)")
        else:
            log.info("Environment: PRODUCTION")

    def load_embeddings(self) -> GoogleGenerativeAIEmbeddings:
        """
        Load Google Generative AI embedding model.
        """
        try:
            model_name = self.config["embedding_model"]["model_name"]
            log.info("Initializing embedding model", model=model_name)
            return GoogleGenerativeAIEmbeddings(
                model=model_name,
                google_api_key=self.api_key_mgr.get("GOOGLE_API_KEY")
            )
        except Exception as e:
            log.error("Failed to initialize embedding model", error=str(e))
            raise EstateRAGException("Embedding model initialization failed", sys)

    def load_llm(self):
        """
        Load the configured LLM model based on provider.
        """
        try:
            llm_config_block = self.config["llm"]
            provider_key = os.getenv("LLM_PROVIDER", "google")

            if provider_key not in llm_config_block:
                raise ValueError(f"LLM provider '{provider_key}' not found in configuration")

            llm_config = llm_config_block[provider_key]
            provider = llm_config.get("provider")
            model_name = llm_config.get("model_name")
            temperature = llm_config.get("temperature", 0.2)
            max_tokens = llm_config.get("max_output_tokens", 2048)

            log.info("Initializing LLM", provider=provider, model=model_name)

            if provider == "google":
                return ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=self.api_key_mgr.get("GOOGLE_API_KEY"),
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            elif provider == "groq":
                return ChatGroq(
                    model=model_name,
                    api_key=self.api_key_mgr.get("GROQ_API_KEY"),
                    temperature=temperature
                )
            else:
                raise ValueError(f"Unsupported LLM provider: {provider}")

        except Exception as e:
            log.error("Failed to initialize LLM", error=str(e))
            raise EstateRAGException("LLM initialization failed", sys)


if __name__ == "__main__":
    try:
        loader = ModelLoader()

        # Embedding Test
        embeddings = loader.load_embeddings()
        print(f"✅ Embedding Model Loaded: {embeddings}")
        result = embeddings.embed_query("Hello, how are you?")
        print(f"🔍 Embedding Result: {result}")

        # LLM Test
        llm = loader.load_llm()
        print(f"✅ LLM Loaded: {llm}")
        response = llm.invoke("Hello, how are you?")
        print(f"💬 LLM Response: {response.content}")

    except Exception as e:
        log.critical("Startup failure", error=str(e))
        sys.exit(1)
