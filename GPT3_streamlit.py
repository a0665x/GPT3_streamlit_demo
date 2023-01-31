import openai as ai
import json
from utils.GPT_moduls import GPT3_start_up , save_QA_append
import streamlit as st
# import streamlit_authenticator as stauth
from pygame import mixer
import tempfile
from gtts import gTTS
import time
def say(text, filename=None):
    with tempfile.NamedTemporaryFile(delete=True) as temp:
        tts = gTTS(text, lang='zh',slow=False) # en/zh
        if filename is None:
            filename = "{}.mp3".format(temp.name)
        tts.save(filename)
        mixer.init()
        mixer.music.load(filename)
        mixer.music.play()
        while mixer.music.get_busy() == True:
            continue
        mixer.quit()

from streamlit_chat import message  # pip install streamlit-chat
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal #pip install typing_extensions

st.title('GPT3 Chat platform')
ApiKey = st.text_input('keyin your API KEY form OpenAi')

Inquiry_Type = st.selectbox('please select your Inquiry Type:',['Hotel Information' , 'Hotel Route' , 'Hotel Price'])
st.write(f"Then let's start talking about '{Inquiry_Type}'")
st.write("\nEnter the questions to openai (to quit type \"stop\")")

Inquiry_Type_txt ='w_hotel_main.txt' if Inquiry_Type=='Hotel Information' else 'w_hotel_route.txt' if Inquiry_Type=='Hotel Route'  else 'w_hotel-room_price.txt'
GPT = GPT3_start_up(API_KEY=ApiKey,Azure_Mode=True)
start_chat_log = GPT.crerat_standard_chart_log(script_path='./Script_data/w_hotel/'+Inquiry_Type_txt,
                                               test_mode=(False,
                                                         {'QA_path': './Script_data/w_hotel/addition/Question_append.json'}))

col1, col2, col3 = st.columns(3)

if Inquiry_Type == 'Hotel Information':
    col2.image("https://img.bigfang.tw/2017/09/1504414572-34d60534293f8e2973da155643a99866.jpg", use_column_width=True)
elif Inquiry_Type =='Hotel Route':
    col2.image('https://pic.pimg.tw/gj94bunbun1021/1430230315-26900053_m.jpg',use_column_width=True)
elif Inquiry_Type == 'Hotel Price':
    col2.image('https://paolointeriors.co.uk/wp-content/uploads/2018/02/Percpetion-bar-W-Hotel04-paolo.interiors.jpg',use_column_width=True)
prev_question = ''
question = st.text_input('User Question:')
st.write('<i class="fa fa-paper-plane">', unsafe_allow_html=True)
m = st.markdown("""
div.stButton > button:<i class="fa fa-paper-plane"></i>
""", unsafe_allow_html=True)
if st.button('send') and question!=prev_question:
    t1 = time.time()
    AI_response = GPT.chat(question, start_chat_log)
    t2 = time.time()
    message(question, is_user=True)
    message(AI_response)
    say(AI_response)
    t3 = time.time()
    prev_question = question
    st.write(f'GPT3 spend {round(t2-t1,2)} sec in inference')
    st.write(f'speech spend {round(t3 - t2, 2)} sec to say')



# global AI_response , question
