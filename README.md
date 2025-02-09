# 🌍 Multilingual Translation API with M2M100

This project provides an **async translation API** using `M2M100` from Hugging Face.This project is an asynchronous batch translation tool that translates English text into 100+ languages using Hugging Face's M2M100 model. The script, translate_async.py, leverages asyncio and aiohttp to handle 60 parallel translation requests, making it fast and efficient.


## 📌 Features
✅ Detects **source language**  
✅ Translates **to 100+ languages**  
✅ Uses **`asyncio` & `aiohttp`** for speed  
✅ Batch processing of **60 parallel requests**
✅ Uses Hugging Face’s M2M100 model for accurate translation

## Outlook of tool 
![Batch Translation Web App](/workspaces/M2M100_Translation_Script/asset/Screenshot 2025-02-09 at 3.21.12 PM.png)

## 🔹 How It Works
User provides a list of up to 60 English phrases.
Each phrase is translated asynchronously using the M2M100 model.
Translations are returned in JSON format, with detected language, translated text, and target language.

## 🚀 Technologies Used
Hugging Face Transformers (M2M100, XLM-RoBERTa)
Python Libraries: asyncio, aiohttp, torch, sentencepiece
Streamlit Web App (Optional) for UI-based interaction
🖼️

## 📌 Future Improvements

Deploy as an API using FastAPI
Allow user-selected target languages
Integrate text-to-speech for real-time voice translation

## 🚀 How to Run
###  Install Dependencies**
 ```bash
pip install -r requirements.txt
streamlit run app.py

