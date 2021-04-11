import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import altair as alt
import seaborn as sns
import requests
from bokeh.io import output_file
from bs4 import BeautifulSoup
import imageio as io
import os
import base64
from bokeh.models import Div, RangeSlider, Spinner
from bokeh.layouts import layout
from bokeh.plotting import figure, show
import streamlit.components.v1 as components

with st.echo(code_location='below'):
    df=pd.read_csv("netflix_titles.csv")
    df.dropna(inplace=True)

    st.title("Netflix Movies and TV Shows")

    st.subheader("Release Dates")
    date1 = st.slider('Please select the starting year of the interval', min_value=1940, max_value=2021)
    date2= st.slider('Please select the ending year of the interval', min_value=date1, max_value=2021)
    index=[i for i in range (date1, date2+1)]
    values=[ sum(df['release_year']==i) for i in range (date1, date2+1)]
    fig, ax = plt.subplots()
    plt.title(f"Number of Movies and TV Shows Released Between {date1} and {date2}")
    ax.bar(index, values, color= 'navy')
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Movies and TV Shows Released")
    st.pyplot(fig)

    st.subheader("Proportion of Movies and TV Shows 1980-2021")
    country = st.selectbox('Please select a country', ('United States', 'India', 'United Kingdom', 'Japan', 'South Korea'))
    df1=df[df['country']==country]
    df1['proportion']=1
    df1=df1[['release_year', 'proportion','type' ]]
    df1=df1[df1['release_year']>=1980]
    prop=alt.Chart(df1, title=f'Movies/TV Shows proportion in {country} in 1980-2021').mark_area().encode(
        x=alt.X('release_year'),
        y=alt.Y('proportion', stack="normalize"),
        color='type'
    ).properties(
        width=700,
        height=500
    )
    st.altair_chart(prop)

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
    url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.write(f'Posters for {name}')
    st.markdown(
        f'<img src="data:image/gif;base64,{url}" alt="gif">',
        unsafe_allow_html=True
    )

    st.subheader("Release Date/The Date a Movie Was Added to Netflix")
    df2=df[df['type']=='Movie']
    rate=st.multiselect('Please select rating of a movie', df2['rating'].unique())
    df2=df2[df['rating'].isin(rate)]
    lst=[]
    for i in df2['date_added'].to_list():
        try:
            splt=i.split()
            lst.append(int(splt[-1]))
        except:
            lst.append(int(i))
    df2['year_added']=np.array(lst)
    fig = plt.figure()
    ax = sns.scatterplot(
        data=df2,
        x='release_year',
        y='year_added',
        hue='rating',
        palette='deep',
        picker=True
    )
    plt.xlabel("Release Year")
    plt.ylabel("The Year the Movie Was Added to Netflix")
    st.pyplot(fig)

    st.subheader("TV Shows' Releases")
    df3 = df[df['type'] == 'TV Show']
    x = [i for i in range(1985, 2022)]
    y = [sum(df3['release_year'] == i) for i in range(1985, 2022)]
    output_file("output.html")
    p = figure(x_range=(1985, 2020), plot_width=700, plot_height=500)
    points = p.circle(x=x, y=y, size=15, fill_color="green")
    div = Div(
        text="""
            <p>Please select the circle's size:</p>
            """,
        width=200,
        height=30,
    )
    spinner = Spinner(
        title="Circle size",
        low=3,
        high=30,
        step=3,
        value=points.glyph.size,
        width=200,
    )
    spinner.js_link("value", points.glyph, "size")
    range_slider = RangeSlider(
        title="Adjust x-axis range",
        start=1985,
        end=2021,
        step=1,
        value=(p.x_range.start, p.x_range.end),
    )
    range_slider.js_link("value", p.x_range, "start", attr_selector=0)
    range_slider.js_link("value", p.x_range, "end", attr_selector=1)
    layout = layout([
        [div, spinner],
        [range_slider],
        [p],
    ])
    show(layout)
    htmlf = open("output.html", 'r', encoding='utf-8')
    source_code = htmlf.read()
    print(source_code)
    components.html(source_code, height=700)



