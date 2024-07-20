import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from googlesearch import search

def find_lyrics_link(query):
   
    search_results = search(query, num_results=10)
    
    for result in search_results:
        if 'genius.com' in result or 'azlyrics.com' in result or 'lyrics.com' in result:
            return result
    
    return "No relevant lyrics link found."


def format_artist_title(artist, title):
    formatted_artist = artist.replace(' ', '-')
    formatted_title = title.replace(' ', '-')
    return formatted_artist, formatted_title

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def clean_lyrics(lyrics):
    lines = lyrics.split('\n')
    cleaned_lines = []
    for line in lines:
        if re.match(r'\[.*?\]', line):
            cleaned_lines.append('')
        else:
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def extract_data(url, class_name=None, data_attr=None, output_file='output.txt'):
    print(url)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    if class_name:
        elements = soup.find_all(class_=class_name)
    elif data_attr:
        elements = soup.find_all(attrs={data_attr: "true"})
    else:
        print("Either class_name or data_attr must be provided.")
        return

    if not elements:
        print("No elements found with the specified class or data attribute.")
        return

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for element in elements:
                text = element.get_text(separator='\n', strip=True)
                cleaned_text = clean_lyrics(text)
                file.write(cleaned_text + '\n\n')
        print(f"Data has been saved to {output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}")

csv_file = 'output_lyricss.csv'
output_dir = 'output_lyrics'  
class_name = "Lyrics__Container-sc-1ynbvzw-1 kUgSbL"
data_attr = "data-lyrics-container"

df = pd.read_csv(csv_file)

for index, row in df.iterrows():
    artist = row['Artist(s)']
    title = row['Title']
    
    formatted_artist, formatted_title = format_artist_title(artist, title)
    name = re.sub(r'"', '', formatted_title)
    query = f'{formatted_artist} {formatted_title} lyrics genius'
    url = find_lyrics_link(query)
    
    
    output_file = os.path.join(output_dir, f"{name}.txt")
    
    extract_data(url, class_name=class_name, data_attr=data_attr, output_file=output_file)
