import streamlit as st
import pandas as pd
import json
from pymongo import MongoClient
from editions import show_editions_page
from athletes import show_athletes_page
from disciplines import show_disciplines_page
from accueil import show_accueil_page

client = MongoClient("localhost", 27017)

database = client["sportsdb"]

athletes = database["athletes"]
disciplines = database["disciplines"]
editions = database["editions"]



st.set_page_config(
        page_title="Jeux Olympiques",
        page_icon="trophy",
        layout="wide",
    )
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)


# Supprimer l’espace du haut
st.markdown("""
    <style>
       
        header {visibility: hidden;} 
        div.block-container {
            padding-top: 0px  !important;
        }
        .stColumn{
            margin: auto;
            }
    </style>
""", unsafe_allow_html=True)


# Titre de l'application
#st.title("Application JO - Résultats et Synthèses")

# Création des onglets
tab1, tab2, tab3, tab4 = st.tabs(["Accueil", "Éditions des JO", "Résultats des Athlètes", "Synthèse des Disciplines"])

with tab1:
    show_accueil_page()

with tab2:
    show_editions_page(editions)
    

with tab3:
    show_athletes_page(athletes)

with tab4:
    show_disciplines_page(disciplines)


 