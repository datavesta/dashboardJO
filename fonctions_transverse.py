import streamlit as st
import pandas as pd
import plotly.express as px

def display_with_pagination(df,page_key):
    items_per_page =10
     # Calcul des indices de la page actuelle
    start_idx = (st.session_state[page_key] - 1) * items_per_page
    end_idx = start_idx + items_per_page

    # Afficher les données paginées
  
    st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True,hide_index=True)
    #st.dataframe(df,use_container_width=True)
    
    # Créer une colonne pour aligner les boutons
  
    col1, col_middle, col2,col_empty = st.columns([1.2,0.5,1,8])

    with col_middle:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; height: 50px;">
                <h2 style="margin: 0; font-size: 10px; font-weight: normal;">Page {st.session_state[page_key]}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
    # Bouton "Précédent"
    if col1.button("Précédent ",key="bouton_1"+page_key) and st.session_state[page_key] > 1:
        st.session_state[page_key] -= 1

    # Bouton "Suivant"
    if col2.button("Suivant ",key="bouton_2"+page_key) and st.session_state[page_key] < len(df) // items_per_page + 1:
        st.session_state[page_key] += 1


