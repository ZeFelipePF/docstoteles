import streamlit as st 
from service.rag import RAGService

def show():
    if not st.session_state.collection:
        st.info("Por favor, selecione uma coleção na barra lateral para começar a conversar.")
        return
    
    col1, col2 = st.columns([9, 1])
    with col1:
        collection_name = st.session_state.collection.title()
        st.header(f"Coleção selecionada: **{collection_name}**")
    with col2:
        if st.button("Limpar Conversa"):
            st.session_state.messages = []
            st.rerun()

    if 'rag_service' not in st.session_state:
        st.session_state.rag_service = RAGService()

    if 'current_collection' not in st.session_state or st.session_state.current_collection != st.session_state.collection:
        with st.spinner("Carregando a coleção..."):
            loaded = st.session_state.rag_service.load_collection(st.session_state.collection)
            if not loaded:
                st.error("Falha ao carregar a coleção. Verifique se os documentos existem.")
                return
            st.session_state.current_collection = st.session_state.collection
            st.info("Coleção carregada com sucesso!")
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Digite sua pergunta aqui..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message('assistant'):
            with st.spinner("Pensando..."):
                response = st.session_state.rag_service.answer_question(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)

    