import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
# Set page config
st.set_page_config(page_title="Signup Analysis", layout="wide")

# Add custom CSS for sticky header (dark theme compatible)
st.markdown("""
    <style>
        div[data-testid="stVerticalBlock"] > div:has(div.stSelectbox) {
            position: sticky;
            top: 0;
            background-color: #0e1117; /* Streamlit dark theme background */
            z-index: 999;
            padding: 1rem 0;
            border-bottom: 1px solid #333;
        }
        .stSelectbox {
            background-color: #262730 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Signup Analysis Dashboard")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
data2 = pd.read_csv('signers.csv')


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Read the CSV file
@st.cache_data
def load_data2():
    print("Starting to load data...")
    # Read CSV without header and assign column names
    df = pd.read_csv('signers.csv', header=None, 
                     names=['id', 'status', 'organization', 'language', 'zipcode', 'signup_date'])
    
    print("CSV loaded. First few rows:")
    print(df.head())
    print("\nColumn names:", df.columns.tolist())
    
    # Filter out rows where signup_date doesn't match the expected format
    def is_valid_date(date_str):
        try:
            pd.to_datetime(date_str, format='%m/%d/%Y %H:%M')
            return True
        except:
            return False
    
    # Filter the dataframe
    df = df[df['signup_date'].apply(is_valid_date)]
    print(f"\nFiltered out {len(df)} valid rows")
    
    # Convert signup_date to datetime with explicit format
    df['signup_date'] = pd.to_datetime(df['signup_date'], format='%m/%d/%Y %H:%M')
    print("\nSuccessfully converted dates")
    
    # Extract month and year
    df['month_year'] = df['signup_date'].dt.to_period('M')
    return df

st.text('yikes markdown signers.csv loaded successfully with length: ' + str(len(data2)))

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

print("About to load data...")
df = load_data2()
print("Data loaded successfully!")


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)

# Add a simple Plotly chart
df_plotly = pd.DataFrame({
    'x': np.arange(10),
    'y': np.random.randint(1, 20, 10)
})
fig = px.line(df_plotly, x='x', y='y', title='Simple Plotly Line Chart')
st.plotly_chart(fig)