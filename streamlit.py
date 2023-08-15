import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# Set global font to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

@st.cache_data
# def load_data():
#     return pd.read_csv('geography.csv')

def load_data(limit = 100000):
    # Endpoint url
    url = 'https://data.cdc.gov/resource/n8mc-b4w4.json'
    
    # Add query parameter for limiting results
    params = {'$limit': limit}
    
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        # Convert 'county_fips_code' to strings
        df['county_fips_code'] = df['county_fips_code'].astype(str)

        # Convert 'NA' to NaN
        df['county_fips_code'] = pd.to_numeric(df['county_fips_code'], errors='coerce')

        return df
    
    else:
        st.error("Failed to load data")
        return pd.DataFrame()

    


def plot_county_cases(df, county_fips_code):
    
    # Filter dataframe for rows where 'county_fips_code' matches the input
    specific_county = df[df['county_fips_code'] == county_fips_code]
    
    
    # for error testing load_data api
    st.write(specific_county)

    # Error Checking for if no data found
    if specific_county.empty:
        st.write(f"No data found for county_fips_code: {county_fips_code}")
        return
    
    # Group by 'case_month' and count the number of cases for each month
    monthly_counts = specific_county.groupby('case_month').size()

    # Error Checking for if no monthly counts found
    if monthly_counts.empty:
        st.write(f"No monthly case data found for county_fips_code: {county_fips_code}")
        return

    # Create a new figure
    fig, ax = plt.subplots(figsize=(10,6))

    # Plot the result
    ax.plot(monthly_counts.index, monthly_counts.values, marker='o', color='red')

    ax.set_xlabel('Month', fontsize=14)
    ax.set_ylabel('Number of Cases', fontsize=14)
    ax.set_title(f'Number of Cases per Month for County: {county_fips_code}', fontsize=16)
    ax.grid(True)
    
    return fig
    

df = load_data()
    
county_fips_code = st.text_input("Enter a county fips code:")

if county_fips_code:
    county_fips_code = float(county_fips_code)  # Convert the input to float
    fig = plot_county_cases(df, county_fips_code)
    if fig:
        st.pyplot(fig)