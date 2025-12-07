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
            st.markdown(
                f"[Click here to download **{title}.mp4**]({file_url})",
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Download failed: {e}")
