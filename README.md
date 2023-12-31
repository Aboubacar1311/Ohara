# Ohara
This repository is part of a project to set up a system for extracting text from images and PDFs, and also for extracting tables from PDFs using the [Streamlit](https://docs.streamlit.io/) framework.
## Setup 
1. Install Streamlit  
    ```
    pip install streamlit
    ```
2. Clone  
   ```
   git clone https://github.com/Aboubacar1311/Ohara.git
   ```
3. Change Directory  
```
   cd Ohara
```
5. Execute  
   ```
   streamlit run app.py
   ```
   __Or__
```
   py -m streamlit run .\app.py
   ```
## On your default browser  
A new page will be created and you'll see a similar interface in the images below.  
![Cover](https://github.com/Aboubacar1311/Ohara/blob/981ec3294a9442077b49f1af920495f2df24bd50/img/12.png)  
  
You have two choices, either to extract text from an image in a PDF or to extract a table in a pdf. 
If you wish to extract a table, you must enter the page number from which you wish to extract the table. The default (0) is to extract all tables in the table. 