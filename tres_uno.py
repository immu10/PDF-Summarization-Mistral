
import tres
import streamlit as st

import base64
import ollama


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