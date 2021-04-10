import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import altair as alt
import seaborn as sns
import requests
from bs4 import BeautifulSoup
import imageio as io
import os
import base64

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

    st.subheader("Proportion of Movies and TV Shows 1980-2021")
    sb = st.selectbox('Please select a country', ('United States', 'India', 'United Kingdom', 'Japan', 'South Korea'))
    country=sb
    df1=df[df['country']==country]
    df1['proportion']=1
    df1=df1[['release_year', 'proportion','type' ]]
    df1=df1[df1['release_year']>=1980]

    st.write(alt.Chart(df1, title=f'Movies/TV Shows proportion in {country} in 1980-2021').mark_area().encode(
        x='release_year:O',
        y=alt.Y('proportion:Q', stack="normalize"),
        color='type'
    ).properties(
        width=700,
        height=500
    ))
    #st.write(c)

    st.subheader("Would you like some posters?")
    fl=st.select_slider('Please select the first letter of a movie/TV show',
                        options=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'])
    lst=df['title'].unique()
    lst=[i for i in lst if i.startswith(fl)]
    name=st.selectbox('Please choose which poster you want to look at', lst)
    Name = ''
    for i in name.split():
        Name = Name + '+' + i
    Name = Name[1:]
    url = f'https://www.google.com/search?q={Name}+netflix&newwindow=1&safe=active&sxsrf=ALeKk00c55dPIS91D_lKRoWWdgnl_CR3CQ:1618000988414&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjBjKSxg_LvAhVjwIsKHTORBi0Q_AUoAXoECAEQAw&biw=1536&bih=754'
    r = requests.get(url)
    s = BeautifulSoup(r.text)
    allpstr = s.find_all('img')
    with io.get_writer('posters.gif', mode='I', duration=0.5) as writer:
        for i in range (10):
            image = io.imread(allpstr[i+1]['src'])
            writer.append_data(image)
    writer.close()
    file_ = open("posters.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt=f'Posters for {name}'>',
        unsafe_allow_html=True,
    )
    #st.write(f'Poster for {name}')
    #st.image(pstr, width=250)
    #st.balloons()


