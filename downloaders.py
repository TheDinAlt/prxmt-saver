from __future__ import unicode_literals
import os
import logging
import yt_dlp


class Youtube():

    def __init__(self):
        def hook(d):
            if d['status'] == 'finished':
                print('Done downloading, now converting ...')

        self.ydl_audio_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': logging,
            'progress_hooks': [hook],
            'ffmpeg_location': "D:\\ffmpeg\\bin\\ffmpeg.exe",
            'outtmpl': './files/%(id)s.%(ext)s',
        }

        self.ydl_video_opts = {
            'format': "bv[height<=1080][vcodec^=avc]+ba[ext=m4a]",
            'logger': logging,
            'progress_hooks': [hook],
            'ffmpeg_location': "D:\\ffmpeg\\bin\\ffmpeg.exe",
            'outtmpl': './files/%(id)s.%(ext)s',
        }

    async def get_info(self, url: str):
        try:
            with yt_dlp.YoutubeDL(self.ydl_audio_opts) as ydl:
                r = ydl.extract_info(url=url, download=False)
                return r
        except Exception as e:
            print(e)

    async def download(self, id: str, type: str):
        try:
            if type == "video":
                with yt_dlp.YoutubeDL(self.ydl_video_opts) as ydl:
                    return ydl.download(id)
            elif type == "audio":
                with yt_dlp.YoutubeDL(self.ydl_audio_opts) as ydl:
                    return ydl.download(id)
        except Exception as e:
            print(e)
        

async def delete_file(name: str):
    try:
        await os.remove(f'./files/{name}')
    except Exception as e:
        print(e)
