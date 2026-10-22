import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import datetime

st.set_page_config(page_title="Universal Web Scraper", page_icon="📊", layout="wide")

st.title("📊 Universal Commercial Web Scraper")
st.write("Paste any public website URL below to extract items, text, and links instantly.")

user_url = st.text_input("Enter Website URL:", "https://webscraper.io/test-sites/e-commerce/allinone")

if st.button("Extract Data"):
    if not user_url:
        st.warning("Please enter a URL!")
    else:
        with st.spinner("Scraping live website data..."):
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                response = requests.get(user_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Universal extraction: look for product cards, headings, or links with text
                    elements = soup.find_all(['a', 'h1', 'h2', 'h3', 'span', 'div'])
                    
                    data = []
                    scan_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    seen_texts = set()
                    
                    for el in elements:
                        text = el.get_text().strip()
                        # Filter for clean, readable text items (avoiding tiny snippets)
                        if text and len(text) > 4 and text not in seen_texts:
                            # Try to find an associated link
                            link_el = el.find('a') if el.name != 'a' else el
                            raw_link = link_el.get('href') if link_el and link_el.has_attr('href') else 'N/A'
                            link = urljoin(user_url, raw_link) if raw_link != 'N/A' else 'N/A'
                            
                            seen_texts.add(text)
                            data.append({
                                "Extracted Text / Title": text,
                                "Associated Link": link,
                                "Scraped At": scan_time
                            })
                            
                            if len(data) >= 30: # Limit to top 30 clean records
                                break
                                
                    if data:
                        df = pd.DataFrame(data)
                        st.success(f"Successfully extracted {len(data)} records!")
                        st.dataframe(df, use_container_width=True)
                        
                        csv_data = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download CSV Report",
                            data=csv_data,
                            file_name="universal_scraped_data.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("This page structure is heavily restricted or protected.")
                else:
                    st.error(f"Failed to connect. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
