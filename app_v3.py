# Final Enhanced Version with Requirements 1, 2, 3 Implemented

#Importing the data
import streamlit as st #For creating interactive web app
import pandas as pd #For loading and manipulating the NYC Restaurants data
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

@st.cache_data #Caches the data to improve performance. This prevents re-downloading the data on every page reload.
def load_data():
    url = "https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv?accessType=DOWNLOAD" #Loads the inspection dataset directly from NYC Open Data.
    df = pd.read_csv(url)
    df = df[['DBA', 'BORO', 'CUISINE DESCRIPTION', 'INSPECTION DATE',
             'VIOLATION DESCRIPTION', 'CRITICAL FLAG', 'GRADE', 'SCORE', 'ZIPCODE']] #selecting only relevant columns needed for analysis and display.
    df.dropna(subset=['DBA', 'GRADE'], inplace=True) #Removes rows where the restaurant name or grade is missing.
    df['INSPECTION DATE'] = pd.to_datetime(df['INSPECTION DATE'], errors='coerce') #Converts the inspection date to datetime format and drops rows where it's invalid.
    df.dropna(subset=['INSPECTION DATE'], inplace=True)
    df['DBA'] = df['DBA'].str.title() #Capitalizes the restaurant names consistently.
    return df #Returns the cleaned dataframe.

#Helper Functions:
def search_restaurants(df, name=None, zip_code=None): #Filters data based on optional name and zip code inputs.
    if name:
        df = df[df['DBA'].str.contains(name, case=False, na=False)] #Filters rows where restaurant name contains the input text
    if zip_code:
        df = df[df['ZIPCODE'] == int(zip_code)] #Filters by exact zip code.
    return df.sort_values(by='INSPECTION DATE', ascending=False).head(20) #Sorts by latest inspection date and returns the top 20 recent records.

def menu_driven_selection(df, cuisine=None, grade=None, critical=None): #Allows filtering by cuisine, grade and critical flag as per user selection.
    if cuisine:
        df = df[df['CUISINE DESCRIPTION'] == cuisine]
    if grade:
        df = df[df['GRADE'] == grade]
    if critical == "Critical":
        df = df[df['CRITICAL FLAG'] == "Critical"]
    elif critical == "Not Critical":
        df = df[df['CRITICAL FLAG'] == "Not Critical"]
    return df.sort_values(by='SCORE').head(20) #Shows top 20 restaurants with lowest score (best food safety compliance)

def rename_columns_for_display(df): #Renaming all columns for display, improving the readability of column headers for the end user.
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
    st.set_page_config(page_title="NYC Restaurant Inspector", layout="wide") #Sets the title and full-width layout.
    df = load_data() #Loads the cached data

    #Sidebar explanation: Permanent definitions that is common to all tabs.
    with st.sidebar: 
        #Rendering descriptive text using markdown format.
        st.markdown("""
        ### 🏅 Grade Details:
        - **A**: 0–13 violation points (Best)
        - **B**: 14–27 points
        - **C**: 28+ points
        - **P/Z**: Pending / Not graded

        ### 📊 Score Details:
        - Lower score = Better food safety compliance
        - 0–13 = A grade

        ### 🔴 Critical Flag Details:
        - **Critical**: 🚨 Major health risk
        - **Not Critical**: ⚠️ Minor issues
        - **Blank**: No issue recorded
        """)

    #Tab Layout:
    tab1, tab2, tab3, tab4 = st.tabs([
        "\U0001F4D8 Project Overview", 
        "\U0001F50D Search Restaurants", 
        "\U0001F37D️ Explore by Cuisine & Grade",
        "📊 Visual Insights"
    ])

    #Tab 1: Project Overview: Describes problem statement, Data Source Details and what this app does.
    with tab1:
        st.title("\U0001F4CA NYC Restaurant Inspection Explorer")
        st.markdown("""
        ### \U0001F4FE Problem Statement  
        This app helps users explore NYC restaurant inspection results to make safer dining decisions.

        ### \U0001F4C2 Dataset Source  
        [NYC Open Data – Restaurant Inspection Results](https://data.cityofnewyork.us/Health/Restaurant-Inspection-Results/43nn-pn8j)

        ### \U0001F3AF App Features  
        - Search by restaurant name and ZIP code  
        - Explore by cuisine type and inspection grade  
        - See latest inspection scores, grades, and violations  
        """)

    #Tab 2: Search Resturants, allowing searching by name or ZIP using user-friendly widgets.
    with tab2:
        st.title("\U0001F50D Search by Restaurant Name & ZIP Code")
        restaurant_list = sorted(df['DBA'].dropna().unique()) #Gets all unique restaurant names, removes NaN and sorts them alphabetically.
        name = st.selectbox("Select Restaurant Name", options=[""] + restaurant_list) #To let user pick a restaurant name, adds a blank default option to nothing is pre-selected.
        zip_code = st.text_input("Enter ZIP Code (optional)") #Text input where user can optionally enter a ZIP code to narrow down results.

        #Logic to trigger Search:
        if st.button("Search"): #When search button is clicked.
            results = search_restaurants(df.copy(), name, zip_code) #Calls the search_restaurants() function, passing a copy of dataframe along with name and ZIP code input, returning top results.
            if not results.empty: #To check if search returned any results.
                st.success(f"Top {len(results)} results for '{name}'") #Displays a subheading showing the restaurant name (formatted with title() to make it pretty).
                display_df = rename_columns_for_display(results) #Renames columns to user-friendly headers using the helper function.
                st.dataframe(display_df[['Restaurant Name', 'Borough', 'Inspection Date', 'Grade', 'Score', 'Critical Issue', 'Violation Details']]) #Displays the search result table.
                csv = display_df.to_csv(index=False).encode('utf-8') #Converts the table to CSV and offers it as a downloadable file.
                st.download_button("Download Results as CSV", csv, "filtered_results.csv", "text/csv")
            else: #If no match is found, show a warning message.
                st.warning("No matching records found.")

    with tab3:
        st.title("\U0001F37D️ Filter by Cuisine, Grade & Critical Flag") #Displays the title at the top of Tab 3.

        cuisine = st.selectbox("Select Cuisine Type", options=sorted(df['CUISINE DESCRIPTION'].dropna().unique())) #Dropdown for selecting a cuisine type from all unique available cuisines.
        unique_grades = sorted(df['GRADE'].dropna().unique())
        default_grade = 'A' if 'A' in unique_grades else unique_grades[0]
        grade = st.radio("Select Inspection Grade", options=unique_grades, index=unique_grades.index(default_grade)) #radio buttons to select a grade (A, B, C, etc.). The first one (index=0) is selected by default.

        critical_choice = st.radio("Select Critical Flag", options=["All", "Critical", "Not Critical"], index=0) #Another radio group to choose between: All restaurants, Only those with critical violations, Only those without critical violations

        filtered = menu_driven_selection(df.copy(), cuisine, grade, critical_choice) #Calls the filtering function with selected inputs & Returns a filtered DataFrame of restaurants based on chosen filters.
        if not filtered.empty: #Checks if the filter returns any restaurants.
            st.success(f"Top {len(filtered)} restaurants with grade '{grade}' for '{cuisine}' cuisine")
            display_df = rename_columns_for_display(filtered) #Renames columns for better display.
            st.dataframe(display_df[['Restaurant Name', 'Borough', 'Inspection Date', 'Grade', 'Score', 'Critical Issue', 'Violation Details']]) #Shows a clean table with the relevant columns.
            csv = display_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Filtered Cuisine Results", csv, "cuisine_filtered.csv", "text/csv") #Adds a download button for the filtered data.
        else:
            st.warning("No records found for selected filters.") #Displays a warning if no data matches the filters.

    #Visual Insights with Matplotlib:
    # with tab4:
    #     st.title("📊 Visual Insights")

    #     col1, col2 = st.columns(2) #Used to show charts side-by-side.

    #     with col1:
    #         st.subheader("Top 10 Cuisine Types")
    #         top_cuisines = df['CUISINE DESCRIPTION'].value_counts().head(10) #Counts how many times each cuisine shows up and takes the top 10.
    #         fig1, ax1 = plt.subplots()
    #         sns.barplot(y=top_cuisines.index, x=top_cuisines.values, ax=ax1, palette='Set2') #Creates horizontal or vertical bar charts.
    #         ax1.set_xlabel("Number of Inspections")
    #         ax1.set_ylabel("Cuisine Type")
    #         ax1.set_title("Top 10 Most Inspected Cuisines")
    #         st.pyplot(fig1) #Renders the matplotlib chart in Streamlit.
 
    #     with col2:
    #         st.subheader("Violations by Borough")
    #         boroughs = df['BORO'].value_counts()
    #         fig2, ax2 = plt.subplots()
    #         sns.barplot(x=boroughs.index, y=boroughs.values, ax=ax2, palette='Set1')
    #         ax2.set_ylabel("Number of Inspections")
    #         ax2.set_xlabel("Borough")
    #         ax2.set_title("Inspections by Borough")
    #         st.pyplot(fig2)


    # tab4 = st.tabs(["📈 Visualizations"])[0]
    # #Visual Insights with Plotly
    
    with tab4:
        st.title("📊 Visual Insights")

        st.markdown("### 🍽️ Top 15 Cuisine Types by Inspection Count")
        top_cuisines = df['CUISINE DESCRIPTION'].value_counts().nlargest(15).reset_index()
        top_cuisines.columns = ['Cuisine Type', 'Number of Inspections']

        fig1 = px.bar(
            top_cuisines,
            x='Cuisine Type',
            y='Number of Inspections',
            color='Number of Inspections',
            color_continuous_scale='Viridis',
            title="Top 15 Cuisine Types",
        )
        fig1.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("### 🗺️ Violations by Borough")
        borough_violations = df['BORO'].value_counts().reset_index()
        borough_violations.columns = ['Borough', 'Number of Violations']

        fig2 = px.pie(
            borough_violations,
            names='Borough',
            values='Number of Violations',
            title="Violations Distribution by Borough",
            hole=0.4  # for donut-style chart
        )
        st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main()
