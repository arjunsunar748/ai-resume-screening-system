import re
import string


class TextCleanerService:
    """
    Dual-track text cleaning service for vector embeddings and skill extraction.
    """

    def clean_for_embeddings(self, text: str) -> str:
        """
        Cleans text while preserving sentence structures and key technical punctuation
        optimal for sentence-transformers / embedding models.
        """
        if not text:
            return ""

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove unprintable / non-ASCII noise characters
        text = "".join(char for char in text if char in string.printable)

        return text.strip()

    def clean_for_skills(self, text: str) -> str:
        """
        Cleans and normalizes text for exact keyword and regex skill extraction.
        """
        if not text:
            return ""

        text = text.lower()
        # Preserve specific tech tokens like c++, c#, .net, node.js
        text = re.sub(r"[^\w\s\+#\.]", " ", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()


text_cleaner_service = TextCleanerService()