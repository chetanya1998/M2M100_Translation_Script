import streamlit as st
import asyncio
import aiohttp
import random
import pandas as pd
from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration

# --- Load Translation Model ---
m2m_tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
m2m_model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")

# --- Supported Languages for Translation ---
language_options = {
    "Afrikaans": "af", "Arabic": "ar", "French": "fr", "German": "de", "Spanish": "es",
    "Chinese": "zh", "Hindi": "hi", "Japanese": "ja", "Russian": "ru", "Portuguese": "pt",
    "Dutch": "nl", "Italian": "it", "Turkish": "tr", "Korean": "ko", "Polish": "pl",
    "Vietnamese": "vi", "Thai": "th", "Greek": "el", "Hebrew": "he", "Indonesian": "id"
}
lang_keys = list(language_options.keys())  # List of available languages

# --- Translation Function ---
async def translate_text(text, src_lang="en", tgt_lang=None):
    """Translates text from English to a target language."""
    if not tgt_lang:
        tgt_lang = random.choice(list(language_options.values()))  # Select random language

    m2m_tokenizer.src_lang = src_lang
    encoded = m2m_tokenizer(text, return_tensors="pt")
    generated_tokens = m2m_model.generate(
        **encoded,
        forced_bos_token_id=m2m_tokenizer.get_lang_id(tgt_lang)
    )
    translated_text = m2m_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    
    return {"original": text, "translated": translated_text, "target_lang": tgt_lang}

async def process_requests(text_list):
    """Handles 60 parallel translation requests asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [translate_text(text) for text in text_list]
        results = await asyncio.gather(*tasks)
    return results

# --- Streamlit UI ---
st.title("🌍 Batch Translation Web App")
st.write("Enter up to **60 English sentences**, and they will be translated into random languages.")

# Input text area
input_texts = st.text_area("Enter multiple sentences (one per line, max 60):", height=200)

if st.button("Translate"):
    text_list = input_texts.strip().split("\n")[:60]  # Limit to 60 sentences

    if len(text_list) == 0:
        st.warning("Please enter at least one sentence.")
    else:
        st.write(f"📤 Sending **{len(text_list)} requests** for translation...")

        responses = asyncio.run(process_requests(text_list))

        # Convert responses to DataFrame
        df = pd.DataFrame(responses)
        df["target_lang"] = df["target_lang"].map({v: k for k, v in language_options.items()})  # Convert codes to names

        # Display results in table
        st.dataframe(df)

        # Provide CSV download option
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Translations", csv, "translations.csv", "text/csv")
