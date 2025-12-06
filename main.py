import streamlit as st
import requests

BACKEND = "https://backend-donwloader-production.up.railway.app"

st.title("Video Downloader")

url = st.text_input("Enter YouTube URL")
format = st.selectbox("Choose format", ["480p", "360p", "720p"], index=0)

if st.button("Download"):
    with st.spinner("Requesting backend..."):
        # Step 1 → send POST request
        r = requests.post(
            f"{BACKEND}/download",
            json={"url": url, "format": format}
        )

        if r.status_code != 200:
            st.error("Backend Error: " + r.text)
        else:
            download_id = r.json()["download_id"]

            # Step 2 → fetch actual file
            file_url = f"{BACKEND}/get_file/{download_id}"
            video_response = requests.get(file_url)

            if video_response.status_code == 200:
                st.success("Download Ready!")

                # Step 3 → Provide download button
                st.download_button(
                    label="Save Video",
                    data=video_response.content,
                    file_name="video.mp4",
                    mime="video/mp4"
                )
            else:
                st.error("Could not fetch the file.")
