import pandas as pd
import geopandas as gpd
import streamlit as st
import matplotlib.pyplot as plt

# Load the processed data and GeoJSON
@st.cache
def load_data():
    # Membaca data dari file filtered_data.csv
    try:
        data = pd.read_csv('filtered_data.csv')
        data['Date'] = pd.to_datetime(data['Date'])  # Pastikan kolom 'Date' dalam format datetime
        return data
    except FileNotFoundError:
        print("File filtered_data.csv tidak ditemukan. Pastikan file tersebut ada di direktori yang benar.")
        return pd.DataFrame()  # Kembalikan DataFrame kosong jika file tidak ditemukan

@st.cache
def load_geojson():
    # Load GeoJSON
    geojson_path = "indonesia.geojson" 
    geojson = gpd.read_file(geojson_path)
    return geojson

# Load datasets
data = load_data()
provinces = load_geojson()

# Sidebar filter
st.sidebar.title("Filter Data")
start_date = st.sidebar.date_input("Tanggal Awal", pd.to_datetime("2021-05-01"))

# Filter data berdasarkan tanggal
filtered_data = data[data['Date'] >= pd.to_datetime(start_date)]

# Gabungkan GeoJSON dengan data kasus
merged = provinces.merge(filtered_data, left_on="state", right_on="Province", how="left")

# Header
st.title("Dashboard Kasus COVID-19 di Indonesia")
st.write(f"Menampilkan data mulai dari: **{start_date}**")

# Display filtered data
st.subheader("Data Filtered")
st.dataframe(filtered_data)

# Visualisasi peta
st.subheader("Visualisasi Peta")
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
merged.plot(
    column="Total Cases",
    cmap="Reds",
    legend=True,
    legend_kwds={"label": "Total Kasus COVID-19"},
    ax=ax,
    missing_kwds={"color": "lightgrey", "label": "No Data"}
)
plt.title("Sebaran Kasus Positif COVID-19", fontsize=16)
plt.axis("off")

# Tampilkan peta
st.pyplot(fig)
