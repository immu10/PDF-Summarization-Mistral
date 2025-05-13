from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

# import base64
import ollama


def file_preprocessing(file):
    loader =PyPDFLoader(file)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(pages)
    #ignore this for now
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