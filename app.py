from flask import Flask, jsonify, render_template
import pandas as pd
import requests

app = Flask(__name__)

# def load_data():
#     return pd.read_csv('geography.csv')

def load_data(limit = 100000):
    # Endpoint url
    url = 'https://data.cdc.gov/resource/n8mc-b4w4.json'
    
    # Add query parameter for limiting results
    params = {
        '$limit': limit,
        '$order': 'county_fips_code ASC'
    }
    
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
        print("Failed to load data")
        return pd.DataFrame()

def get_county_cases(county_fips_code):
    df = load_data()
    specific_county = df[df['county_fips_code'] == float(county_fips_code)]
    monthly_counts = specific_county.groupby('case_month').size()
    return monthly_counts.index.tolist(), monthly_counts.values.tolist()

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/data/<county_fips_code>')
def data(county_fips_code):
    months, cases = get_county_cases(county_fips_code)
    return jsonify(months=months, cases=cases)

if __name__ == "__main__":
    app.run(debug=True)