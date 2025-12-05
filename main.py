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

	# Print each format's details
	for f in formats:
		st.success(f"ID: {f['format_id']}, Ext: {f.get('ext')}, Resolution: {f.get('resolution')}, FPS: {f.get('fps')}, Audio: {f.get('acodec')}, Video: {f.get('vcodec')}")

