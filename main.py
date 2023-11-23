import datetime
import requests
import os
import re
import pytube
import subprocess
from pytube import YouTube
import streamlit as st
from PIL import Image
from io import BytesIO

def get_video(url):
    global video_found, video
    try:
        video = YouTube(url)
        video_found = True
    except pytube.exceptions.RegexMatchError:
        st.error('Invalid URL.')
        video_found = False
    except pytube.exceptions.VideoUnavailable:
        st.error('This video is unavailable')
        video_found = False
    return video

def load_thumbnail(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img

@st.cache
def get_stats(video):
    header = (f'**{video.title}**' 
            + f' *By: {video.author}*')
    thumbnail = load_thumbnail(video.thumbnail_url)
    info = (f'Length: **{datetime.timedelta(seconds=video.length)}** \n'
          + f'Views: **{video.views:,}**')
    return header, thumbnail, info

def download_audio(video):
    stream = video.streams.get_audio_only()
    filesize = round(stream.filesize / 1000000, 2)
    if st.button(f'Download Audio (~{filesize} MB)'):
        with st.spinner(f'Downloading {video.title}... Please wait to open any files until the download has finished'):
            stream.download(filename='audio')
            convert_to_mp3(video.title)
            os.remove('Downloads/audio.mp4')
        st.success(f'Finished Downloading {video.title}!')

def convert_to_mp3(title):
    convert_mp3 = f'ffmpeg -i Downloads/audio.mp4 Downloads/{re.sub("[^0-9a-zA-Z]+", "-", title)}.mp3'
    subprocess.run(convert_mp3, shell=True)

st.title('YouTube Downloader')

url = st.text_input('Enter the URL of the YouTube video')

if url:
    video = get_video(url)
    if video_found:
        header, thumbnail, info = get_stats(video)
        st.header(header)
        st.image(thumbnail, width=750)
        st.write(info)

        download_type = st.radio(
            'Select the type of download you would like', [
                'Video and Audio (.mkv)', 
                'Audio Only (.mp3)', 
                'Video Only (.mp4)']
        )

        if download_type == 'Video and Audio (.mkv)':
            # Your existing code for downloading video and audio

        elif download_type == 'Audio Only (.mp3)':
            download_audio(video)

        elif download_type == 'Video Only (.mp4)':
            # Your existing code for downloading video only
