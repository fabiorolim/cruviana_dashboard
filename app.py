import streamlit as st
import pandas as pd
from api.service import get_data
import folium
from streamlit_folium import st_folium

st.image('img/ifpi.png', width=150)
st.title('Cruviana Dashboard')
st.subheader('Estação Meteorológica: UAPP IFPI Oeiras')
st.write('---')
st.header("Leituras")
data = st.date_input('Data')


def load_data():
    df = pd.DataFrame(get_data(data))

    df = df.drop(columns=['Data_add', 'Data',
                          'WindSpeed', 'WindSpeed10Min',
                          'RainRate', 'ETMonth',
                          'RainStorm', 'Station',
                          ])

    df = df.set_index('id')
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['Datetime'] = df['Datetime'].dt.strftime('%d/%m/%Y %H:%M')

    return df


leituras = load_data()
st.write(leituras)
st.write('---')
st.subheader('Temperatura')
st.line_chart(data=leituras, x='Datetime', y='TempOut', color='#F00')
st.write(f'Temperatura mínima: {leituras.TempOut.min()} ºC')
st.write(f'Temperatura máxima: {leituras.TempOut.max()} ºC')
st.write('---')
st.subheader('Precipitações')
st.line_chart(data=leituras, x='Datetime', y='RainDay')
st.write(f'Volume total acumulado: {leituras.RainDay.max()} mm')
st.write('---')
st.subheader('Localização')
m = folium.Map(
    location=[-7.000126399270931, -42.10095318786533],
    zoom_start=20
)
folium.Marker(
    [-7.000126399270931, -42.10095318786533],
    popup='Estação Meteorológica UAPP - IFPI',
    tooltip='Estação Meteorológica UAPP - IFPI'
).add_to(m)

mapa = st_folium(m, width=700)
