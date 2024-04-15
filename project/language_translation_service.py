from typing import Optional

from google.cloud import translate_v2 as translate
from pydantic import BaseModel


class LanguageTranslationResponse(BaseModel):
    """
    The outcome of the translation process, including the translated text and any relevant status information.
    """

    translated_text: str
    status: str
    error: Optional[str] = None


def language_translation(
    source_text: str, source_language: str, target_language: str
) -> LanguageTranslationResponse:
    """
    Translates text from a source language to a target language.

    Args:
    source_text (str): The text to be translated.
    source_language (str): The language code of the source text (e.g., 'en' for English).
    target_language (str): The language code of the target translation (e.g., 'fr' for French).

    Returns:
    LanguageTranslationResponse: The outcome of the translation process, including the translated text and any relevant status information.

    Usage:
    response = language_translation("Hello, world!", "en", "fr")
    if response.status == "success":
        print(response.translated_text)
    else:
        print(f"Translation failed with error: {response.error}")
    """
    try:
        client = translate.Client()
        result = client.translate(
            source_text,
            source_language=source_language,
            target_language=target_language,
        )
        translated_text = result["translatedText"]
        return LanguageTranslationResponse(
            translated_text=translated_text, status="success"
        )
    except Exception as e:
        return LanguageTranslationResponse(
            translated_text="", status="error", error=str(e)
        )
