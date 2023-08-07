from flask import Flask, jsonify, render_template
import pandas as pd

app = Flask(__name__)

def load_data():
    return pd.read_csv('geography.csv')

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