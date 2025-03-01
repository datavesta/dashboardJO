import streamlit as st
import json
import pandas as pd
import plotly.express as px
from fonctions_transverse import display_with_pagination



def show_athletes_page(athletes):

    st.subheader("Résultats des athlètes aux Jeux olympiques depuis l'ère moderne")

    pipeline = [
        {
            "$group": {
                "_id": None,
                "countries":{
                    "$addToSet":"$country"
                }
            }
        },
        {
            "$project":{"countries": 1, "_id":0}
        }
    ]

    countries = sorted(list(athletes.aggregate(pipeline))[0]["countries"])

    df = list(athletes.find({},{"_id":0,"name":1, "country":1, "born":1, "sex":1, "nb_medals":1,"nb_sports":1, "nb_disciplines":1, "nb_editions":1}))

    df = pd.DataFrame(df)
    df.sort_values(by="nb_medals",ascending=False , inplace=True)

    # Filtrer les athletes par pays, sexe
    div1,div2,div3 = st.columns([2,2,2])
    selected_country = div1.selectbox("Choisissez un pays :", ["All"]+countries)
    selected_sex = div2.selectbox("Choisissez un  sexe :", ["All","Male","Female"])

    match (selected_country, selected_sex):
        case ("All", "All"):
            df_filtered = df
        case ("All",selected_sex) if selected_sex !="All":
            df_filtered = df[df["sex"]==selected_sex]
        case (selected_country, "All") if selected_country !="All":
            df_filtered = df[df["country"]==selected_country]
        case _:
            df_filtered = df[(df["country"]==selected_country) & (df["sex"]==selected_sex)]



    metric1, metric2, metric3, metric4, metric5 = st.columns([2,2,2,2,2])

    metric1.markdown(
        f"""
        <div style="background-color: #eee; padding: 5px; border-radius: 10px; text-align: center; margin: 10px;">   
            <p style="margin: 0;font-size: 15px; color: #7823B9; "><i class="fa-solid fa-person-snowboarding"></i> Nombre d'athlètes</p>
            <p style="font-size: 20px; font-weight: bold; margin: 2px 0; color: #7823B9;">{len(df_filtered)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


     # Initialiser la variable de session pour la page actuelle
    if "page_number4" not in st.session_state:
        st.session_state.page_number4 = 1
    
    if "page_number5" not in st.session_state:
        st.session_state.page_number5 = 1



    display_with_pagination(df_filtered,"page_number4")

    st.subheader("Fiche d'un athlète")

    div1,div2,div3 = st.columns([2,2,2])
    selected_name= div1.selectbox("Choisissez un athlète :", df["name"].tolist())

    # Affichage des détails
    if selected_name:
        athlete_json=list(athletes.find({"name":selected_name},{"_id":0,"name":1, "country":1, "born":1, "sex":1, "nb_medals":1,"nb_sports":1, "nb_disciplines":1, "nb_editions":1, "nb_medals_by_type":1, "results":1}))
        pipeline = [{"$match": {"name":selected_name}}, {"$unwind":"$results"}, {"$group":{"_id":"$_id", "sports": {"$addToSet":"$results.sport"}, "disciplines":{"$addToSet":"$results.discipline"}, "editions":{"$addToSet":"$results.edition"}}}]
        details = list(athletes.aggregate(pipeline))

        sub1,sub2 = st.columns([0.5,11.5])
        if athlete_json[0].get("sex") == "Female" :
            sub1.image("images/femme.png", width=50)
        else:
            sub1.image("images/homme.png", width=50)

        
        sub2.markdown("""
            <div>
                <p style="font-size:0.6cm;">
                    Informations personnelles
                </p>    
            </div>       
        """, unsafe_allow_html=True)

        st.write(f"Nom : {athlete_json[0].get("name")}")
        st.write(f"Date de naissance : {athlete_json[0].get("born")}")
        st.write(f"Pays : {athlete_json[0].get("country")}")
        st.write(f"Taille : {athlete_json[0].get("height", "Pas communiqué")}")
        st.write(f"Poids : {athlete_json[0].get("weight","Pas communiqué")}")

        sub1,sub2 = st.columns([0.5,11.5])
        sub1.image("images/torche.png", width=50)
        
        sub2.markdown("""
            <div>
                <p style="font-size:0.6cm;">
                    Participation aux Jeux olympiques
                </p>    
            </div>       
        """, unsafe_allow_html=True)
        st.write(", ".join(details[0]['editions']))
        st.write(f"Nombre de participations au total: {len(details[0]['editions'])}")

        sub1,sub2 = st.columns([0.5,11.5])
        sub1.image("images/velo.png", width=50)
        
        sub2.markdown("""
            <div>
                <p style="font-size:0.6cm;">
                    Sports
                </p>    
            </div>       
        """, unsafe_allow_html=True)

        st.write(", ".join(details[0]['sports']))
        st.write(f"Nombre de sports au total: {len(details[0]['sports'])}")

        sub1,sub2 = st.columns([0.5,11.5])
        sub1.image("images/velo.png", width=50)
        
        sub2.markdown("""
            <div>
                <p style="font-size:0.6cm;">
                    Epreuves
                </p>    
            </div>       
        """, unsafe_allow_html=True)

        st.write(", ".join(details[0]['disciplines']))
        st.write(f"Nombre d'épreuves au total: {len(details[0]['disciplines'])}")

        sub1,sub2 = st.columns([0.5,11.5])
        sub1.image("images/podium.png", width=50)
        
        sub2.markdown("""
            <div>
                <p style="font-size:0.6cm;">
                    Palmarès
                </p>    
            </div>       
        """, unsafe_allow_html=True)

        st.write(f"🥇 Gold : {athlete_json[0]["nb_medals_by_type"].get("Gold", 0)}")
        st.write(f"🥈 Silver : {athlete_json[0]["nb_medals_by_type"].get("Silver", 0)}")
        st.write(f"🥉 Bronze : {athlete_json[0]["nb_medals_by_type"].get("Bronze",0)}")

        sub1,sub2 = st.columns([0.5,11.5])
        sub1.image("images/gagnant.png")
        
        sub2.markdown("""
            <div>
                <p style="font-size:0.6cm;">
                    Historique complet
                </p>    
            </div>       
        """, unsafe_allow_html=True)

        results_by_year = pd.DataFrame(athlete_json[0]["results"])
        results_by_year=results_by_year[["year","edition","sport","discipline","medal","pos"]].sort_values(by="year")
        st.dataframe(results_by_year,hide_index=True, use_container_width=True)
       



       

      
     





   

      
     
