import streamlit as st
import pdf2image
from PIL import Image
import pytesseract
from pytesseract import Output, TesseractError
import pandas as pd
import tabula
import PyPDF2
from subprocess import CalledProcessError
from mes_function import convert_pdf_to_txt_pages, convert_pdf_to_txt_file, save_pages, displayPDF, images_to_txt
#Installer JDK
st.set_page_config(page_title="Ohara")


html_temp = """
            <div style="background-color:{};padding:1px">
            
            </div>
            """


st.markdown("""
    ## Extraire du texte d'une image ou d'un pdf
    
""")

    
languages = {
    'English': 'eng',
    'French': 'fra',
}

with st.sidebar:
    st.title(":outbox_tray: Ohara")
    textOutput = st.selectbox(
        "Comment voulez-vous que votre texte de sortie soit rédigé ?",
        ('En fichier texte (.txt)', 'En Fichier texte par page (ZIP)'))
    ocr_box = st.checkbox("Activer l'OCR (document numérisé)(scanner le document)")
    
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    Project de Fin d'etude en Master Data Science 
    """)
    
tab1, tab2 = st.tabs(["Extraire du Texte dans un fichier", "Extraire un Tableau dans un fichier"])

with tab1:
    pdf_file = st.file_uploader("Chargez votre fichier", type=['pdf', 'png', 'jpg','jpeg'], key = 'tab1')
    hide="""
    <style>
    footer{
        visibility: hidden;
            position: relative;
    }
    .viewerBadge_container__1QSob{
        visibility: hidden;
    }
    #MainMenu{
        visibility: hidden;
    }
    <style>
    """
    st.markdown(hide, unsafe_allow_html=True)
    if pdf_file:
        path = pdf_file.read()
        file_extension = pdf_file.name.split(".")[-1]
        
        if file_extension == "pdf":
            # display document
            with st.expander("Display document"):
                displayPDF(path)
            if ocr_box:
                option = st.selectbox('Sélectionner la langue du fichier', list(languages.keys()))
            # pdf to text
            if textOutput == 'One text file (.txt)':
                if ocr_box:
                    texts, nbPages = images_to_txt(path, languages[option])
                    totalPages = "Pages: "+str(nbPages)+" in total"
                    text_data_f = "\n\n".join(texts)
                else:
                    text_data_f, nbPages = convert_pdf_to_txt_file(pdf_file)
                    totalPages = "Pages: "+str(nbPages)+" in total"

                st.info(totalPages)
                st.download_button("Télécharger le fichier texte", text_data_f)
            else:
                if ocr_box:
                    text_data, nbPages = images_to_txt(path, languages[option])
                    totalPages = "Pages: "+str(nbPages)+" in total"
                else:
                    text_data, nbPages = convert_pdf_to_txt_pages(pdf_file)
                    totalPages = "Pages: "+str(nbPages)+" in total"
                st.info(totalPages)
                zipPath = save_pages(text_data)
                # download text data   
                with open(zipPath, "rb") as fp:
                    btn = st.download_button(
                        label="Download ZIP (txt)",
                        data=fp,
                        file_name="pdf_to_txt.zip",
                        mime="application/zip"
                    )
                
        else:
            option = st.selectbox("Quelle est la langue du texte dans l'image ?", list(languages.keys()))
            pil_image = Image.open(pdf_file)
            text = pytesseract.image_to_string(pil_image, lang=languages[option])
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("Afficher l'image"):
                    st.image(pdf_file)
            with col2:
                with st.expander("Afficher le texte"):
                    st.info(text)
            st.download_button("Télécharger le fichier texte", text)
st.caption("Projet de fin d'études de @MAIGA_Aboubacar_Abdou")
with tab2:
    n_pages = int(st.number_input('Entrez le numero de la page ou se trouve le Tableau',step = 1))

    pdf_file = st.file_uploader("Chargez votre fichier PDF", type=['pdf'], key= 'tab2')
    st.markdown(hide, unsafe_allow_html=True)

    if pdf_file:
        try :
            if n_pages == 0:
                df = tabula.io.read_pdf(pdf_file, pages= "all")
                i = 0
                cle = 0
                while i != len(df):
                    st.dataframe(df[i])
                    df[i] = df[i].to_csv(index=False).encode("utf-8")
                    st.download_button("Télécharger le fichier texte", df[i],"Ohara.csv", "text/csv", key= cle,)
                    i = i+1
                    cle =cle + 1
            else:
                df = tabula.io.read_pdf(pdf_file, pages= n_pages)
                i = 0
                cle = 0
                while i != len(df):
                    st.dataframe(df[i])
                    df[i] = df[i].to_csv(index=False).encode("utf-8")
                    st.download_button("Télécharger le fichier texte", df[i],"Ohara.csv", "text/csv", key= cle)
                    i = i+1
                    cle =cle + 1
        except IndexError as e:
            st.write("Le numéro de page n'existe pas.")