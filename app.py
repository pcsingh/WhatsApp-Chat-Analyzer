# Libraries Imported
import streamlit as st

import func_use_extract_data as func
import func_analysis as analysis

import pandas as pd
import re

import emoji
import collections as c

import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("WhatsApp Chat Analyzer 😃")
st.sidebar.title("Analyze:")
st.markdown("This app is use to analyze your WhatsApp Chat using the txt file.")
st.sidebar.markdown("This app is use to analyze your WhatsApp Chat using the txt file.")

filename = ("./Chat.txt")

@st.cache(persist=True)
def load_data():
    with open(filename, encoding="utf-8") as f:
        file_contents = [x.rstrip() for x in f]
    
    return pd.DataFrame(func.read_data(file_contents), columns=['Date', 'Time', 'Author', 'Message'])


data = load_data()

st.write(data)

