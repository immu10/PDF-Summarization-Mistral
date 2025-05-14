
import tres
import streamlit as st
import pypandoc
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
    
def convert_to_txt(input_path):
    try:
        output = pypandoc.convert_file(input_path, 'plain')
        return output
    except Exception as e:
        return f"Error converting file: {e}"
    
def displayTextContent(text):
    st.markdown(f"<div style='white-space: pre-wrap; font-family: monospace;'>{text}</div>", unsafe_allow_html=True)


def main():
    global explanation
    global uploaded_file 
    uploaded_file = None
    explanation = None
    spawn_da_box = False
    st.title("Document Summarization App using Language Model")

    col1, col2 = st.columns(2)

    with col1:
        if "captured_text" not in st.session_state:
            st.session_state.captured_text = "Summarize the attached pdf."

        user_input = st.text_area(
            "Enter prompt/questions:",
            value=st.session_state.captured_text,
            height=150
        )
        promptbutton = st.button("Submit")
        if promptbutton:
            st.session_state.captured_text = user_input
            # st.success(f"Captured Text: {st.session_state.captured_text}") # debugging line
        if promptbutton and uploaded_file is None:
            st.warning("Upload file first")
        # else:
        #     st.warning("File preview not supported for this format.") samething as ^

    with col2:
        st.subheader("Explain Word or Sentence")
        input_to_explain = st.text_input("Type a word or sentence:")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Explain"):
                if input_to_explain.strip():
                    explanation = tres.explain_text(input_to_explain)
                    spawn_da_box = True
                else:
                    st.warning("Please enter something to explain.")
        with col2:    
            if st.button("Lookup"):
                if input_to_explain.strip():
                    explanation = tres.explain_with_wordnet(input_to_explain.strip())
                    spawn_da_box = True
                else:
                    st.warning("Enter a word first.")
        with col3:
            if st.button("Listen"):
                if input_to_explain.strip():
                    tres.generate_tts(input_to_explain.strip(),"phrase.mp3") #the tts generation fucntion 
                    if os.path.exists("phrase.mp3"):
                        with open("phrase.mp3", "rb") as audio_file:
                            st.audio(audio_file.read(), format="audio/mp3")
                    
                else:
                    st.warning("Enter a word first.")
    if spawn_da_box:    
        st.text_area("Definition", explanation, height=150)
    len = st.slider(
        "length of summary(1.00 for better explanation :: 4.00 for summarization):", 
        min_value=1.0,  
        max_value=4.0, 
        value=2.0, 
        step=0.1,
    )
    

    uploaded_file = st.file_uploader("Upload your PDF file", type=['pdf','docx','txt'])
    if uploaded_file is not None:
        
        filetype = get_filetype(uploaded_file.name)
        
        if st.button("Summarize"):
            col1, col2 = st.columns(2)
            filepath = "data/" + uploaded_file.name
            with open(filepath, "wb") as temp_file:
                temp_file.write(uploaded_file.read())
            with col1:
                st.info("Uploaded File")
                if filetype == 'pdf':
                    displayPDF(filepath)
                elif filetype in ['doc', 'docx']:
                    text_content = convert_to_txt(filepath)
                    displayTextContent(text_content)
                elif filetype == 'txt':
                    with open(filepath, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                    displayTextContent(text_content)

            with col2:
                print(st.session_state.captured_text)
                if filetype:
                    summary = tres.llm_pipeline(filepath, st.session_state.captured_text,filetype,(len+0.1))
                else:
                    st.error("Unsupported file type")
                # st.info(st.session_state.captured_text) for debugging
                tres.generate_tts(summary) #the tts generation fucntion 
                if os.path.exists("output.mp3"):
                    with open("output.mp3", "rb") as audio_file:
                       st.audio(audio_file.read(), format="audio/mp3")
                
                st.success(summary)
                
if __name__ == "__main__":
    main()