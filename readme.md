# 🧠 Document Summarization App with LLaMA 2

This is a lightweight Streamlit-based app (`tres.py`) that summarizes PDF documents using a locally running LLaMA 2 model through the Ollama backend.

## 🚀 Features
- Accepts PDF file uploads and summarizes their content.
- Uses LangChain for document loading and text splitting.
- Powered by LLaMA 2 — we initially aimed for LLaMA 3.3, but it exceeded local hardware limits (33.7 GiB RAM required vs. 19.9 GiB available).
- Simple text prompt input included via a textbox.
- The summarization output is displayed alongside the uploaded document.

## 📄 Input Format
Currently, the app **only accepts PDFs**.  
We haven’t added support for other input formats — frankly, because we didn’t feel like it.  
But hey, if you want to, it's as easy as copying from the [LangChain documentation](https://docs.langchain.com/).

## 📂 Main File
Run the app using:

```bash
streamlit run tres.py
