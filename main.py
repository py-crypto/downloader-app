import streamlit as st
import yt_dlp
import os
import time

st.title('Vid downloader')
url=st.text_input('URL:')

#url='https://www.youtube.com/watch?v=hm8b1Gnw1Z4'
if st.button('download'):
	st.success('downloading...')
	ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",  
        "outtmpl": "%(title)s.%(ext)s",
        "merge_output_format": "mp4"
    }

		
	with yt_dlp.YoutubeDL(ydl_opts) as yd1:
		yd1.download([url])
	st.success('downloaded.')
