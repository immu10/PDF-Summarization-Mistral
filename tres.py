from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader
from docx import Document
import docx2txt  # For .doc files

from gTTS import gTTS
import os
import ollama

def generate_tts(text, filename="output.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename
<<<<<<< HEAD
=======

>>>>>>> cc392390de39e1b3a8201c88f2841132b7a122b9

def file_preprocessing(file, filetype):
    if filetype == 'pdf':
        loader = PyPDFLoader(file)
        pages = loader.load_and_split()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(pages)
        return texts

    elif filetype == 'docx':
        doc = Document(file)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.create_documents([full_text])
        return texts

    elif filetype == 'doc':
        full_text = docx2txt.process(file)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.create_documents([full_text])
        return texts

    elif filetype == 'txt':
        with open(file, 'r', encoding='utf-8') as f:
            full_text = f.read()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.create_documents([full_text])
        return texts

    else:
        raise ValueError("Unsupported file type")


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