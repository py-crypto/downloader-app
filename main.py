import streamlit as st
import requests

BACKEND_URL = "https://backend-donwloader-production.up.railway.app/download"

st.set_page_config(page_title="Universal Downloader", layout="centered")

st.title("📥 Universal Video Downloader")

url = st.text_input("Enter Video URL")

if st.button("Download"):
    if not url:
        st.error("Please enter a valid URL!")
    else:
        try:
            with st.spinner("Downloading... Please wait."):
                response = requests.post(
                    BACKEND_URL,
                    json={"url": url},
                    timeout=600
                )

            if response.status_code == 200:
                file_name = response.headers.get("Content-Disposition", "video.mp4")
                file_data = response.content

                st.success("Download Complete!")

                st.download_button(
                    label="Click to Save File",
                    data=file_data,
                    file_name=file_name.replace("attachment; filename=", ""),
                    mime="video/mp4"
                )
            else:
                st.error(f"Backend Error: {response.text}")

        except Exception as e:
            st.error(f"Error: {e}")
