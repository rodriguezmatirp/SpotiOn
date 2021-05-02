from bs4 import BeautifulSoup as bs
import requests, os
from pytube import YouTube
import urllib.request, re

def scrap_video(query):
    base_url = "https://www.youtube.com/results?search_query="
    query.replace(" ", "+")
    html = urllib.request.urlopen(base_url+query)
    x = re.search(r'watch\?v=(\S{11})', html.read().decode())
    if x != None:
        html = urllib.request.urlopen(base_url+query)
        vid_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
        return f'https://www.youtube.com/watch?v=' + vid_ids[0]
    return False

def download_video(query):
    video_id = scrap_video(query)
    if video_id:
        ytd = YouTube(url=video_id).streams.filter(progressive=True,file_extension='mp4').first()
        try:
            out_file,ext = ytd.download('Downloads/Videos').split('.')
        except Exception as err:
            return False
        return out_file
    else:
        return False

def download_audio(query):
    track_id = scrap_video(query)
    if track_id:
        ytd = YouTube(url=track_id).streams.filter(only_audio=True).first()
        print(ytd)
        try:
            out_file = ytd.download('Downloads/Songs')
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)

        except Exception as err:
            return False
        return base
    else:
        return False
