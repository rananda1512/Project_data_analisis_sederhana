import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency
sns.set_theme(style='dark')

# memfilter banyak penyewa dalam kurun waktu tertentu
def create_sum_daily(df):
    df_daily_counts = df.groupby('dteday')['cnt'].sum().reset_index()
    return df_daily_counts
#end

# memfilter banyak penyewa berdasarkan musim
def create_sum_season(df): 
    df_season=df.groupby(by="season").cnt.sum().sort_values(ascending=False).reset_index()
# membuat nilai interger season menjadi string agar mudah dipahami audien
    df_season['season'] = df_season['season'].apply(lambda x: 'Musim Dingin' if x == 1 
                                                     else 'Musim Semi' if x == 2 
                                                     else 'Musim Panas' if x == 3 
                                                     else 'Musim Gugur')
    return df_season
#end

def create_season_casual_regisrated(df):
    df_season_casual_register=df.groupby(by="season").agg({
    "casual":"sum",
    "registered":"sum",
}).sort_values(by="casual").reset_index()

# membuat nilai interger season menjadi string agar mudah dipahami audien
    df_season_casual_register['season'] = df_season_casual_register['season'].apply(lambda x: 'Musim Dingin' if x == 1 
                                                     else 'Musim Semi' if x == 2 
                                                     else 'Musim Panas' if x == 3 
                                                     else 'Musim Gugur')
    return df_season_casual_register

# memanggil all_data csv
file_path = os.path.join(os.getcwd(), 'all_data.csv')
all_df=pd.read_csv("dashboard/all_data.csv")
all_df['dteday'] = pd.to_datetime(all_df['dteday']) # mengubah tipe data  fiekl dteday dari object ke datetime
min_date=all_df["dteday"].min()
max_date=all_df["dteday"].max()
#end

season_df=create_sum_season(all_df)

st.header('Bike Sharing Dashboard :bike:')

# membuat diagram line untuk melihat total penyewa dalam kurun waktu tertentu
st.subheader("Daily Sharing Bike")
col1,col2,col3=st.columns([2,3,1])
with col1:
    start_date,end_date=st.date_input(
        label="Rentang waktu",min_value=min_date,
        max_value=max_date,
        value=[min_date,max_date]
    )
    date_df= all_df[(all_df["dteday"]>=str(start_date))&(all_df["dteday"]<=str(end_date))]
    df_sum_daily=create_sum_daily(date_df)

with col2:
    st.write("  ")

with col3:
    st.metric("Total Penyewa", value=df_sum_daily["cnt"].sum())

fig , ax=plt.subplots(figsize=(16,8))
ax.plot(
    df_sum_daily["dteday"],
    df_sum_daily["cnt"],
    marker="o",
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis="y",labelsize=20)
ax.tick_params(axis="x",labelsize=15)

st.pyplot(fig)
#end

# membuat diagram bar untuk memvisualisasikan musim terbaik dengan musim terburuk
st.subheader("Best & Worst Season For Sharing Bike")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="cnt", y="season", data=season_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sharing", fontsize=30)
ax[0].set_title("Best Season", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="cnt", y="season", data=season_df.sort_values(by="cnt", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sharing", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Season", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)
#end

# membual pie chart untuk melihat persentasi perbandingan antara penyewa casual dengan regirated untuk setiap musim
df_season_casual_register = create_season_casual_regisrated(all_df)
tabs = st.tabs(df_season_casual_register['season'].tolist())  # Ambil semua musim sebagai list

# Menampilkan pie chart untuk setiap musim
for i, season in enumerate(df_season_casual_register['season']):
    with tabs[i]:
        st.header(f"Perbandingan Penyewaan Sepeda di {season}")
        
        # Mengambil data pengguna kasual dan terdaftar
        row = df_season_casual_register.iloc[i]
        labels = ['Pengguna Kasual', 'Pengguna Terdaftar']
        sizes = [row['casual'], row['registered']]
        colors = ['red', 'blue']
        explode = (0.1, 0)  # Memisahkan bagian pengguna kasual sedikit dari pie

        # Membuat pie chart
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
               autopct='%1.1f%%', shadow=True, startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie chart is a circle.

        # Menampilkan chart di Streamlit
        st.pyplot(fig)
#end