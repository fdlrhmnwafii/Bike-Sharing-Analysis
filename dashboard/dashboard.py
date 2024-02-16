import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
# Helper Function

def create_bike_share_monthly_df(df):
    monthly_rent_df = df.groupby(['yr','mnth']).agg({
        'cnt':'mean'
        })
    month_mapping = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
    year_mapping = {0: 2011, 1: 2012}
    monthly_rent_df.rename(index=year_mapping, level='yr', inplace=True)
    monthly_rent_df.rename(index=month_mapping, level='mnth', inplace=True)
    return monthly_rent_df

def create_holidays_df(df):
    rent_bike_2011 = df[df['yr']==0]
    rent_bike_2012 = df[df['yr']==1]
    days_mapping = {
        0 : 'Working Days',
        1 : 'Holidays'
        }
    rent_bike_2011['holiday'] = rent_bike_2011['holiday'].map(days_mapping)
    rent_bike_2012['holiday'] = rent_bike_2012['holiday'].map(days_mapping)
    grouped_by_holiday_2011 = rent_bike_2011.groupby('holiday')['cnt'].count()
    grouped_by_holiday_2012 = rent_bike_2012.groupby(['holiday'])['cnt'].count()
    return grouped_by_holiday_2011, grouped_by_holiday_2012

def create_season_df(df):
    season_df = df
    season_labels = {
        1 : 'Clear',
        2 : 'Mist',
        3 : 'Light (Snow/Rain)',
        4 : 'Heavy Rain'
        }
    season_df['season'] = season_df['season'].map(season_labels)
    group_season = season_df.groupby('season')['cnt'].sum().reset_index().sort_values('cnt')
    return group_season

# load dataset
bike_sharing_df = pd.read_csv('https://github.com/fdlrhmnwafii/Bike-Sharing-Analysis/blob/main/dashboard/hour.csv')
bike_sharing_df['dteday'] = pd.to_datetime(bike_sharing_df['dteday'])

# Filter Data
min_date = bike_sharing_df['dteday'].min()
max_date = bike_sharing_df['dteday'].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = bike_sharing_df[(bike_sharing_df["dteday"] >= str(start_date)) & 
                (bike_sharing_df["dteday"] <= str(end_date))]

# preparing data frame
bike_share_monthly = create_bike_share_monthly_df(main_df)
holidays_df2011, holidays_df2012 = create_holidays_df(main_df)
season_df = create_season_df(main_df)

st.header('Fadel Bike Sharing Dashboard :sparkles:')
st.subheader('Bike Sharing Perform')
st.dataframe(data=bike_share_monthly)

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x='mnth',
    y='cnt',
    data=bike_share_monthly,
    marker='o',
    hue='yr',
    ax=ax
)
ax.set_title('Monthly Bike Rental Counts Over Time')
ax.set_xlabel('Month')
ax.set_ylabel('Rental Counts')
ax.legend(title='Year', labels=['2011', '2012'], loc='upper left')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

st.pyplot(fig)

st.subheader("Comparison of Bike Share During Holidays and Working Days per Year")
st.dataframe(data=holidays_df2011)
st.dataframe(data=holidays_df2012)

colors = ["#D3D3D3", "#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
plt.suptitle('Number of Observations in Holidays', fontsize=15)

holidays_df2011.plot(kind='bar', color=colors, ax=ax[0])
ax[0].set_title('in 2011', loc="center", fontsize=10)
ax[0].set_xlabel('Category')
ax[0].set_ylabel('Count')
ax[0].tick_params(axis ='y', labelsize=10)
ax[0].tick_params(axis ='x', labelsize=10)
ax[0].set_xticklabels(holidays_df2011.index, rotation=0)

holidays_df2012.plot(kind='bar', color=colors, ax=ax[1])
ax[1].set_title('in 2012', loc="center", fontsize=10)
ax[1].set_xlabel('Category')
ax[1].set_ylabel('Count')
ax[1].tick_params(axis ='y', labelsize=10)
ax[1].tick_params(axis ='x', labelsize=10)
ax[1].set_xticklabels(holidays_df2012.index, rotation=0)

st.pyplot(fig)

st.subheader("Average Bike Rent Depends on Seasonal Condition")
st.dataframe(data=season_df)

colors = ["#D3D3D3","#D3D3D3", "#D3D3D3", "#72BCD4"]
fig, ax = plt.subplots(figsize=(8, 8))
sns.barplot(
    x = 'season',
    y = 'cnt',
    data=season_df,
    palette=colors,
    ax=ax
)
ax.set_title('Count Bike Sharing based on Season')
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.ticklabel_format(style='plain', axis='y')
st.pyplot(fig)
