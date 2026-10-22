import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# Target website (Hacker News tech blog index)
URL = "https://news.ycombinator.com/"
print("[*] Scraping data from target source...")

try:
    response = requests.get(URL, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract titles and links
        titles = soup.find_all('span', class_='titleline')
        
        data = []
        scan_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for item in titles[:10]: # Grab top 10 items
            title_text = item.get_text()
            link = item.find('a')['href'] if item.find('a') else "N/A"
            data.append({
                "Title": title_text,
                "Link": link,
                "Scraped At": scan_time
            })
            
        # Convert data into a Pandas DataFrame
        df = pd.DataFrame(data)
        
        # Save to a CSV file (ready for client delivery)
        filename = "scraped_output.csv"
        df.to_csv(filename, index=False)
        
        print(f"\n[+] Success! Extracted {len(data)} records.")
        print(f"[+] Data successfully saved to spreadsheet: {filename}")
        print("\n--- Preview of Extracted Data ---")
        print(df.head())
        
    else:
        print(f"[-] Failed to connect. Status code: {response.status_code}")

except Exception as e:
    print(f"[-] An error occurred: {e}")
