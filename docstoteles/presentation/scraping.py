import os 
import streamlit as st
from dotenv import load_dotenv
from service.scrapping import ScrappingService

def show():
    st.header("Web Scraping")

    scraper = ScrappingService()

    with st.form("scrape_form"):
        url = st.text_input("URL do site para scraping:", placeholder="https://example.com")
        collection_name = st.text_input("Nome da coleção para salvar os dados:", placeholder="minha_colecao")

        submitted = st.form_submit_button("Iniciar Scraping")

        if submitted and url and collection_name:
            with st.spinner("Iniciando o scraping..."):
                result = scraper.scrape_website(url, collection_name)
                if result.get("success"):
                    st.success(f"Scraping concluído! {result.get('files', 0)} arquivos salvos na coleção '{collection_name}'.")
                else:
                    st.error(f"Erro durante o scraping: {result.get('error')}")