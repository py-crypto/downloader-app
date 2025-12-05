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
        "format": "96",  # MUST be a single progressive stream
        "outtmpl": "%(title)s.%(ext)s",
    }
		
	with yt_dlp.YoutubeDL(ydl_opts) as yd1:
		yd1.download([url])
	st.success('downloaded.')
