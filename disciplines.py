import streamlit as st
import json
import pandas as pd
import plotly.express as px
from fonctions_transverse import display_with_pagination



def show_disciplines_page(disciplines):

    st.subheader("Disciplines des jeux olympiques depuis l'ère moderne")



    df = list(disciplines.find({},{"_id":0,"discipline":1, "event":1, "sport":1, "nb_country":1,"nb_participants":1, "time_held":1}))

    df = pd.DataFrame(df)
    df.sort_values(by="time_held",ascending=False , inplace=True)


    metric1, metric2, metric3, metric4, metric5 = st.columns([2,2,2,2,2])

    metric1.markdown(
        f"""
        <div style="background-color: #eee; padding: 5px; border-radius: 10px; text-align: center; margin: 10px;">   
            <p style="margin: 0;font-size: 15px; color: #7823B9; "><i class="fa-solid fa-person-snowboarding"></i> Nombre de disciplines</p>
            <p style="font-size: 20px; font-weight: bold; margin: 2px 0; color: #7823B9;">{len(df)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


     # Initialiser la variable de session pour la page actuelle
    if "page_number6" not in st.session_state:
        st.session_state.page_number6 = 1

    if "page_number7" not in st.session_state:
        st.session_state.page_number7 = 1
    
 

    display_with_pagination(df,"page_number6")

    st.subheader("Fiche d'une discipline")

    div1,div2,div3 = st.columns([2,2,2])
    selected_discipline= div1.selectbox("Choisissez une discipline :", sorted(df["discipline"].tolist()))

    # Affichage des détails
    if selected_discipline:
        discipline_json=list(disciplines.find({"discipline":selected_discipline},{"_id":0,"discipline":1, "event":1, "sport":1, "nb_country":1,"nb_participants":1, "time_held":1, "medals_by_country":1, "medals_by_athlete":1}))


        sub1,sub2 = st.columns([0.5,11.5])
      
        sub1.image("images/velo.png", width=50)
       
        sub2.markdown("""
            <div>
                <p style="font-size:0.6cm;">
                    Informations générales
                </p>    
            </div>       
        """, unsafe_allow_html=True)

        st.write(f"Discipline : {discipline_json[0].get("discipline")}")
        st.write(f"Sport : {discipline_json[0].get("sport")}")
        st.write(f"Nombre d'éditions : {discipline_json[0].get("time_held")}")
        st.write(f"Nombre de pays : {discipline_json[0].get("nb_countries")}")
        st.write(f"Nombre de participants : {discipline_json[0].get("nb_participants")}")

        sub1,sub2 = st.columns([0.5,11.5])
        sub1.image("images/torche.png", width=50)
        
        sub2.markdown("""
            <div>
                <p style="font-size:0.6cm;">
                    Classement des médailles par pays
                </p>    
            </div>       
        """, unsafe_allow_html=True)
        if discipline_json[0]["medals_by_country"] :
            medals_by_country= pd.DataFrame(discipline_json[0]["medals_by_country"])[["country","Gold","Silver","Bronze","total"]].sort_values(by=["Gold","Silver","Bronze"], ascending=[False, False,False])

            display_with_pagination(medals_by_country,"page_number7")


        sub1,sub2 = st.columns([0.5,11.5])
        sub1.image("images/velo.png", width=50)
        
        sub2.markdown("""
            <div>
                <p style="font-size:0.6cm;">
                    Top 10 athlètes de la discipline
                </p>    
            </div>       
        """, unsafe_allow_html=True)
        if discipline_json[0]["medals_by_athlete"] :

            medals_by_athlete= pd.DataFrame(discipline_json[0]["medals_by_athlete"])[["name","Gold","Silver","Bronze","total"]].sort_values(by=["Gold","Silver","Bronze"], ascending=[False, False,False])

            st.dataframe(medals_by_athlete, use_container_width=True, hide_index=True)


       

      
     





   

      
     
