import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_byseason_df(df):
    season_mapping = {1: "spring", 2: "summer", 3: "fall", 4: "winter"}
    df["season"] = df["season"].map(season_mapping)
    byseason_df = df.groupby(by="season").cnt.sum().reset_index()
    return byseason_df
def create_bytemp_df(df):
    bytemp_df = df.groupby(by="temp_group").cnt.sum().reset_index()
    return bytemp_df
def create_byweather_df(df):
    weather_mapping = {1: "Sejuk", 2: "Berawan", 3: "Hujan Ringan", 4: "Hujan Lebat/Badai Salju"}
    df["weathersit"] = df["weathersit"].map(weather_mapping)
    byweather_df = df.groupby(by="weathersit").cnt.sum().reset_index()
    return byweather_df
def create_byholiday_df(df):
    byholiday_df = df.groupby(by="holiday").cnt.sum().reset_index()
    return byholiday_df
def create_byworkday_df(df):
    byworkday_df = df.groupby(by="workingday").cnt.sum().reset_index()
    return byworkday_df
def create_registered_df(df):
    registered_df = df.groupby(by="registered").cnt.sum().reset_index()
    return registered_df
def create_notregistered_df(df):
    not_registered_df = df.groupby(by="casual").cnt.sum().reset_index()
    return not_registered_df

analysis_df = pd.read_csv("bike_rental_analysis.csv")

datetime_columns = ["dteday"]
analysis_df.sort_values(by="dteday", inplace=True)
analysis_df.reset_index(inplace=True)


for column in datetime_columns:
    analysis_df[column] = pd.to_datetime(analysis_df[column])

min_date = analysis_df["dteday"].min()
max_date = analysis_df["dteday"].max()
 
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = analysis_df[(analysis_df["dteday"] >= str(start_date)) & 
                (analysis_df["dteday"] <= str(end_date))]

byseason_df = create_byseason_df(main_df)
bytemp_df = create_bytemp_df(main_df)
byweather_df = create_byweather_df(main_df)
byholiday_df = create_byholiday_df(main_df)
byworkday_df = create_byworkday_df(main_df)
registered_df = create_registered_df(main_df)
not_registered_df = create_notregistered_df(main_df)

st.header("Analisis Jasa Rental Sepeda :bike:")
st.subheader ("Jumlah Sepeda yang Disewakan")

total_count = main_df["cnt"].sum()
st.metric("Jumlah Sepeda Disewakan", value=total_count)

daily_counts = main_df.groupby("dteday")["cnt"].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(daily_counts["dteday"], daily_counts["cnt"], marker='o')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Sepeda")
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader ("Jumlah Sepeda yang Dirental Berdasarkan Faktor Lingkungan")

col1, col2, col3 = st.columns(3)

with col1:
    fig, ax = plt.subplots(figsize=(5, 5))
    max_value = byseason_df["cnt"].max()
    colors = ["#D3D3D3" if cnt != max_value else "#90CAF9" for cnt in byseason_df["cnt"]]
    sns.barplot(data=byseason_df, x="season", y="cnt", ax=ax, palette=colors)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("Berdasarkan Musim")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(5, 5))
    max_value = bytemp_df["cnt"].max()
    colors = ["#D3D3D3" if cnt != max_value else "#90CAF9" for cnt in bytemp_df["cnt"]]
    sns.barplot(data=bytemp_df, x="temp_group", y="cnt", ax=ax, palette = colors)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("Berdasarkan Suhu")
    st.pyplot(fig)

with col3:
    fig, ax = plt.subplots(figsize=(5, 5))
    max_value = byweather_df["cnt"].max()
    colors = ["#D3D3D3" if cnt != max_value else "#90CAF9" for cnt in byweather_df["cnt"]]
    sns.barplot(data=byweather_df, x="weathersit", y="cnt", ax=ax, palette = colors)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("Berdasarkan Cuaca")
    st.pyplot(fig)

st.subheader ("Jumlah Sepeda yang Dirental Berdasarkan Faktor Tanggal dan Hari")
col1, col2 = st.columns(2)

holiday = main_df.groupby("holiday")["cnt"].mean().reset_index()
holiday["holiday"] = holiday["holiday"].map({0: "Bukan Hari Libur", 1: "Hari Libur"})

workingday = main_df.groupby("workingday")["cnt"].mean().reset_index()
workingday["workingday"] = workingday["workingday"].map({0: "Bukan Hari Kerja", 1: "Hari Kerja"})

with col1:
    fig, ax = plt.subplots(figsize=(5, 5))
    max_value = holiday["cnt"].max()
    colors = ["#D3D3D3" if cnt != max_value else "#90CAF9" for cnt in holiday["cnt"]]
    sns.barplot(x=["Bukan Hari Libur", "Hari Libur"], y=holiday["cnt"], ax=ax, palette=colors)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("Berdasarkan Hari Libur")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(5, 5))
    max_value = workingday["cnt"].max()
    colors = ["#D3D3D3" if cnt != max_value else "#90CAF9" for cnt in workingday["cnt"]]
    sns.barplot(x=["Bukan Hari Kerja", "Hari Kerja"], y=workingday["cnt"], ax=ax, palette=colors)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("Berdasarkan Hari Kerja")
    st.pyplot(fig)

st.subheader ("Komparasi Jumlah Pengguna yang Sudah Registrasi dan Belum")

fig, ax = plt.subplots(figsize=(5, 5))
registered_counts = registered_df.sum()
not_registered_counts = not_registered_df.sum()
labels = ["Sudah Registrasi", "Belum Registrasi"]
sizes = [registered_counts["registered"], not_registered_counts["casual"]]
colors = ["#90CAF9", "#D3D3D3"]
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
ax.axis('equal')
st.pyplot(fig)