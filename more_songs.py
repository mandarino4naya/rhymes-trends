import pandas as pd
import requests
import os

# Load the CSV file with the artists
artists_file_path = '3000_artist.csv'
artists_df = pd.read_csv(artists_file_path)
print("Artists CSV loaded successfully. Columns are:", artists_df.columns)

# Get the list of artist names
artist_names = artists_df['name'].dropna().tolist()

# Load the CSV file with the songs to exclude
excluded_songs_file_path = 'billboard_year_end_hot_100_singles_1993_2023.csv'
excluded_songs_df = pd.read_csv(excluded_songs_file_path, quotechar='"', skipinitialspace=True)
print("Excluded songs CSV loaded successfully. Columns are:", excluded_songs_df.columns)

excluded_songs = set(excluded_songs_df['Title'].str.strip().str.lower())
print(f"Number of excluded songs: {len(excluded_songs)}")

# Genius API token
GENIUS_API_TOKEN = 'USE YOUR TOKEN'

# Get artist object from Genius API
def request_artist_info(artist_name, page):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch artist info: {response.status_code}")
        print(response.text)
    return response

# Get Genius.com song URLs from artist object
def request_song_url(artist_name, song_cap):
    page = 1
    songs = []
    
    while len(songs) < song_cap:
        response = request_artist_info(artist_name, page)
        try:
            json_response = response.json()
        except ValueError:
            print("Error parsing JSON response")
            return []
        
        if 'response' not in json_response:
            print(f"Unexpected response format: {json_response}")
            return []

        # Collect up to song_cap song objects from artist
        song_info = [hit for hit in json_response['response']['hits'] if artist_name.lower() in hit['result']['primary_artist']['name'].lower()]
    
        # Collect song URLs from song objects
        for song in song_info:
            title = song['result']['title'].strip().lower()
            if len(songs) < song_cap and title not in excluded_songs:
                songs.append((song['result']['title'], song['result']['primary_artist']['name']))
            
        page += 1
        
    print(f'Found {len(songs)} songs by {artist_name}')
    return songs

# Fetch songs for each artist in the CSV file until we have 3000 unique songs
unique_songs = set()
song_list = []

for artist_name in artist_names:
    print(f"Processing artist: {artist_name}")
    songs = request_song_url(artist_name, 10)
    
    for title, artist in songs:
        if (title, artist) not in unique_songs:
            unique_songs.add((title, artist))
            song_list.append({'Title': title, 'Artist': artist})
        if len(unique_songs) >= 3000:
            break
    
    if len(unique_songs) >= 3000:
        break

# Save the list of unique songs to a CSV file
output_file = 'unique_songs.csv'
df = pd.DataFrame(song_list)
df.to_csv(output_file, index=False)
print(f"Collected {len(unique_songs)} unique songs. Saved to {output_file}.")