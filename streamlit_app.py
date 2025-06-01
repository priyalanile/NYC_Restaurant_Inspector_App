import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    url = "https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv?accessType=DOWNLOAD"
    df = pd.read_csv(url)
    df = df[['DBA', 'BORO', 'CUISINE DESCRIPTION', 'INSPECTION DATE',
             'VIOLATION DESCRIPTION', 'CRITICAL FLAG', 'GRADE', 'ZIPCODE']]
    df.dropna(subset=['DBA', 'GRADE'], inplace=True)
    df['INSPECTION DATE'] = pd.to_datetime(df['INSPECTION DATE'])
    return df

df = load_data()

st.title("NYC Restaurant Inspection Search")
name = st.text_input("Enter restaurant name:")
zip_code = st.text_input("Enter ZIP code (optional):")

if st.button("Search"):
    results = df.copy()
    if name:
        results = results[results['DBA'].str.contains(name, case=False, na=False)]
    if zip_code:
        results = results[results['ZIPCODE'] == int(zip_code)]
    results = results.sort_values(by='INSPECTION DATE', ascending=False).head(10)
    st.dataframe(results[['DBA', 'BORO', 'INSPECTION DATE', 'GRADE', 'CRITICAL FLAG', 'VIOLATION DESCRIPTION']])