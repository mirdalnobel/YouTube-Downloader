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
    try:
        video = YouTube(url)
        return video
    except pytube.exceptions.RegexMatchError:
        st.error('Invalid URL.')
        return None
    except pytube.exceptions.VideoUnavailable:
        st.error('This video is unavailable.')
        return None

@st.cache
def get_stats(video):
    header = f'**{video.title}** *By: {video.author}*'
    thumbnail = load_thumbnail(video.thumbnail_url)
    info = f'Length: **{datetime.timedelta(seconds=video.length)}** \nViews: **{video.views:,}**'
    return header, thumbnail, info

def load_thumbnail(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img

def download_video(video, download_type):
    if download_type == 'Video and Audio (.mkv)':
        download_video_and_audio(video)
    elif download_type == 'Audio Only (.mp3)':
        download_audio(video)
    elif download_type == 'Video Only (.mp4)':
        download_video_only(video)

def download_video_and_audio(video):
    # Download and merge video and audio
    # ...

def download_audio(video):
    # Download audio only
    stream = video.streams.get_audio_only()
    filesize = round(stream.filesize / 1000000, 2)
    if st.button(f'Download Audio (~{filesize} MB)'):
        with st.spinner(f'Downloading {video.title} audio...'):
            stream.download(filename='audio')
            convert_mp3 = f'ffmpeg -i audio.mp4 Downloads/{re.sub("[^0-9a-zA-Z]+", "-", video.title)}.mp3'
            subprocess.run(convert_mp3, shell=True)
            os.remove('Downloads/audio.mp4')
        st.success(f'Finished Downloading {video.title} audio!')

def download_video_only(video):
    # Download video only
    # ...

st.title('YouTube Downloader')

url = st.text_input('Enter the URL of the YouTube video')

if url:
    video = get_video(url)
    if video:
        header, thumbnail, info = get_stats(video)
        st.header(header)
        st.image(thumbnail, width=750)
        st.write(info)

        download_type = st.radio(
            'Select the type of download you would like', [
                'Video and Audio (.mkv)',
                'Audio Only (.mp3)',
                'Video Only (.mp4)'
            ]
        )

        if st.button(f'Download {download_type}'):
            download_video(video, download_type)
            st.success(f'Finished Downloading {video.title}!')

