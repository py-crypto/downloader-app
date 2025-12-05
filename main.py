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
		
	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(url, download=False)  # do NOT download yet

	# 'formats' key contains a list of all formats
	formats = info.get("formats", [])

	safe_formats = [
	    f for f in formats
	    if f['vcodec'] != 'none' and f['acodec'] != 'none' and f['ext'] == 'mp4'
	]
	
	for f in safe_formats:
	    st.success(f"ID: {f['format_id']}, Resolution: {f.get('resolution')}, Format: {f['ext']}")
