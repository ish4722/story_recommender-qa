import streamlit as st
import requests
import base64
import google.generativeai as genai

# Spotify API credentials
CLIENT_ID = 'cc4a25cce13f4b3dbb91fc2e09f44870'  # Replace with your Client ID
CLIENT_SECRET = '3a9b7a2f0ca642e881805a890135f6ed'  # Replace with your Client Secret

# Step 1: Get Access Token
def get_access_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()
    }
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        st.error(f"Could not authenticate: {response.json()}")
        return None

# Step 2: Fetch Top Artists
def search_top_artists(token, limit=15):
    url = "https://api.spotify.com/v1/search"
    headers = {'Authorization': f'Bearer {token}'}
    params = {'q': 'genre:pop', 'type': 'artist', 'limit': limit}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['artists']['items']
    else:
        st.error(f"Error: {response.status_code} - {response.json()}")
        return []

# Step 3: Fetch Top Tracks
def get_top_tracks(token, artist_id, country='US', limit=10):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = {'Authorization': f'Bearer {token}'}
    params = {'country': country}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['tracks'][:limit]
    else:
        st.error(f"Error fetching top tracks: {response.status_code} - {response.json()}")
        return []

# Step 4: Fetch Lyrics
def get_lyrics_lyrics_ovh(artist, title):
    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('lyrics', 'Lyrics not found.')
    else:
        return 'Lyrics not found.'

# Main Streamlit App
st.title('Song Extractor')

# Step 1: Get Spotify access token
access_token = get_access_token()

if access_token:
    # Fetch top 15 artists
    top_artists = search_top_artists(access_token)

    if top_artists:
        st.subheader('Top Artists:')
        for artist in top_artists:
            artist_name = artist['name']
            artist_id = artist['id']
            st.write(f"Artist: {artist_name}")

            # Fetch top 10 tracks for the artist
            top_tracks = get_top_tracks(access_token, artist_id)
            refined_description_list=[]

            for track in top_tracks:
                track_name = track['name']
                st.write(f"Track: {track_name}")

                # Fetch the lyrics using Lyrics.ovh
                lyrics = get_lyrics_lyrics_ovh(artist_name, track_name)
                st.write(f"Lyrics for {track_name}: {lyrics[:500]}...")

                # Step 5: Generate song description using Google Gemini
                if lyrics:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(f"""
                    You are a music expert who analyzes song lyrics to provide a concise description of the song.
                    Artist Name: {artist_name}
                    Track Name: {track_name}
                    Lyrics:
                    {lyrics}
                    """)

                    if response and hasattr(response, 'candidates'):
                        candidate = response.candidates[0]
                        if hasattr(candidate, 'content'):
                            refined_description = candidate.content
                            st.write(f"Description for {track_name}: {refined_description}")
                            refined_description_list.append(refined_description)

                    else:
                        st.write(f"No description available for {track_name}.")
    def refined_discription_music():
        return refined_description_list