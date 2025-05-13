
import tres
import streamlit as st

import base64
import os

@st.cache_data

def displayPDF(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    #pdf to html
    pdf_display = f'<iframe src = "data:application/pdf;base64,{base64_pdf}" width="100%" height = "600" type = "application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def get_filetype(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.pdf':
        return 'pdf'
    elif ext == '.docx':
        return 'docx'
    elif ext == '.doc':
        return 'doc'
    elif ext == '.txt':
        return 'txt'
    else:
        return None
    

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

   
    len = st.slider(
        "length of summary", 
        min_value=0.1, 
        max_value=2.0, 
        value=1.0, 
        step=0.1
    )
    

    uploaded_file = st.file_uploader("Upload your PDF file", type=['pdf','doc','docx','txt'])
    if uploaded_file is not None:
        
        filetype = get_filetype(uploaded_file.name)
        
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
                if filetype:
                    summary = tres.llm_pipeline(filepath, st.session_state.captured_text,filetype,len)
                else:
                    st.error("Unsupported file type")
                # st.info(st.session_state.captured_text) for debugging
                tres.generate_tts(summary)
                if os.path.exists("output.mp3"):
                    with open("output.mp3", "rb") as audio_file:
                       st.audio(audio_file.read(), format="audio/mp3")
                
                st.success(summary)
                
if __name__ == "__main__":
    main()