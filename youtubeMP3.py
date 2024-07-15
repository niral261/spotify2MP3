from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pathlib import Path
import yt_dlp as youtube_dl
import pandas as pd
import os

def create_directory(directory):
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory '{directory}' created successfully.")
    except OSError as e:
        print(f"Error creating directory '{directory}': {e}")

def DownloadVideosFromIds(lov):
    RAPCHIK_SONGS = str(os.path.join(Path.home(), "Downloads/songs"))
    create_directory(RAPCHIK_SONGS)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': RAPCHIK_SONGS + '/%(title)s.%(ext)s',
        'ffmpeg_location': "C:/Users/Nishi Ajmera/ffmpeg-2024-06-24-git-6ec22731ae-full_build/bin",
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download(lov)
        except youtube_dl.utils.DownloadError as e:
            print(f"Error downloading: {e}")

def GetVideoUrl(query):
    print(f"Getting video id for: {query}")
    BASIC = "http://www.youtube.com/results?search_query="
    URL = BASIC + query.replace(" ", "+")
    
    session = HTMLSession()
    try:
        response = session.get(URL)
        response.html.render(sleep=1)
        
        soup = BeautifulSoup(response.html.html, "html.parser")
        result = soup.find('a', id="video-title")
        
        if result:
            video_id = result['href'].split('/watch?v=')[1]
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            return None
    except Exception as e:
        print(f"Error fetching video URL for '{query}': {e}")
        return None

def DownloadVideosFromTitles(songs):
    RAPCHIK_SONGS = str(os.path.join(Path.home(), "Downloads/songs"))
    create_directory(RAPCHIK_SONGS)
    
    existing_songs = set(os.path.splitext(f)[0] for f in os.listdir(RAPCHIK_SONGS) if os.path.isfile(os.path.join(RAPCHIK_SONGS, f)))
    songs_to_download = [song for song in songs if song not in existing_songs]
    
    if not songs_to_download:
        print("All songs are already downloaded in the songs folder.")
        return
    
    urls = []
    for song in songs_to_download:
        video_url = GetVideoUrl(song)
        if video_url:
            urls.append(video_url)
    
    if urls:
        print(f"Found {len(urls)} valid video URLs. Downloading songs 🎶")
        DownloadVideosFromIds(urls)
    else:
        print("No valid video URLs found to download")

def main():
    # Construct the absolute path for the CSV file
    csv_path = os.path.join(os.getcwd(), 'songs.csv')  # Use absolute path
    
    print(f"Looking for CSV file at: {csv_path}")
    
    try:
        # Read the CSV file
        data = pd.read_csv(csv_path)
        songs = data['song names'].tolist()
        
        print(f"Found {len(songs)} songs in CSV file.")
        
        # Print the list of songs to verify
        print("Songs list:", songs)
        
        # Proceed to download the songs
        DownloadVideosFromTitles(songs)
    except FileNotFoundError:
        print(f"Error: '{csv_path}' not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: '{csv_path}' is empty or malformed.")

if __name__ == '__main__':
    main()
