import streamlit as st
import time
import pandas as pd
# semantic role labeling classification
from src.srl_methods.classification import extract
# predictor
from src.transformer_predictor import predictor
# Text to show 
file1=open('media/text/home.txt')
file2=open('media/text/tools.txt')
file3=open('media/text/authors.txt')
home=file1.read()
tools=file2.read()
authors=file3.read()
# Examples to make predictions
sentences=pd.read_csv('io/input/inputs.csv',header=0)

######################################################
################## PAGE SETTINGS #####################
######################################################
st.set_page_config(page_title="KICoDi",
                   page_icon=":book:",
                   layout="wide",
                   initial_sidebar_state="auto"
)
st.header('KICoDi')
######################################################
################# SIDEBAR SETTINGS ###################
######################################################
st.sidebar.image('media/logo.png')
st.sidebar.header('KICoDi')
nav=st.sidebar.radio('',['Inference','Home','Authors'])
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('2022')
st.sidebar.write('Contact')
st.sidebar.write('[I. Arroyo](https://iarroyof.github.io)')
st.sidebar.write('[Y. Balderas](https://github.com/Yalbibalderas)')
st.sidebar.write('[E. Galicia](https://enriquegap.github.io)')
######################################################
###################### HOME ##########################
######################################################
if nav=='Home':
    st.subheader('Knowledge Inference for nonCommunicable Diseases literature')
    st.markdown('___')
    st.markdown(home)
######################################################
#################### RUN MODEL #######################
######################################################
if nav=='Inference':
    st.markdown('___')
    st.markdown(tools)
    example = st.selectbox(
    'Example Inputs',sentences)
    input = st.text_area("Use the example below or input your own text in English",
    			  value=example, max_chars=100, height=100)
    if st.button('Go'):
            if len(input) < 10:
                st.error('Please enter a text in English of minimum 10 characters')
            else:
                with st.spinner('Running...'):
                    time.sleep(3)
                    SP_O=extract(input)                            
                    Subject_Predicate = SP_O[0]#"The cause of lung cancer can be"
                    Object = SP_O[1]#"DNA methylation"
                    prediction=predictor((Subject_Predicate, Object))
                    prediction = prediction.replace("[start] ", '').replace(" [end]", '')
                    st.write(f"\n\n\n\nGiven sentence: {Subject_Predicate} {Object}")
                    st.write(f"Generated sentence: {Subject_Predicate} {prediction}")
                #st.dataframe(pd.read_csv('io/output/data.csv'))
                #with open('io/output/data.csv') as f:
                #    st.download_button('Download CSV', f, 'nlp_results.csv')
######################################################
###################### ABOUT #########################
######################################################
if nav=='Authors':
    st.markdown('___')
    st.markdown(authors,unsafe_allow_html=True)
