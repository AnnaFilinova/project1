import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

with st.echo(code_location='below'):
    df=pd.read_csv("netflix_titles.csv")
    st.title("Netflix Movies and TV Shows")
    date1 = st.slider('The Starting Year of the Interval', min_value=1925, max_value=2021)
    date2= st.slider('The Ending Year of the Interval', min_value=date1, max_value=2021)
    index=[i for i in range (date1, date2+1)]
    values=[ sum(df['release_year']==i) for i in range (date1, date2+1)]
    fig, ax = plt.subplots()
    plt.title(f"Number of Movies and TV Shows Released Between {date1} and {date2}")
    ax.bar(index, values)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Movies and TV Shows Released")
    plt.show()
