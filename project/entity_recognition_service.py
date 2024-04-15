from typing import List, Optional

import spacy
from pydantic import BaseModel
from spacy.language import Language


class Entity(BaseModel):
    """
    A single entity identified in the text, along with its category.
    """

    text: str
    category: str
    confidence: float


class EntityRecognitionResponse(BaseModel):
    """
    This model represents the output of the entity recognition process, providing a list of identified entities along with their categories.
    """

    entities: List[Entity]


def entity_recognition(
    text: str, language: Optional[str] = None
) -> EntityRecognitionResponse:
    """
    Identifies key entities within the input text.

    Args:
        text (str): The unstructured text input from which entities will be identified and categorized.
        language (Optional[str]): Optional language parameter to optimize the entity recognition process for texts in specific languages.

    Returns:
        EntityRecognitionResponse: This model represents the output of the entity recognition process, providing a list of identified entities along with their categories.

    Raises:
        ValueError: If the specified language model is not supported or not installed.
    """
    nlp: Language
    if not language or language == "en":
        lang_model = "en_core_web_sm"
    else:
        lang_model = f"{language}_core_news_sm"
    try:
        nlp = spacy.load(lang_model)
    except OSError:
        raise ValueError(
            f"Language model for '{language}' not found. Please install the spaCy language model '{lang_model}'."
        )
    doc = nlp(text)
    entities = [
        Entity(
            text=ent.text, category=ent.label_, confidence=ent.similarity(nlp(ent.text))
        )
        for ent in doc.ents
    ]
    response = EntityRecognitionResponse(entities=entities)
    return response
