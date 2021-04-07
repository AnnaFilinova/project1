import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import altair as alt

with st.echo(code_location='below'):
    df=pd.read_csv("netflix_titles.csv")

    st.title("Netflix Movies and TV Shows")

    st.subheader("Release Dates")
    date1 = st.slider('Please select the starting year of the interval', min_value=1925, max_value=2021)
    date2= st.slider('Please select the ending year of the interval', min_value=date1, max_value=2021)
    index=[i for i in range (date1, date2+1)]
    values=[ sum(df['release_year']==i) for i in range (date1, date2+1)]
    fig, ax = plt.subplots()
    plt.title(f"Number of Movies and TV Shows Released Between {date1} and {date2}")
    ax.bar(index, values)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Movies and TV Shows Released")
    st.pyplot(fig)

    st.subheader("Proportion of Movies and TV Shows")
    #Choose country
    country='United States'
    df1=df[df['country']==country]
    df1=df1[['release_year', 'type']]
    df1['values']=1
    c=alt.Chart(df1).mark_area().encode(
        x='release_year:T',
        y=alt.Y('Type:Q'),
        color='type'
    )
    st.write(c)
