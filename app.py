import streamlit as st
import requests
import json
def community_page(alg_sel_ft, alg_sel_urg, alg_sel_sent):
    # Mantener el logo original
    st.logo("assets/Logos_NTT_Mediolanum.png", size="large")
    
    # Lista de tipologías
    list_typo = ["Pendiente Determinación", "Cancelación de cuentas", "Mi remuneración", 'CONSULTA: no pertinente', "Exclusivo para Expertos Protección", "Eventos", "Sugerencias", "Comision liquidacion", "CRM", "Herencias", "Mediolanum a tu medida", "Otros", "Alta nuevo cliente", "MIFID-PPA-ASG", "Crédito/Préstamo", "MIF / Fondos nacionales", "MIL", 'Llamada Entrante Número Rosso']
    list_typo.sort()

    # Layout de columnas
    typo_col, fb_col, vinc_col = st.columns([2, 1, 1])

    # Campos de entrada
    with typo_col:
        typology = st.selectbox("Tipología", list_typo)
    
    with fb_col:
        family_banker = st.selectbox("Family Banker", [None, 'Private', 'Wealth'])
        family_banker = 'W' if family_banker == 'Wealth' else 'P' if family_banker == 'Private' else 'No selected'
    
    with vinc_col:
        vinculacion = st.selectbox("Vinculación cliente", [None, 1, 2, 3, 4, 5])
    pregunta = st.text_area("Pregunta")

    if st.button("Clasificar"):
        alg_selected = { 'fasttrack': alg_sel_ft, 'urgency': alg_sel_urg, 'sentiment': alg_sel_sent }
        respuesta = classify(pregunta, typology, family_banker, vinculacion, alg_selected)
        
        if isinstance(respuesta, dict):
            #ft_answer = respuesta.get('FastTrack', {})
            ur_answer = respuesta.get('Urgencia', {})
            sentiment_answer = respuesta.get('Sentimiento', {})
            def key_rename(dc, kf, ki):
               new_dict = dict({kf:dc[ki]}, **dc)
               del new_dict[ki]
               return new_dict
            #ft_answer = key_rename(ft_answer, 'Clasificación', 'Clasificacion')
            ur_answer = key_rename(ur_answer, 'Clasificación', 'Clasificacion')
            sentiment_answer = key_rename(sentiment_answer, 'Puntuación', 'Puntuacion')
            
            # Mostrar resultados con el mismo estilo visual
            # st.markdown('<span style="font-size: 24px;">Complejidad</span>', unsafe_allow_html=True)
            # for item in ft_answer:
            #     col1, col2 = st.columns([1, 4])
            #     with col1:
            #         st.write(f'**{item}**')
            #     with col2:
            #         if ft_answer[item] == 'FastTrack':
            #             st.markdown(f'<span style="color: Green;">{ft_answer[item]}</span>', unsafe_allow_html=True)
            #         else:
            #             st.write(ft_answer[item])
                        
            st.divider()
            st.markdown('<span style="font-size: 24px;">Urgencia</span>', unsafe_allow_html=True)
            if ur_answer:
                for item in ur_answer:
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.write(f'**{item}**')
                    with col2:
                        if ur_answer[item] == 'Urgente':
                            st.markdown(f'<span style="color: Red;">{ur_answer[item]}</span>', unsafe_allow_html=True)
                        else:
                            st.write(ur_answer[item])
            else:
                st.write("No urgency classification available.")
                
            st.divider()
            st.markdown('<span style="font-size: 24px;">Sentimiento</span>', unsafe_allow_html=True)
            for item in sentiment_answer:
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.write(f'**{item}**')
                with col2:
                    if sentiment_answer[item] in [3, '3']:
                        st.markdown(f'<span style="color: Red; font-size: 16px;">{sentiment_answer[item]}</span>', unsafe_allow_html=True)
                    elif sentiment_answer[item] in [2, '2']:
                        st.markdown(f'<span style="color: Yellow; font-size: 16px;">{sentiment_answer[item]}</span>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<span style="color: Green; font-size: 16px;">{sentiment_answer[item]}</span>', unsafe_allow_html=True)
        else:
            st.error(respuesta)

def main():

    # Crear la barra lateral de navegación
    with st.sidebar:
         st.write("**Algoritmos seleccionados**")
    # st.sidebar.markdown("**FastTrack**")
    # alg_sel_ft = {
    #     'typos_box': st.sidebar.checkbox("Tipologías predefinidas", value = True),
    #     'len_box': st.sidebar.checkbox("Longitud de la pregunta", value = True),
    #     'clustering_box': st.sidebar.checkbox("Clustering", value = True),
    #     'simil_box': st.sidebar.checkbox("Similitud", value = True),
    #     'llm_box': st.sidebar.checkbox("FastTrack LLM", value = True)
    # }
    st.sidebar.markdown("**Urgencia**")
    alg_sel_urg = {
        'predef_box': st.sidebar.checkbox("Predefinido", value = True),
        'import_box': st.sidebar.checkbox("Importe", value = True),
        'fuzzy_box': st.sidebar.checkbox("Fuzzy", value = True),
        'urllm_box': st.sidebar.checkbox("Urgency LLM", value = True)
    }
    st.sidebar.markdown("**Sentimiento**")
    alg_sel_sent = {
        'sent_box': st.sidebar.checkbox("Sentimiento", value = True)
    }

    
    # Botón para seleccionar todos los algoritmos
    # if st.sidebar.button("Seleccionar todos"):
    #     for key in alg_sel_ft:
    #         st.session_state[key] = True
    #         # set values to True 
    #         alg_sel_ft[key] = True

    #     for key in alg_sel_urg:
    #         st.session_state[key] = True
    #         # set values to True
    #         alg_sel_urg[key] = True
    #     for key in alg_sel_sent:
    #         st.session_state[key] = True
    #         # set values to True
    #         alg_sel_sent[key] = True


    # Sincronizar los valores de los checkboxes con st.session_state
    # for key in alg_sel_ft:
    #     alg_sel_ft[key] = st.session_state.get(key, alg_sel_ft[key])
    for key in alg_sel_urg:
        alg_sel_urg[key] = st.session_state.get(key, alg_sel_urg[key])
    for key in alg_sel_sent:
        alg_sel_sent[key] = st.session_state.get(key, alg_sel_sent[key])

    # Mostrar mensaje si todos los algoritmos están seleccionados
    # if all(alg_sel_ft.values()) and all(alg_sel_urg.values()) and all(alg_sel_sent.values()):
    #     # all checkboxes visally marked as selected
    #     st.sidebar.markdown("**Todos los algoritmos seleccionados**<span style='color: green;'>✔️</span>", unsafe_allow_html=True)

    alg_sel_ft = {
        'typos_box': False,
        'len_box': False,
        'clustering_box': False,
        'simil_box': False,
        'llm_box': False
    }
    community_page(alg_sel_ft, alg_sel_urg, alg_sel_sent)
    # Estilos CSS para el logo
    st.markdown("""
    <style>
    div[data-testid="stSidebarHeader"] > img {
        height: 5rem;
        width: auto;
    },
    div[data-testid="stSidebarCollapsedControl"] > img {
        height: 5rem;
        width: auto;
    },
    div[data-testid="stSidebarHeader"], div[data-testid="stSidebarHeader"] > *,
    div[data-testid="collapsedControl"], div[data-testid="collapsedControl"] > * {
        display: flex;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)
        # Button for batch processing
    

def classify(pregunta, typology, family_banker, vinculacion, alg_selected):

    req = requests.get(
        'https://instanceclassifier.azurewebsites.net/api/mediolanum',
        params={'instance': pregunta,
                'typology': typology,
                'family_banker': family_banker,
                'vinculacion': vinculacion}
    )

    return json.loads(req.text)

if __name__ == "__main__":
    main()
