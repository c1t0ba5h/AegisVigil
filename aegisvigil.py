import requests
from bs4 import BeautifulSoup
import pandas as pd

# URLs to scrape
urls = [
    "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
    "https://thehackernews.com/search/label/Vulnerability",
    "https://www.exploit-db.com"
]

# Load the wordlist from the CSV (assumes wordlist is in the first column)
def load_wordlist(csv_file):
    try:
        df = pd.read_csv(csv_file, usecols=[0], header=None)
        wordlist = df[0].tolist()
        return wordlist
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

# Fetch HTML content from a given URL
def fetch_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

# Search the HTML content for matches from the wordlist
def search_content(html, wordlist):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text().lower()  # Convert to lowercase for case-insensitive matching
    matches = [word for word in wordlist if word.lower() in text]
    return matches

def main():
    # Path to the CSV file with the wordlist
    csv_file = "wordlist.csv"

    # Load the wordlist from the CSV file
    wordlist = load_wordlist(csv_file)
    if not wordlist:
        print("No words loaded from the CSV. Exiting.")
        return

    # Iterate over the URLs, fetch content, and search for matches
    for url in urls:
        print(f"\nChecking {url}...")
        html = fetch_html(url)
        if html:
            matches = search_content(html, wordlist)
            if matches:
                print(f"Found matches: {', '.join(matches)}")
            else:
                print("No matches found.")

if __name__ == "__main__":
    main()
