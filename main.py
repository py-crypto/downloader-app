#frontend
import requests as re
import streamlit as st

st.set_page_config(page_title="YouTube Video Downloader", layout="centered")
st.title("YouTube Video Downloader")


#takes input field

yt_link=st.text_input('Enter the url')
backend='https://backend-donwloader-production.up.railway.app'


def list_format():
	payload={'url':yt_link}
	response=re.post(url=f'{backend}/get_format',json=payload)
	avl_formats=response.json()
	return avl_formats

def download_vid():
		payload2={'url':yt_link,'format_id':format_id}
		response2=re.post(f'{backend}/download',json=payload2)
		file_name=response2.json().get('file_name',' ')
		download_url=(f'{backend}/download_file?file_name={file_name}')
		st.markdown(f"<a href='{download_url}' download='{file_name}'>📥 Click here to download</a>",unsafe_allow_html=True)
		

if yt_link:
	avl_formats=list_format()
	req_format=st.selectbox('Enter the required format',avl_formats.keys())
	if st.button('Download video'):
		with st.spinner('downloading video'):
			format_id=avl_formats.get(req_format,'480')
			download_vid()

			
	
