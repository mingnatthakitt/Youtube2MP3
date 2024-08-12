import streamlit as st
import yt_dlp
import os


st.title("Youtube2MP3")

url = st.text_input(label="Youtube2MP3", placeholder="Paste Youtube link here", label_visibility="collapsed")

ffmpeg_path = r'D:\ffmpeg-2024-07-10-git-1a86a7a48d-full_build\bin\ffmpeg.exe' 

def download_audio(url):
    output_dir = os.getcwd()
    ydl_opts = {
    'format': 'bestaudio/best',
    'ffmpeg_location': ffmpeg_path,  # Specify the path to your FFmpeg bin folder
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Save file in the current directory
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = info_dict.get('title', None)
        filename = os.path.join(output_dir, f"{title}.mp3")
        return filename

if st.button("Convert to MP3"):
    if url:
        try:
            mp3_file = download_audio(url)
            if mp3_file:
                with open(mp3_file, "rb") as file:
                    st.download_button(
                        label="Download MP3",
                        data=file,
                        file_name=os.path.basename(mp3_file),
                        mime="audio/mpeg"
                    )
        except Exception as e:
            st.error(f"An error occurred: {e}")