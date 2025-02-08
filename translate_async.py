import asyncio
import aiohttp
from transformers import pipeline, M2M100Tokenizer, M2M100ForConditionalGeneration

# --- Initialize Models ---
lang_detector = pipeline("text-classification", model="papluca/xlm-roberta-base-language-detection")
m2m_tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
m2m_model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")

def detect_language(text: str) -> str:
    """Detects the language of a given text."""
    if text.strip() == "":
        return "Unknown"
    
    result = lang_detector(text, top_k=1)
    return result[0]['label']

def translate_text(text: str, src_lang: str, tgt_lang: str) -> str:
    """Translates text from source language to target language."""
    if text.strip() == "":
        return ""
    
    m2m_tokenizer.src_lang = src_lang.lower()
    encoded = m2m_tokenizer(text, return_tensors="pt")
    generated_tokens = m2m_model.generate(
        **encoded,
        forced_bos_token_id=m2m_tokenizer.get_lang_id(tgt_lang.lower())
    )
    return m2m_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

async def fetch_translation(session, text, target_lang):
    """Handles detection and translation asynchronously for each request."""
    try:
        detected_lang = detect_language(text)
        translation = translate_text(text, src_lang=detected_lang, tgt_lang=target_lang)
        return {"text": text, "detected_lang": detected_lang, "translation": translation}
    except Exception as e:
        return {"text": text, "error": str(e)}

async def process_requests(text_list, target_lang):
    """Sends 50 simultaneous requests."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_translation(session, text, target_lang) for text in text_list]
        responses = await asyncio.gather(*tasks)
    return responses

def main():
    """Runs the async function and prints results."""
    texts = ["Hello!", "Bonjour!", "Hola!", "Guten Tag!", "Ciao!", "Привет!", "नमस्ते!", "你好!", "こんにちは!", "안녕하세요!"] * 5
    target_language = "en"  # Translate all texts to English

    responses = asyncio.run(process_requests(texts, target_language))

    for response in responses:
        print(response)

if __name__ == "__main__":
    main()
