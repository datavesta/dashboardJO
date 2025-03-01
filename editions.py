import streamlit as st
import json
import pandas as pd
import plotly.express as px
from fonctions_transverse import display_with_pagination



def show_editions_page(editions):
  
    st.subheader("Éditions des Jeux Olympiques depuis l'ère moderne")

    editions_selections = list(editions.find({},{"_id":0,"edition":1, "nb_participants":1, "year":1, "nb_participants_by_sex":1,"nb_medals":1, "nb_countries":1, "nb_disciplines":1, "nb_sports":1, "type":1}).sort({'year':1}))

    total_editions = len(editions_selections)

    total_summer_editions = editions.count_documents({"type":"Summer"})
    total_winter_editions = editions.count_documents({"type":"Winter"})

     # Convertir en DataFrame Pandas
    df = pd.DataFrame(editions_selections)

    # Séparer les colonnes Female et Male
    df["Female"] = df["nb_participants_by_sex"].apply(lambda x: x.get("Female", 0)).astype(int)
    df["Male"] = df["nb_participants_by_sex"].apply(lambda x: x.get("Male", 0)).astype(int)
    df["year"] = df["year"].astype(int) 
    df.drop(columns="nb_participants_by_sex", inplace=True)
    # Renommer les colonnes
    df.rename(columns={"edition":"Nom", "nb_participants": "Participants", "Female": "Femmes", "Male": "Hommes", "nb_countries": "Pays", "nb_disciplines": "Disciplines", "nb_sports": "Sports", "year":"Année", "nb_medals":"Médailles"}, inplace=True)


    metric1, metric2, metric3, metric4, metric5 = st.columns([2,2,2,2,2])

    metric1.markdown(
        f"""
        <div style="background-color: #eee; padding: 5px; border-radius: 10px; text-align: center;">   
            <p style="margin: 0;font-size: 15px; color: #7823B9; "><i class="fa-solid fa-person-snowboarding"></i> Nombre d'éditions</p>
            <p style="font-size: 20px; font-weight: bold; margin: 2px 0; color: #7823B9;">{total_editions}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    metric2.markdown(
        f"""
        <div style="background-color: #eee; padding: 5px; border-radius: 10px; text-align: center;">   
            <p style="margin: 0;font-size: 15px; color: #7823B9; "><i class="fa-regular fa-snowflake"></i> Jeux d'hiver</p>
            <p style="font-size: 20px; font-weight: bold; margin: 2px 0; color: #7823B9;">{total_winter_editions}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    metric3.markdown(
        f"""
        <div style="background-color: #eee; padding: 5px; border-radius: 10px; text-align: center;">   
            <p style="margin: 0;font-size: 15px; color: #7823B9; "><i class="fa-regular fa-sun"></i> Jeux d'Eté</p>
            <p style="font-size: 20px; font-weight: bold; margin: 2px 0; color: #7823B9;">{total_summer_editions}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
   
    st.markdown(
        f"""
        <div style="display: flex; justify-content: right; align-items: right; height: 50px;">
            <h2 style="margin: 0; font-size: 15px; font-weight: normal;">Données à l'année {df["Année"].max()}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
   

    # Initialiser la variable de session pour la page actuelle
    if "page_number" not in st.session_state:
        st.session_state.page_number = 1

    # Initialiser la variable de session pour la page actuelle
    if "page_number2" not in st.session_state:
        st.session_state.page_number2 = 1

    # Initialiser la variable de session pour la page actuelle
    if "page_number3" not in st.session_state:
        st.session_state.page_number3 = 1

    
    display_with_pagination(df,"page_number")

   
    # Evolution temporelle des jeux olympiques (Jeux d'été et Jeux d'Hiver)
    st.subheader("Evolution temporelle de métriques")

    df_sorted = df.sort_values(by="Année")

    # Sélecteur déroulant pour choisir une édition
    div1,div2,div3 = st.columns([2,2,2])
    selected_metric = div1.selectbox("Choisissez une métrique :", list(df[["Participants", "Femmes","Hommes","Pays", "Sports", "Disciplines",]].columns))
    selected_type = div2.selectbox("Choisissez un type de jeux :", ["Summer","Winter"])
    # Création du graphique avec Plotly
 
    if selected_metric and selected_type:
        filtered_df = df[df["type"]==selected_type]
        fig = px.line(filtered_df, x="Année", y=[selected_metric], 
            markers=True,  # Ajouter des points sur les lignes
            labels={"Année": "Année", "value": "Nombre", "variable": "Métrique"},
            title="Évolution par année",
            color_discrete_sequence=['#7823b9']
        )
        

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Exploration d'une édition")
    
    # Sélecteur déroulant pour choisir une édition
    div1,div2,div3 = st.columns([2,2,2])
    selected_edition = div1.selectbox("Choisissez une édition :", df["Nom"].tolist())

    # Affichage des détails
    if selected_edition:
        edition_json=list(editions.find({"edition":selected_edition},{"_id":0,"medals_by_sport":1, "medals_by_athlete":1, "medals_by_country":1}))
        pipeline = [{"$match": {"edition":selected_edition}}, {"$unwind":"$results"}, {"$group":{"_id":"$_id", "sports": {"$addToSet":"$results.sport"}}}]
        sports = list(editions.aggregate(pipeline))
        sub1,sub2 = st.columns([0.5,11.5])
        sub1.image("images/torche.png", width=50)
        
        sub2.markdown("""
            <div>
                <p style="font-size:0.6cm;">
                    Sports présents
                </p>    
            </div>       
        """, unsafe_allow_html=True)
        st.write(", ".join(sports[0]['sports']))

        sub1,sub2 = st.columns([0.5,11.5])
        sub1.image("images/gagnant.png", width=50)
        
        sub2.markdown("""
            <div>
                <p style="font-size:0.6cm;">
                    Classement des pays par médailles
                </p>    
            </div>       
        """, unsafe_allow_html=True)

        medals_by_country = pd.DataFrame(edition_json[0]["medals_by_country"])
        medals_by_country =medals_by_country[["country","Gold","Silver","Bronze","total"]]
        medals_by_country = medals_by_country.sort_values(by=["Gold", "Silver","Bronze"], ascending=[False, False, False])
        
        display_with_pagination(medals_by_country,"page_number2")


        sub1,sub2 = st.columns([0.5,11.5])
        sub1.image("images/medaille-dor.png", width=50)
        
        sub2.markdown("""
            <div>
                <p style="font-size:0.6cm;">
                    Classement des athlètes par médailles
                </p>    
            </div>       
        """, unsafe_allow_html=True)
        medals_by_athlete = pd.DataFrame(edition_json[0]["medals_by_athlete"])
        medals_by_athlete =medals_by_athlete[["name","country","Gold","Silver","Bronze","total"]]
        medals_by_athlete = medals_by_athlete.sort_values(by=["Gold", "Silver","Bronze"], ascending=[False, False, False])
        display_with_pagination(medals_by_athlete,"page_number3")


      
     
