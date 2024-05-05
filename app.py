import os
import sys
import datetime
import openai
import dotenv
import streamlit as st
import numpy as np
import time

from pathlib import Path
from audio_recorder_streamlit import audio_recorder
import pandas as pd
import json

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Import OpenAI and dotenv for API key management
import dotenv
from openai import OpenAI
from Chat.chat import *

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai.api_key)

def load_json_to_df(file_path):
    # Carga el archivo JSON
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Transforma el diccionario en un DataFrame
    df = pd.DataFrame(list(data.items()), columns=['Product', 'Quantity'])
    return df

def save_audio_file(audio_bytes, file_extension):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"
    with open(file_name, "wb") as f:
        f.write(audio_bytes)
    return file_name

def transcribe(audio_file):
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcript

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = transcribe(audio_file)
    return transcript.text

def text_to_speech(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path


def main():
    st.title("Lister of products")

    tab1, tab2 = st.tabs(["Record Audio", "Upload Audio"])

    with tab1:
        audio_bytes = audio_recorder()
        if audio_bytes:
            saved_file = save_audio_file(audio_bytes, "mp3")

    with tab2:
        audio_file = st.file_uploader("Upload Audio", type=["mp3", "mp4", "wav", "m4a"])
        if audio_file:
            file_extension = audio_file.type.split('/')[1]
            saved_file = save_audio_file(audio_file.read(), file_extension)

    audio_file_path = max([f for f in os.listdir(".") if f.startswith("audio")], key=os.path.getctime)
    transcript_text = transcribe_audio(audio_file_path)
    
    chatbot_response, is_planning = chatbot_assistant(transcript_text, tools)
    st.header("Chatbot Response")
    
    speech_file_path = text_to_speech(chatbot_response)
    audio_file = open(speech_file_path, "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    df = load_json_to_df("product_list.json")
    names_df = pd.read_csv('./data_final.csv')
    names_df['id'] = names_df['id'].astype(str)

    # Fusionar los DataFrames utilizando el identificador como clave de fusión
    merged_df = pd.merge(df, names_df[['id', 'name']], how='left', left_on='Product', right_on='id')

    # Eliminar la columna 'id' redundante
    merged_df.drop('id', axis=1, inplace=True)
    st.dataframe(merged_df)

    if is_planning:
        st.image('simulacion_incendio.gif', caption="Planning process visualization")
        
if __name__ == "__main__":
    working_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(working_dir)
    main()
