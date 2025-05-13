from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader
from docx import Document
import docx2txt  # For .doc files

from gtts import gTTS
import os
import ollama

def generate_tts(text, filename="output.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename


def file_preprocessing(file, filetype,len,olap):
    if filetype == 'pdf':
        loader = PyPDFLoader(file)
        pages = loader.load_and_split()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=len, chunk_overlap=olap)
        texts = text_splitter.split_documents(pages)
        return texts

    elif filetype == 'docx':
        doc = Document(file)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = len, chunk_overlap=olap)
        texts = text_splitter.create_documents([full_text])
        return texts

    elif filetype == 'doc':
        full_text = docx2txt.process(file)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = len, chunk_overlap=olap)
        texts = text_splitter.create_documents([full_text])
        return texts

    elif filetype == 'txt':
        with open(file, 'r', encoding='utf-8') as f:
            full_text = f.read()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = len, chunk_overlap=olap)
        texts = text_splitter.create_documents([full_text])
        return texts

    else:
        raise ValueError("Unsupported file type")


def llm_pipeline(filepath,msg,filetype,len):
    num = len*1000
    chunk_size = int(num)
    num2= len*100
    chunk_overlap=int(num2)
    num1 = (len-1)*250
    max_tokens = int(num1)
    input_text = file_preprocessing(filepath,filetype,chunk_size,chunk_overlap)
    summaries = []
    for chunk in input_text:
        prompt =f"\n{msg}\n{chunk.page_content}"
        response = ollama.generate(
            model='mistral',
            prompt=prompt,
            options={
                'temperature':0.7,
                'max_tokens': max_tokens,
                'top_p': 0.5
            }
        )
        summaries.append(response['response'])

    return "\n\n".join(summaries)