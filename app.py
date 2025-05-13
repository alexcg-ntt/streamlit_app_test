import streamlit as st

def community_page(alg_sel_ft, alg_sel_urg, alg_sel_sent):
    # Mantener el logo original
    #st.logo("assets\\Logos_NTT_Mediolanum.png", size="large")
    
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
                      
        st.divider()
        st.markdown('<span style="font-size: 24px;">Urgencia</span>', unsafe_allow_html=True)
        
        st.write("Aquí saldrá la urgencia")
            
        st.divider()
        st.markdown('<span style="font-size: 24px;">Sentimiento</span>', unsafe_allow_html=True)
        st.write("Aquí saldrá el sentimiento")

        
def main():

    # Crear la barra lateral de navegación
    with st.sidebar:
         st.write("**Algoritmos seleccionados**")
    
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

    

    # Sincronizar los valores de los checkboxes con st.session_state
    for key in alg_sel_urg:
        alg_sel_urg[key] = st.session_state.get(key, alg_sel_urg[key])
    for key in alg_sel_sent:
        alg_sel_sent[key] = st.session_state.get(key, alg_sel_sent[key])

    
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
    



if __name__ == "__main__":
    main()
