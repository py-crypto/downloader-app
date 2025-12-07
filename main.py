import streamlit as st
import requests

BACKEND = "https://backend-donwloader-production.up.railway.app"

st.title("YouTube Video Downloader")

url = st.text_input("Enter YouTube URL")

if url:
    # Fetch available formats from backend
    with st.spinner("Fetching available formats..."):
        try:
            r = requests.post(f"{BACKEND}/formats", json={"url": url})
            r.raise_for_status()
            data = r.json()
            title = data.get("title", "video")
            formats = data.get("formats", [])
        except Exception as e:
            st.error(f"Failed to fetch formats: {e}")
            formats = []

    if formats:
        # Build selectbox options: "360p (mp4)"
        options = [f'{f["resolution"]}p ({f["ext"]})' for f in formats]
        selection = st.selectbox("Choose format", options)

        # Get the format_id for the selected option
        chosen_format = formats[options.index(selection)]["format_id"]

        if st.button("Download"):
            with st.spinner("Requesting backend to download..."):
                try:
                    # Request backend to download video
                    r = requests.post(f"{BACKEND}/download",
                                      json={"url": url, "format": chosen_format})
                    r.raise_for_status()
                    download_id = r.json()["download_id"]

                    # Generate the direct file link
                    file_url = f"{BACKEND}/get_file/{download_id}"

                    st.success("Download ready!")
                    st.markdown
