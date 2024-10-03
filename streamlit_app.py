import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
sns.set(style='dark')


def create_hourGroup_df(hour_df):
    hour_df["hr_group"] = hour_df.hr.apply(lambda x: "Subuh" if x>=0 and x<6 
                                       else ("Pagi" if x>=6 and x<11 
                                             else ("Siang" if x>=11 and x<15 
                                                   else "Sore" if x>=15 and x<18 else "Malam")
                                            )
                                      )
    hourGroup_df = hour_df.groupby(by="hr_group").cnt.sum().reset_index()
    return hourGroup_df


def create_monthlyYear_df(day_df):
    monthlyYear_df = day_df.groupby(by=["yr","mnth"]).cnt.sum().reset_index()
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    year2011=monthlyYear_df[monthlyYear_df['yr'] == '2011']
    year2011 = year2011.set_index('mnth').loc[month_order].reset_index()

    year2012=monthlyYear_df[monthlyYear_df['yr'] == '2012']
    year2012 = year2012.set_index('mnth').loc[month_order].reset_index()

    return year2011,year2012

def create_season_df(day_df):
    season_df = day_df.groupby(by="season").cnt.sum().reset_index()
    return season_df




st.header('Proyek Bike Sharing Dicoding  :sparkles:')

hour_df = pd.read_csv("data/hour.csv")
day_df = pd.read_csv("data/day.csv")
day_df['mnth'] = day_df['mnth'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['yr']= day_df['yr'].map({
    0: '2011', 1: '2012'
})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Clear/Few Clouds',
    2: 'Cloudy/Mist',
    3: 'Light Rain',
    4: 'Heavy Rain'
})

hourGroup_df=create_hourGroup_df(hour_df)
year2011,year2012=create_monthlyYear_df(day_df)
season_df=create_season_df(day_df)

column = "dteday"
day_df.sort_values(by=column, inplace=True)
day_df.reset_index(inplace=True)
hour_df.sort_values(by=column, inplace=True)
hour_df.reset_index(inplace=True)

day_df[column] = pd.to_datetime(day_df[column])
hour_df[column] = pd.to_datetime(hour_df[column])



min_date = day_df[column].min()
max_date = day_df[column].max()
 


with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://static.vecteezy.com/system/resources/previews/007/280/351/original/bike-sharing-rental-service-icon-vector.jpg")
    start_date, end_date = st.date_input(
        label='Time Span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.subheader("Kelompok Jumlah Penjualan")
col1, col2 = st.columns(2)
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"] 

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="cnt", 
        x="season",
        data=season_df.sort_values(by="cnt", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Jumlah Penjualan Setiap Bulan", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="cnt", 
        x="hr_group",
        data=hourGroup_df.sort_values(by="cnt", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Jumlah Penjualan Kelompok Jam", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

st.subheader("Perbandingan Jumlah total penjualan dalan 2 tahun")
year2011 = year2011.reset_index()
year2012 = year2012.reset_index()
data = pd.DataFrame({
    '2011':year2011['cnt'],
    '2012':year2012['cnt']}
)
st.write("")

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
month_type = pd.CategoricalDtype(categories=months, ordered=True)
data.index = pd.Index(months, dtype=month_type)

st.line_chart(data)   
