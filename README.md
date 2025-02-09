# 🌍 Multilingual Translation API with M2M100

This project provides an **async translation API** using `M2M100` from Hugging Face.

## 📌 Features
✅ Detects **source language**  
✅ Translates **to 100+ languages**  
✅ Uses **`asyncio` & `aiohttp`** for speed  
✅ Batch processing of **60 parallel requests**

## 🖼️ Output Screenshot
![Translation Output][/workspaces/M2M100_Translation_Script/asset]

## 📜 Script Description: `translate_async.py`
`translate_async.py` is the **main script** for:
- Detecting **input text language**
- Translating text **to a random language**
- Using `aiohttp` to process **60 parallel translations**
- Running translations via Hugging Face's **M2M100 model**

## 🚀 How to Run
###  Install Dependencies**
 ```bash
pip install -r requirements.txt
streamlit run app.py

