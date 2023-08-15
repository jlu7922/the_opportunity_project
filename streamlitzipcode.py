# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import requests

# # Set global font to Times New Roman
# plt.rcParams['font.family'] = 'Times New Roman'

# def find_fips(zip_code, type=3): # Set type to 3 for ZIP to County
#     url = f"https://www.huduser.gov/hudapi/public/usps?type={type}&query={zip_code}"
#     token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjQ3NTkxODc3ZTAxM2FjZjhhMzUzYTY0YzcxOGY3MGIyYzljMWVhYjBjOTliNWE0NzIzYmE0ZDBiYmZjNDhkOGYxMGZiMDg1NGIyM2Q3ZWU3In0.eyJhdWQiOiI2IiwianRpIjoiNDc1OTE4NzdlMDEzYWNmOGEzNTNhNjRjNzE4ZjcwYjJjOWMxZWFiMGM5OWI1YTQ3MjNiYTRkMGJiZmM0OGQ4ZjEwZmIwODU0YjIzZDdlZTciLCJpYXQiOjE2OTIwMzQ4ODMsIm5iZiI6MTY5MjAzNDg4MywiZXhwIjoyMDA3NjU0MDgzLCJzdWIiOiI1NjAxNSIsInNjb3BlcyI6W119.JacEPIzzNZDQvk_0STKfTT-JuRDsVYW3ERKfR18-EcUpH5H_znFMirmivU4TQ3FKEZhDT0GK9AMS_g6hUGRB0Q"
    
#     headers = {"Authorization": "Bearer {0}".format(token)}

#     response = requests.get(url, headers=headers)
    
#     if response.status_code != 200:
#         st.error("Failed to fetch FIPS code")
#         return []

#     response_data = response.json()
#     results = response_data["data"]["results"]
#     fips_codes = [result["geoid"][:5] for result in results] # Extracting the first 5 characters of geoid for county FIPS code

#     return fips_codes


# @st.cache_data
# def load_data(limit=100000):
#     # Endpoint url
#     url = 'https://data.cdc.gov/resource/n8mc-b4w4.json'
    
#     # Add query parameter for limiting results
#     params = {'$limit': limit}
    
#     response = requests.get(url, params=params)

#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.json()
#         df = pd.DataFrame(data)

#         # Convert 'county_fips_code' to strings
#         df['county_fips_code'] = df['county_fips_code'].astype(str)

#         # Convert 'NA' to NaN
#         df['county_fips_code'] = pd.to_numeric(df['county_fips_code'], errors='coerce')

#         return df
    
#     else:
#         st.error("Failed to load data")
#         return pd.DataFrame()

# def plot_county_cases(df, fips_codes):
#     for county_fips_code in fips_codes:
#         specific_county = df[df['county_fips_code'] == float(county_fips_code)]
#         st.write(specific_county)

#         if specific_county.empty:
#             st.write(f"No data found for county_fips_code: {county_fips_code}")
#             continue

#         monthly_counts = specific_county.groupby('case_month').size()
#         if monthly_counts.empty:
#             st.write(f"No monthly case data found for county_fips_code: {county_fips_code}")
#             continue

#         fig, ax = plt.subplots(figsize=(10,6))
#         ax.plot(monthly_counts.index, monthly_counts.values, marker='o', color='red')

#         ax.set_xlabel('Month', fontsize=14)
#         ax.set_ylabel('Number of Cases', fontsize=14)
#         ax.set_title(f'Number of Cases per Month for County: {county_fips_code}', fontsize=16)
#         ax.grid(True)

#         st.pyplot(fig)

# df = load_data()

# zip_code = st.text_input("Enter a ZIP code:")

# if zip_code:
#     fips_codes = find_fips(zip_code)
#     if fips_codes:
#         plot_county_cases(df, fips_codes)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# Set global font to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

def find_fips(zip_code, type=2): # Set type to 2 for ZIP to County
    url = f"https://www.huduser.gov/hudapi/public/usps?type={type}&query={zip_code}"
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjQ3NTkxODc3ZTAxM2FjZjhhMzUzYTY0YzcxOGY3MGIyYzljMWVhYjBjOTliNWE0NzIzYmE0ZDBiYmZjNDhkOGYxMGZiMDg1NGIyM2Q3ZWU3In0.eyJhdWQiOiI2IiwianRpIjoiNDc1OTE4NzdlMDEzYWNmOGEzNTNhNjRjNzE4ZjcwYjJjOWMxZWFiMGM5OWI1YTQ3MjNiYTRkMGJiZmM0OGQ4ZjEwZmIwODU0YjIzZDdlZTciLCJpYXQiOjE2OTIwMzQ4ODMsIm5iZiI6MTY5MjAzNDg4MywiZXhwIjoyMDA3NjU0MDgzLCJzdWIiOiI1NjAxNSIsInNjb3BlcyI6W119.JacEPIzzNZDQvk_0STKfTT-JuRDsVYW3ERKfR18-EcUpH5H_znFMirmivU4TQ3FKEZhDT0GK9AMS_g6hUGRB0Q"
    
    headers = {"Authorization": "Bearer {0}".format(token)}

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        st.error("Failed to fetch FIPS code")
        return []

    response_data = response.json()
    results = response_data["data"]["results"]
    fips_codes = [result["geoid"][:5] for result in results] # Extracting the first 5 characters of geoid for county FIPS code

    return fips_codes


@st.cache_data
def load_data(limit=100000):
    # Endpoint url
    url = 'https://data.cdc.gov/resource/n8mc-b4w4.json'
    
    # Add query parameter for limiting results
    params = {'$limit': limit}
    
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        # Convert 'county_fips_code' to string
        df['county_fips_code'] = df['county_fips_code'].astype(str)

        # Replace 'NA' with NaN and remove commas
        df['county_fips_code'] = df['county_fips_code'].replace('NA', float('nan')).str.replace(',', '')

        # Convert to float
        df['county_fips_code'] = df['county_fips_code'].astype(float)
        
    

        return df
    
    else:
        st.error("Failed to load data")
        return pd.DataFrame()

def plot_county_cases(df, fips_codes):
    for county_fips_code in fips_codes:
        specific_county = df[df['county_fips_code'] == float(county_fips_code)]
        st.write(specific_county)

        if specific_county.empty:
            st.write(f"No data found for county_fips_code: {county_fips_code}")
            continue

        monthly_counts = specific_county.groupby('case_month').size()
        if monthly_counts.empty:
            st.write(f"No monthly case data found for county_fips_code: {county_fips_code}")
            continue

        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(monthly_counts.index, monthly_counts.values, marker='o', color='red')

        ax.set_xlabel('Month', fontsize=14)
        ax.set_ylabel('Number of Cases', fontsize=14)
        ax.set_title(f'Number of Cases per Month for County: {county_fips_code}', fontsize=16)
        ax.grid(True)

        st.pyplot(fig)

df = load_data()

zip_code = st.text_input("Enter a ZIP code:")

if zip_code:
    fips_codes = find_fips(zip_code)
    if fips_codes:
        plot_county_cases(df, fips_codes)
