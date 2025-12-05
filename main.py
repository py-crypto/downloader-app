import streamlit as st
import yt_dlp
import os
import uuid
from urllib.parse import urlparse
import time

st.set_page_config(page_title="Universal Video Downloader", layout="centered")

st.title("📥 Universal Video Downloader")
st.write("Download YouTube, Instagram, Facebook, Twitter videos")
st.warning("⚠️ Only download videos you have permission to use.")

# ---------------------------
# Create a session-unique folder
# ---------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

SESSION_DIR = f"downloads_{st.session_state.session_id}"
os.makedirs(SESSION_DIR, exist_ok=True)

# ---------------------------
# Cleanup only user's folder
# ---------------------------
def cleanup_session():
    try:
        for f in os.listdir(SESSION_DIR):
            os.remove(os.path.join(SESSION_DIR, f))
    except:
        pass

# ---------------------------
# User Inputs
# ---------------------------
url = st.text_input("Enter Video URL (YouTube / Instagram / Facebook / Twitter)")
quality = st.selectbox("Select Video Quality", ["best", "720p", "360p"])

format_map = {
    "best": "best[ext=mp4][vcodec!=none][acodec!=none]",
    "720p": "22/best[height<=720][ext=mp4][vcodec!=none][acodec!=none]",
    "360p": "18/best[height<=360][ext=mp4][vcodec!=none][acodec!=none]",
}

# ---------------------------
# Download Progress Hook
# ---------------------------
def make_hook(progress_text, progress_bar):
    def hook(d):
        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
            fraction = min(max(float(downloaded) / float(total), 0.0), 1.0)
            progress_bar.progress(fraction)

            downloaded_mb = downloaded / (1024 * 1024)
            total_mb = total / (1024 * 1024)
            progress_text.text(f"Downloaded: {downloaded_mb:.2f} MB / {total_mb:.2f} MB")
    return hook

# ---------------------------
# Download Button
# ---------------------------
if st.button("Download"):

    if url.strip() == "":
        st.error("Please enter a valid URL.")
        st.stop()

    cleanup_session()  # clear old files for THIS user

    progress_bar = st.progress(0)
    progress_text = st.empty()

    temp_filename = f"{SESSION_DIR}/temp_%(id)s.%(ext)s"

    ydl_opts = {
        "format": format_map[quality],
        "outtmpl": temp_filename,
        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        },
        "progress_hooks": [make_hook(progress_text, progress_bar)],
    }


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            original = ydl.prepare_filename(info)

            title = info.get("title", "video").replace("/", "_").replace("\\", "_")
            final_file = f"{SESSION_DIR}/{title}.mp4"

            os.rename(original, final_file)

            with open(final_file, "rb") as f:
                st.download_button(
                    label="Download Video",
                    data=f,
                    file_name=f"{title}.mp4",
                    mime="video/mp4"
                )

            st.success("Download ready!")

            if "thumbnail" in info:
                st.image(info["thumbnail"], caption="Video Thumbnail", width=300)

    except Exception as e:
        st.error("Error downloading video. Please try a different link.")
        st.write(str(e))
