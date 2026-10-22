import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import datetime

st.set_page_config(page_title="Product & Price Scraper", page_icon="📊", layout="wide")

st.title("📊 Commercial Web Scraper & Price Tracker")
st.write("Extract structured product names, prices, and links into a clean spreadsheet for clients.")

# Default example: A public catalog or directory page
user_url = st.text_input("Enter Website URL:", "https://books.toscrape.com/")

if st.button("Extract Commercial Data"):
    if not user_url:
        st.warning("Please enter a URL!")
    else:
        with st.spinner("Scraping marketplace data..."):
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(user_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Target common product/item card structures
                    items = soup.find_all(['article', 'div'], class_=['product_pod', 'card', 'item'])
                    if not items:
                        # Fallback if specific classes aren't found
                        items = soup.find_all(['h3', 'h2'])
                        
                    data = []
                    scan_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    for item in items[:25]:
                        # Try to extract title/name
                        title_el = item.find(['a', 'h3', 'h2', 'span'])
                        title = title_el.get_text().strip() if title_el else "N/A"
                        
                        # Try to extract price if available
                        price_el = item.find(class_=['price', 'cost', 'amount'])
                        price = price_el.get_text().strip() if price_el else "Check Link"
                        
                        # Extract link
                        link_el = item.find('a')
                        raw_link = link_el.get('href') if link_el and link_el.has_attr('href') else 'N/A'
                        link = urljoin(user_url, raw_link) if raw_link != 'N/A' else 'N/A'
                        
                        if title and title != "N/A":
                            data.append({
                                "Item Name / Title": title,
                                "Price / Detail": price,
                                "Product Link": link,
                                "Extracted At": scan_time
                            })
                            
                    if data:
                        df = pd.DataFrame(data)
                        st.success(f"Successfully extracted {len(data)} commercial records!")
                        st.dataframe(df, use_container_width=True)
                        
                        csv_data = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Client Excel/CSV Report",
                            data=csv_data,
                            file_name="client_market_data.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("No structured items found. Try a different category URL.")
                else:
                    st.error(f"Failed to connect. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
