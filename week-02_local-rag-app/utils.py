import yaml
from rag.embedder import Embedder
from rag.retriever import Retriever
from rag.llm_wrapper import LLMWrapper
from rag.chain import RAGChain

def load_config(config_path: str):
    """
    Load the YAML configuration file.
    """
    try:
        with open(config_path) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None

def initialize_components(cfg):
    """
    Initialize the Embedder, Retriever, and RAGChain components.
    """
    try:
        embedder = Embedder(cfg["embedding"]["model"])
        retriever = Retriever(embedder, **cfg["retriever"])
        llm = LLMWrapper(cfg["llm"])
        return retriever, llm, RAGChain(retriever, llm)
    except Exception as e:
        print(f"Error initializing components: {e}")
        return None, None, None

def prepare_retriever(retriever: Retriever) -> bool:
    """
    Prepare the retriever by indexing documents.
    """
    try:
        print("Attempting to load the retriever index...")
        if not retriever.load_index():
            print("Warn: Index store not found or invalid. Starting indexation.")
            retriever.index_documents()
            print("Indexation completed successfully.")
        else:
            print("Index loaded successfully.")
    except FileNotFoundError:
        print("Warn: Index store not found. Starting indexation.")
        retriever.index_documents()
        print("Indexation completed successfully.")
        return False
    except Exception as e:
        print(f"Error loading or indexing documents: {e}")
        return False
    return True