import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    url = "https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv?accessType=DOWNLOAD"
    df = pd.read_csv(url)
    df = df[['DBA', 'BORO', 'CUISINE DESCRIPTION', 'INSPECTION DATE',
             'VIOLATION DESCRIPTION', 'CRITICAL FLAG', 'GRADE', 'ZIPCODE']]
    df.dropna(subset=['DBA', 'GRADE'], inplace=True)
    df['INSPECTION DATE'] = pd.to_datetime(df['INSPECTION DATE'])
    return df

def search_restaurants(df, name=None, zip_code=None):
    filtered = df.copy()
    if name:
        filtered = filtered[filtered['DBA'].str.lower() == name.lower()]
    if zip_code:
        filtered = filtered[filtered['ZIPCODE'] == int(zip_code)]

    # Top 3 most recent inspections
    recent = filtered.sort_values(by='INSPECTION DATE', ascending=False).head(3)
    # All historical records sorted by date desc
    history = filtered.sort_values(by='INSPECTION DATE', ascending=False)
    return recent, history

def main():
    st.title("NYC Restaurant Inspection Search")

    df = load_data()

    # Dropdown with all unique restaurant names, sorted alphabetically
    restaurant_names = sorted(df['DBA'].dropna().unique())
    name = st.selectbox("Select restaurant name:", [""] + restaurant_names)

    zip_code = st.text_input("Enter ZIP code (optional):")

    if st.button("Search"):
        if name == "":
            st.warning("Please select a restaurant name.")
            return
        
        recent, history = search_restaurants(df, name, zip_code)

        if recent.empty:
            st.write("No matching records found.")
        else:
            st.subheader("Top 3 Recent Inspections")
            st.dataframe(recent[['DBA', 'BORO', 'CUISINE DESCRIPTION', 'INSPECTION DATE',
                                 'GRADE', 'CRITICAL FLAG', 'VIOLATION DESCRIPTION']])

            st.subheader("Historical Violation Records")
            st.dataframe(history[['DBA', 'BORO', 'CUISINE DESCRIPTION', 'INSPECTION DATE',
                                  'GRADE', 'CRITICAL FLAG', 'VIOLATION DESCRIPTION']])

if __name__ == "__main__":
    main()
