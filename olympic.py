import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Function to inject custom CSS
def set_custom_css():
    st.markdown(
        """
        <style>
        .reportview-container {
            background: #4B0082; /* Dark purple background */
            color: white; /* Text color */
        }
        .sidebar .sidebar-content {
            background: #4B0082; /* Dark purple background for sidebar */
            color: white; /* Text color in sidebar */
        }
        .css-1u3izw2 {
            background: #4B0082; /* Purple background for header */
        }
        .css-1y4b62k {
            color: white; /* Text color for headers */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Set custom CSS
set_custom_css()

# List of CSV file names and their display names
file_mapping = {
    "Athens 2004": "Athens2004.csv",
    "Atlanta 1996": "Atlanta1996.csv",
    "Beijing 2022": "beijing2022.csv",
    "Lillehammer 1994": "Lillehammer1994.csv",
    "London 2012": "London2012.csv",
    "Nagano 1998": "Nagano1998.csv",
    "Paris 2024": "Paris2024.csv",
    "PyeongChang 2018": "PyeongChang2018.csv",
    "Rio 2016": "Rio2016.csv",
    "Salt Lake City 2002": "SaltLakeCity2002.csv",
    "Sochi 2014": "Sochi2014.csv",
    "Sydney 2000": "Sydney2000.csv",
    "Tokyo 2020": "Tokyo2020.csv",
    "Torino 2006": "Torino2006.csv",
    "Vancouver 2010": "Vancouver2010.csv"
}

# Streamlit app
st.sidebar.title("Olympics Data Dashboard")
selected_year = st.sidebar.selectbox("Select Olympic Year", list(file_mapping.keys()))

# Get the file name based on the selection
file_name = file_mapping[selected_year]

# Load and display data
try:
    df = pd.read_csv(file_name)

    # Main area content
    st.write(f"### Data for {selected_year}")
    st.dataframe(df)

    # Grouped Bar Chart
    st.write("### Medal Counts by Country")
    # Aggregate medal counts by country
    country_medals = df.groupby('NOC')[['Gold', 'Silver', 'Bronze']].sum().reset_index()

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(12, 8))
    width = 0.25  # Width of the bars
    countries = country_medals['NOC']
    x = range(len(countries))

    # Plot bars for each medal type
    ax.bar([i - width for i in x], country_medals['Gold'], width, label='Gold', color='gold')
    ax.bar(x, country_medals['Silver'], width, label='Silver', color='silver')
    ax.bar([i + width for i in x], country_medals['Bronze'], width, label='Bronze', color='#cd7f32')

    ax.set_xlabel('Country')
    ax.set_ylabel('Count')
    ax.set_title('Medal Counts by Country')
    ax.set_xticks(x)
    ax.set_xticklabels(countries, rotation=90)
    ax.legend()

    st.pyplot(fig)

    # Pie chart
    st.write("### Medal Distribution by Country")
    country_medals['Total'] = country_medals[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    fig = px.pie(country_medals, names='NOC', values='Total', title='Medal Distribution by Country')
    st.plotly_chart(fig)

except Exception as e:
    st.error(f"Error loading {file_name}: {e}")
