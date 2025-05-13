import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

import base64
import ollama


def file_preprocessing(file):
    loader =PyPDFLoader(file)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(pages)

    # final_texts= "" 
    # for  text in texts:
    #    # print(text)
    #     final_texts = final_texts +text.page_content
    return texts


def llm_pipeline(filepath,msg,temperature):
    input_text = file_preprocessing(filepath)
    summaries = []
    for chunk in input_text:
        prompt =f"\n{msg}\n{chunk.page_content}"
        response = ollama.generate(
            model='mistral',
            prompt=prompt,
            options={
                'temperature':temperature,
                'max_tokens': 500,
                'top_p': 0.5
            }
        )
        summaries.append(response['response'])

    return "\n\n".join(summaries)

@st.cache_data

def displayPDF(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    #pdf to html
    pdf_display = f'<iframe src = "data:application/pdf;base64,{base64_pdf}" width="100%" height = "600" type = "application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    st.title("Document Summarization App using Language Model")

    # Initialize session_state if it doesn't exist
    if "captured_text" not in st.session_state:
        st.session_state.captured_text = "Summarize the attached pdf."

    # Textbox with default text
    user_input = st.text_area(
        "Enter your text below:",
        value=st.session_state.captured_text
    )

    if st.button("Submit"):
        st.session_state.captured_text = user_input
        st.success(f"Captured Text: {st.session_state.captured_text}")

    uploaded_file = st.file_uploader("Upload your PDF file", type=['pdf'])
    temperature = st.slider(
        "Set the model's creativity (temperature):", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.7, 
        step=0.1
    )

    if uploaded_file is not None:
        if st.button("Summarize"):
            col1, col2 = st.columns(2)
            filepath = "data/" + uploaded_file.name
            with open(filepath, "wb") as temp_file:
                temp_file.write(uploaded_file.read())
            with col1:
                st.info("Uploaded File")
                pdf_view = displayPDF(filepath)

            with col2:
                print(st.session_state.captured_text)
                summary = llm_pipeline(filepath, st.session_state.captured_text,temperature)
                st.info(st.session_state.captured_text)
                st.success(summary)
if __name__ == "__main__":
    main()