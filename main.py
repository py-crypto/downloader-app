import streamlit as st
import yt_dlp
import os
from urllib.parse import urlparse
import time

st.set_page_config(page_title="Universal Video Downloader", layout="centered")

# ----------------------------------
# Title
# ----------------------------------
st.title("📥 Universal Video Downloader")
st.write("Download YouTube, Instagram, Facebook, Twitter videos")
st.warning("⚠️ Only download videos that you have permission to use. Respect copyright and platform policies.")

# ----------------------------------
# User Input
# ----------------------------------
url = st.text_input("Enter Video URL (YouTube / Instagram / Facebook / Twitter)")

quality = st.selectbox(
    "Select Video Quality",
    ["best", "720p", "360p"]
)

# Safe progressive formats (no ffmpeg needed)
format_map = {
    "best": "best[ext=mp4][vcodec!=none][acodec!=none]",
    "720p": "22/best[height<=720][ext=mp4][vcodec!=none][acodec!=none]",
    "360p": "18/best[height<=360][ext=mp4][vcodec!=none][acodec!=none]",
}

# ----------------------------------
# Cleanup function (DELETE FILES)
# ----------------------------------
def cleanup_files():
    for f in os.listdir():
        if f.startswith("downloaded") or f.endswith(".mp4") or f.endswith(".part"):
            try:
                os.remove(f)
            except:
                pass

# ----------------------------------
# Progress Hook with MB display
# ----------------------------------
def make_hook(progress_text, progress_bar):
    def hook(d):
        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
            # Calculate fraction for progress bar
            fraction = min(max(float(downloaded) / float(total), 0.0), 1.0)
            progress_bar.progress(fraction)
            
            # Convert bytes to MB for display
            downloaded_mb = downloaded / (1024 * 1024)
            total_mb = total / (1024 * 1024)
            progress_text.text(f"Downloaded: {downloaded_mb:.2f} MB / {total_mb:.2f} MB")
            
            time.sleep(0.01)
    return hook

# ----------------------------------
# Download Logic with safe cleanup
# ----------------------------------
if st.button("Download"):

    if url.strip() == "":
        st.error("Please enter a valid URL.")
        st.stop()

    progress_bar = st.progress(0)
    progress_text = st.empty()  # for MB display
    temp_filename = "downloaded.%(ext)s"

    ydl_opts = {
        "format": format_map[quality],
        "outtmpl": temp_filename,
        "progress_hooks": [make_hook(progress_text, progress_bar)],
    }

    try:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                original_filename = ydl.prepare_filename(info)

                # Create clean filename from title
                title = info.get("title", "video").replace("/", "_").replace("\\", "_")
                final_filename = f"{title}.mp4"

                # Rename downloaded file
                os.rename(original_filename, final_filename)

                # Download button
                with open(final_filename, "rb") as f:
                    st.download_button(
                        label="Download Video",
                        data=f,
                        file_name=final_filename,
                        mime="video/mp4"
                    )

                st.success("Download ready!")

                # Show thumbnail AFTER download
                if "thumbnail" in info:
                    st.image(info["thumbnail"], caption="Video Thumbnail", width=300)

        finally:
            # Cleanup temp and partial files even if download is interrupted
            cleanup_files()

    except Exception as e:
        st.error("Please enter a valid URL or try after some time")

