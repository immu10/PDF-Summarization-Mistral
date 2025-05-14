from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader
from docx import Document
from PyDictionary import PyDictionary #didnt work
from gtts import gTTS
from nltk.corpus import wordnet
import docx2txt  # For .doc files
import ollama
import pyttsx3


def generate_tts(text, filename="output.mp3"):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)  # Words per minute
    engine.setProperty('volume', 1.0)  # Volume: 0.0 to 1.0

    # Save to file
    engine.save_to_file(text, filename)
    engine.runAndWait()

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

    elif filetype == 'txt':
        with open(file, 'r', encoding='utf-8') as f:
            full_text = f.read()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = len, chunk_overlap=olap)
        texts = text_splitter.create_documents([full_text])
        return texts

    else:
        raise ValueError("Unsupported file type")
dictionary = PyDictionary()

def explain_with_wordnet(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return "Sorry, no meaning found. This function only works with singular word look ups no phrases. Kindly use the other one"

    explanation = ""
    for i, syn in enumerate(synsets[:2]):  # Limit to top 2 meanings
        definition = syn.definition()
        examples = syn.examples()
        explanation += f"{i+1}. {definition}\n"
        if examples:
            explanation += f"   e.g., {examples[0]}\n"

    return explanation.strip()
    
def explain_text(text): # the definitions etc
    prompt = f"Explain the following word or sentence in very simple terms and concisely: '{text}'"
    response = ollama.generate(
        model='mistral',
        prompt=prompt,
        options={
            'temperature': 0.5,
            'max_tokens': 300,
            'top_p': 0.8
        }
    )
    return response['response']

def llm_pipeline(filepath,msg,filetype,len):
    chunk_size = int(len*1000)
    chunk_overlap=int(len*100)
    max_tokens = int((len-1)*250)
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