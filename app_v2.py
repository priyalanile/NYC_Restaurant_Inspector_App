#App Final is better version as of now!

import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    url = "https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv?accessType=DOWNLOAD"
    df = pd.read_csv(url)
    df = df[['DBA', 'BORO', 'CUISINE DESCRIPTION', 'INSPECTION DATE',
             'VIOLATION DESCRIPTION', 'CRITICAL FLAG', 'GRADE', 'SCORE', 'ZIPCODE']]
    df.dropna(subset=['DBA', 'GRADE'], inplace=True)
    df['INSPECTION DATE'] = pd.to_datetime(df['INSPECTION DATE'], errors='coerce')
    df.dropna(subset=['INSPECTION DATE'], inplace=True)
    df['DBA'] = df['DBA'].str.title()
    return df

def search_restaurants(df, name=None, zip_code=None):
    if name:
        df = df[df['DBA'].str.contains(name, case=False, na=False)]
    if zip_code:
        df = df[df['ZIPCODE'] == int(zip_code)]
    return df.sort_values(by='INSPECTION DATE', ascending=False).head(4)

def menu_driven_selection(df, cuisine=None, grade=None):
    if cuisine:
        df = df[df['CUISINE DESCRIPTION'] == cuisine]
    if grade:
        df = df[df['GRADE'] == grade]
    return df.sort_values(by='SCORE').head(20)

def rename_columns_for_display(df):
    return df.rename(columns={
        'DBA': 'Restaurant Name',
        'BORO': 'Borough',
        'INSPECTION DATE': 'Inspection Date',
        'GRADE': 'Grade',
        'SCORE': 'Score',
        'VIOLATION DESCRIPTION': 'Violation Details',
        'CRITICAL FLAG': 'Critical Issue'
    })

def main():
    st.set_page_config(page_title="NYC Restaurant Inspector", layout="wide")
    df = load_data()

    tab1, tab2, tab3 = st.tabs([
        "📘 Project Overview", 
        "🔍 Search Restaurants", 
        "🍽️ Explore by Cuisine & Grade"
    ])

    # Tab 1: Introduction
    with tab1:
        st.title("📊 NYC Restaurant Inspection Explorer")
        st.markdown("""
        ### 🧾 Problem Statement  
        This app helps users explore NYC restaurant inspection results to make safer dining decisions.

        ### 📂 Dataset Source  
        [NYC Open Data – Restaurant Inspection Results](https://data.cityofnewyork.us/Health/Restaurant-Inspection-Results/43nn-pn8j)

        ### 🎯 App Features  
        - Search by restaurant name and ZIP code  
        - Explore by cuisine type and inspection grade  
        - See latest inspection scores, grades, and violations  
        """)

        # Add Explanation of Grades and Scores
        #with st.expander("ℹ️ Grade & Score Meaning"):
        st.markdown("""
        ### 🏅 Grade Meaning:
        - **A**: Best. Restaurant has scored 0–13 violation points.
        - **B**: Restaurant has scored 14–27 violation points.
        - **C**: Restaurant has scored 28 or more violation points.
        - **P/Z**: Pending or not yet graded.

        ### 📊 Score Meaning:
        - A **lower score** means **better compliance** with food safety rules.
        - A score of **0–13** generally corresponds to an **A grade**.
        
        ### 🔴 Critical Flag Meaning:
        - **Critical**: 🚨 A violation that poses a serious health risk (e.g. improper food temperature, rodent activity). Must be addressed quickly.
        - **Not Critical**: ⚠️ A less serious issue (e.g. dirty walls or light bulbs without covers). Still needs fixing but not immediately dangerous.
        - **N/A or blank**: No violation was recorded for that inspection
                    
        """)

    # Tab 2: Search
    with tab2:
        st.title("🔍 Search by Restaurant Name & ZIP Code")

        # Add Explanation of Grades and Scores
        with st.expander("ℹ️ Grade, Score & Critical Flag Details"):
            st.markdown("""
            ### 🏅 Grade Meaning
            - **A**: Best. Restaurant has scored 0–13 violation points.
            - **B**: Restaurant has scored 14–27 violation points.
            - **C**: Restaurant has scored 28 or more violation points.
            - **P/Z**: Pending or not yet graded.

            ### 📊 Score Meaning
            - A **lower score** means **better compliance** with food safety rules.
            - A score of **0–13** generally corresponds to an **A grade**.
                        

             ### 🔴 Critical Flag Meaning:
            - **Critical**: 🚨 A violation that poses a serious health risk (e.g. improper food temperature, rodent activity). Must be addressed quickly.
            - **Not Critical**: ⚠️ A less serious issue (e.g. dirty walls or light bulbs without covers). Still needs fixing but not immediately dangerous.
            - **N/A or blank**: No violation was recorded for that inspection

            """)

        restaurant_list = sorted(df['DBA'].dropna().unique())
        name = st.selectbox("Select Restaurant Name", options=[""] + restaurant_list)
        zip_code = st.text_input("Enter ZIP Code (optional)")

        if st.button("Search"):
            results = search_restaurants(df.copy(), name, zip_code)
            if not results.empty:
                st.success(f"Top {len(results)} results for '{name}'")
                display_df = rename_columns_for_display(results)
                st.dataframe(display_df[['Restaurant Name', 'Borough', 'Inspection Date', 'Grade', 'Score', 'Critical Issue', 'Violation Details']])
            else:
                st.warning("No matching records found.")

    # Tab 3: Cuisine + Grade Menu
    with tab3:
        st.title("🍽️ Filter by Cuisine & Grade & Critical Flag")


        # Add Explanation of Grades and Scores
        with st.expander("ℹ️ Grade, Score & Critical Flag Details"):
            st.markdown("""
            ### 🏅 Grade Meaning
            - **A**: Best. Restaurant has scored 0–13 violation points.
            - **B**: Restaurant has scored 14–27 violation points.
            - **C**: Restaurant has scored 28 or more violation points.
            - **P/Z**: Pending or not yet graded.

            ### 📊 Score Meaning
            - A **lower score** means **better compliance** with food safety rules.
            - A score of **0–13** generally corresponds to an **A grade**.
                        
            ### 🔴 Critical Flag Meaning:
            - **Critical**: 🚨 A violation that poses a serious health risk (e.g. improper food temperature, rodent activity). Must be addressed quickly.
            - **Not Critical**: ⚠️ A less serious issue (e.g. dirty walls or light bulbs without covers). Still needs fixing but not immediately dangerous.
            - **N/A or blank**: No violation was recorded for that inspection

            """)

        cuisine = st.selectbox("Select Cuisine Type", options=sorted(df['CUISINE DESCRIPTION'].dropna().unique()))
        unique_grades = sorted(df['GRADE'].dropna().unique())
        default_grade = 'A' if 'A' in unique_grades else unique_grades[0]
        grade = st.radio("Select Inspection Grade", options=unique_grades, index=unique_grades.index(default_grade))

        filtered = menu_driven_selection(df.copy(), cuisine, grade)
        if not filtered.empty:
            st.success(f"Top {len(filtered)} restaurants with grade '{grade}' for '{cuisine}' cuisine")
            display_df = rename_columns_for_display(filtered)
            st.dataframe(display_df[['Restaurant Name', 'Borough', 'Inspection Date', 'Grade', 'Score', 'Critical Issue', 'Violation Details']])
        else:
            st.warning("No records found for selected filters.")



if __name__ == "__main__":
    main()