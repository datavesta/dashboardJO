import streamlit as st
import json
import pandas as pd
import plotly.express as px



def show_accueil_page():
    start,col1,col2,end = st.columns([3.5,1,5,3.5])
    col1.image("images/jeux-olympiques.png", width=200)
    col2.subheader("Bienvenue sur le dashboard des JO")
    col1,col2 = st.columns(2)
    col1.image("images/jo.jpg")
    col2.image("images/jo3.jpg")
