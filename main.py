import streamlit as st
import yt_dlp

st.title("YouTube Downloader")

url = st.text_input("Enter YouTube URL:")

if st.button("Download"):
    st.info("Downloading...")

    ydl_opts = {
        "format": "91/92/93/18/94",  # pick progressive formats
        "outtmpl": "%(title)s.%(ext)s",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        st.success("Download complete!")
    except Exception as e:
        st.error(f"Error: {e}")
