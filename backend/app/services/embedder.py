from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.core.config import settings


class EmbedderService:
    """
    Production service for generating dense vector embeddings and calculating semantic similarity.
    Uses lazy initialization to keep the neural network loaded in memory.
    """

    def __init__(self, model_name: str = settings.EMBEDDING_MODEL_NAME):
        self.model_name = model_name
        self._model: Union[SentenceTransformer, None] = None

    @property
    def model(self) -> SentenceTransformer:
        """
        Lazy-loads the SentenceTransformer model into memory on demand.
        """
        if self._model is None:
            print(f"[INFO] Loading Sentence Transformer model '{self.model_name}' into memory...")
            self._model = SentenceTransformer(self.model_name)
            print("[SUCCESS] Model loaded and ready for vector inference.")
        return self._model

    def get_embedding(self, text: str) -> np.ndarray:
        """
        Generates a 384-dimensional dense vector representation for a single text input.

        Args:
            text (str): Preprocessed text input.

        Returns:
            np.ndarray: 1D array of shape (384,)
        """
        if not text or not text.strip():
            # Return zero vector if text is empty
            return np.zeros(384, dtype=np.float32)

        return self.model.encode(text, convert_to_numpy=True)

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Computes the cosine similarity score between two raw or cleaned text strings.

        Args:
            text1 (str): Cleaned resume text.
            text2 (str): Cleaned job description text.

        Returns:
            float: Normalized score between 0.0 and 100.0
        """
        if not text1.strip() or not text2.strip():
            return 0.0

        vec1 = self.get_embedding(text1)
        vec2 = self.get_embedding(text2)

        # Reshape vectors to 2D arrays (1, N) required by scikit-learn
        similarity = cosine_similarity([vec1], [vec2])[0][0]

        # Convert similarity bounded [-1.0, 1.0] to float range [0.0, 100.0]
        bounded_score = max(0.0, float(similarity)) * 100.0
        return round(bounded_score, 2)


# Instantiate single global instance for dependency injection across endpoints
embedder_service = EmbedderService()