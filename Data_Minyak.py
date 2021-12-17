"""
Aplikasi Streamlit untuk menggambarkan data produksi minyak mentah dari berbagai negara di seluruh duni
Referensi API Streamlit: https://docs.streamlit.io/library/api-reference
"""
## Import Module##
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit as st
from PIL import Image
from HandleofFile import HandleofCSV, HandleofJson
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import plotly.express as px
#########

CSV = HandleofCSV('produksi_minyak_mentah.csv')
JSON = HandleofJson('kode_negara_lengkap.json')

############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Data Produksi Minyak Mentah dari Berbagai Negara di Seluruh Dunia")
st.header("Aplikasi Data Produksi Minyak Mentah")
st.markdown("*Sumber data berasal dari produksi_minyak_mentah.csv*")
st.markdown("Silahkan isi konfigurasi tampilan di kiri layar")
############### title ###############)

############### sidebar ###############
image = Image.open("Oil_rig.jpg")
st.sidebar.image(image)

st.sidebar.title("Konfigurasi")
st.sidebar.subheader("Pengaturan Konfigurasi Tampilan")

######## (a) Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara N ######
st.header("Bagian Pertama")
st.write("Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara")
st.sidebar.subheader("Konfigurasi Bagian Pertama")
datafr = CSV.dataFrame
datafr_info = JSON.dataFrame

ListNegara = datafr_info["name"].tolist()
negara = st.sidebar.selectbox("Pilih nama negara: ", ListNegara) 
kode_negara = datafr_info[datafr_info["name"] == negara]["alpha-3"].tolist()[0]

st.write("Kode negara   :", kode_negara)
st.write("Negara        :",negara)

T = datafr[datafr["kode_negara"] == kode_negara] ["tahun"].tolist()
P = datafr[datafr["kode_negara"] == kode_negara] ["produksi"].tolist()

dict = {"tahun":T,"produksi":P}
if len(dict) == 0:
    st.write("Tidak ada Data")
else:
    st.write(pd.DataFrame(dict))
    plt.title("Grafik Produksi Minyak Mentah Terhadap Waktu Negara {}".format(negara))
    plt.plot(T,P,label="Data Produksi")
    plt.xlabel("Tahun")
    plt.ylabel("Jumlah Produksi")
    plt.legend()
    st.pyplot(plt)

### (b) B-besar negara dengan jumlah produksi terbesar pada tahun T ###
st.header("Bagian Kedua")
st.write("Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar pada tahun T")

st.sidebar.subheader("Konfigurasi Bagian 2")
b = st.sidebar.number_input("Masukkan jumlah besar negara teratas yang diinginkan",  min_value=1, max_value=None)
t = st.sidebar.number_input("Masukkan tahun produksi",  min_value=1971, max_value=2015)

df = datafr
df1 = datafr_info
df = df[df["tahun"] == t]
kode_negara = df[df["tahun"] == t] ["kode_negara"].tolist()
Produksi_terbanyak = []
negara_tahun = []

kode_negara = list(dict.fromkeys(kode_negara))
for kode in kode_negara:
    try:
        produksi = df[df["kode_negara"] == kode ]["produksi"].tolist()
        negara = df1[df1["alpha-3"] == kode] ["name"].tolist()[0]
        Produksi_terbanyak.append(max(produksi))
        negara_tahun.append(negara)
    except: continue
        
dict = {"negara":negara_tahun,"Produksi_terbanyak":Produksi_terbanyak}
df2 = pd.DataFrame(dict)
df2 = df2.sort_values("Produksi_terbanyak",ascending=False).reset_index()
st.write(df2)
plt.clf()

plt.title("{b} Besar Negara dengan Produksi Terbesar pada Tahun {t}".format(b = b, t = t))
plt.bar(df2["negara"][:b],df2["Produksi_terbanyak"][:b],width=0.5, bottom=None, align="center",color="maroon", edgecolor="pink", data=None, zorder=3)
plt.grid(True, color="rosybrown", linewidth="0.5", linestyle="-.", zorder=0)
plt.xlabel("Negara")
plt.ylabel("Besar Produksi")
st.pyplot(plt)

## (c) Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar secara kumulatif keseluruhan tahun
st.header("Bagian Ketiga")
st.write("Grafik yang menunjukan B-besar negara dengan jumlahproduksi terbesar secara kumulatif keseluruhan tahun, dimana nilai B dapat dipilih oleh user secara interaktif")

st.sidebar.subheader("Konfigurasi Bagian 3")
c = st.sidebar.number_input("Masukkan jumlah negara teratas yang diinginkan",  min_value = 1, max_value = None)
df = datafr
df1 = datafr_info
kode_negara = df["kode_negara"].tolist()
kode_negara = list(dict.fromkeys(kode_negara))
Total_produksi = []
negaralist = []
for kode in kode_negara:
    try:
        produksi = df[df["kode_negara"] == kode] ["produksi"].tolist()
        negara = df1[df1["alpha-3"] == kode] ['name'].tolist()[0]
        Total_produksi.append(np.sum(np.array(produksi)))
        if negara not in negaralist:
            negaralist.append(negara)
    except: continue
dict = {"negara":negaralist,"Total_produksi":Total_produksi}
df2 = pd.DataFrame(dict)
df2 = df2.sort_values('Total_produksi',ascending=False).reset_index()
st.write(df2)
plt.clf()

plt.title("{c} Besar Negara dengan Produksi Terbesar Keseluruhan".format(c=c))
plt.bar(df2["negara"][:c],df2["Total_produksi"][:c],width=0.5, bottom=None, align="center",color="Blue", edgecolor="rosybrown", data=None, zorder=3)
plt.grid(True, color="maroon", linewidth="0.5", linestyle="-.", zorder=0)
plt.xlabel("Negara")
plt.ylabel("Total produksi")
st.pyplot(plt)

## (d) INFORMASI ###
st.header("Bagian Keempat")
st.write(" Informasi yang menyebutkan:")
st.write("-nama lengkap negara,kode negara,region,dan sub-region dengan jumlah produksi terbesar pada tahun yang dipilih dan keseluruhan tahun.")
st.write("-nama lengkap negara,kode negara,region,dan sub-region dengan jumlah produksi terkecil pada tahun yang dipilih dan keseluruhan tahun.")
st.write("-nama lengkap negara,kode negara,region,dan sub-region dengan jumlah produksi = 0 pada tahun yang dipilih dan keseluruhan tahun.")

st.sidebar.subheader("Konfigurasi Bagian 4")
T = st.sidebar.number_input("Tahun Produksi", min_value = 1971, max_value = 2015)
df = CSV.dataFrame
df1 = JSON.dataFrame
tahun = list(dict.fromkeys(df["tahun"].tolist()))

dict_maks = {"negara":[],"kode_negara":[],"region":[],"sub_region":[],"produksi":[],"tahun":tahun}
dict_min = {"negara":[],"kode_negara":[],"region":[], "sub_region":[], "produksi":[],"tahun":tahun}
dict_nol = {"negara":[],"kode_negara":[],"region":[],"sub_region":[],"produksi":[],"tahun":tahun}

for t in tahun:
    df_per_tahun = df[df["tahun"] == t]
    produksi = np.array(df_per_tahun["produksi"].tolist())
    maks_prod = max(produksi)
    min_prod = min([p for p in produksi if p != 0])
    zero_prod = min([p for p in produksi if p == 0])
    # maksimum
    kode_negara = df_per_tahun[df_per_tahun["produksi"]==maks_prod]["kode_negara"].tolist()[0]
    if kode_negara == "WLD": kode_negara = "WLF"
    dict_maks["negara"].append(df1[df1["alpha-3"]==kode_negara]["name"].tolist()[0])
    dict_maks["kode_negara"].append(kode_negara)
    dict_maks["region"].append(df1[df1["alpha-3"]==kode_negara]["region"].tolist()[0])
    dict_maks["sub_region"].append(df1[df1["alpha-3"]==kode_negara]["sub-region"].tolist()[0])
    dict_maks["produksi"].append(maks_prod)
    # minimum != 0
    kode_negara = df_per_tahun[df_per_tahun["produksi"]==min_prod]["kode_negara"].tolist()[0]
    if kode_negara == "WLD":kode_negara = "WLF"
    dict_min["negara"].append(df1[df1["alpha-3"]==kode_negara]["name"].tolist()[0])
    dict_min["kode_negara"].append(kode_negara)
    dict_min["region"].append(df1[df1["alpha-3"]==kode_negara]["region"].tolist()[0])
    dict_min["sub_region"].append(df1[df1["alpha-3"]==kode_negara]["sub-region"].tolist()[0])
    dict_min["produksi"].append(min_prod)
    # zero == 0
    kode_negara = df_per_tahun[df_per_tahun["produksi"]==zero_prod]["kode_negara"].tolist()[0]
    if kode_negara == "WLD":kode_negara = "WLF"
    dict_nol["negara"].append(df1[df1["alpha-3"]==kode_negara]["name"].tolist()[0])
    dict_nol["kode_negara"].append(kode_negara)
    dict_nol["region"].append(df1[df1["alpha-3"]==kode_negara]["region"].tolist()[0])
    dict_nol["sub_region"].append(df1[df1["alpha-3"]==kode_negara]["sub-region"].tolist()[0])
    dict_nol["produksi"].append(zero_prod)
df_maks = pd.DataFrame(dict_maks)
df_min = pd.DataFrame(dict_min)
df_nol = pd.DataFrame(dict_nol)

st.write("Info Produksi Maksimum Tahun ke-{}".format(T))
st.write(df_maks[df_maks["tahun"]==T])
st.write("Tabel Maks per Tahun")
st.write(df_maks)
st.write("Info Produksi Minimum (Not Zero) Tahun ke-{}".format(T))
st.write(df_min[df_min["tahun"]==T])
st.write("Tabel Min (Not Zero) per Tahun")
st.write(df_min)
st.write("Info Produksi Zero Tahun ke-{}".format(T))
st.write(df_nol[df_nol["tahun"]==T])
st.write("Tabel Zero per Tahun")
st.write(df_nol)
