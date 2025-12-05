import streamlit as st
import yt_dlp
import os
import time

st.title('Vid downloader')
url=st.text_input('URL:')

#url='https://www.youtube.com/watch?v=hm8b1Gnw1Z4'
if st.button('download'):
	ydl_opts = {
        'list_formats':True,
    }
		
	with yt_dlp.YoutubeDL(ydl_opts) as yd1:
		info=yd1.extract_info(url)

st.text(info['formats'])
