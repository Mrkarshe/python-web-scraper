import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# Page Configuration
st.set_page_config(page_title="Data Scraper App", page_icon="🚀", layout="wide")

st.title("🚀 Python Web Scraper Dashboard")
st.write("Turn your script into a local web app! Click the button below to fetch live data without touching the terminal code.")

# Action Button
if st.button("Run Scraper & Generate Data"):
    with st.spinner("Fetching live data from the web..."):
        URL = "https://news.ycombinator.com/"
        response = requests.get(URL, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            titles = soup.find_all('span', class_='titleline')
            
            data = []
            scan_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for item in titles[:10]:
                title_text = item.get_text()
                link = item.find('a')['href'] if item.find('a') else "N/A"
                data.append({
                    "Title": title_text,
                    "Link": link,
                    "Scraped At": scan_time
                })
                
            df = pd.DataFrame(data)
            
            st.success(f"Successfully extracted {len(data)} records!")
            
            # Display interactive table in the app
            st.dataframe(df, use_container_width=True)
            
            # Add a download button for the CSV file
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV Report",
                data=csv_data,
                file_name="scraped_output.csv",
                mime="text/csv"
            )
        else:
            st.error(f"Failed to connect. Status code: {response.status_code}")
