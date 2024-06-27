import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables
import os
import google.generativeai  as genai  # Corrected import path

from youtube_transcript_api import YouTubeTranscriptApi

# Configure API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initial prompt template for summarizing the video transcript
default_words = 250
prompt_template = f"""You are a YouTube video summarizer. You will take the transcript text and summarize the entire video, providing the important points within {{words}} words. Please provide the summary of the text given here: """

# Function to extract transcript data from YouTube videos
def extract_transcript_details(youtube_video_url, language_code='en'):
    try:
        video_id = youtube_video_url.split("=")[1]
        
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

# Function to generate summary using Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt.format(words=default_words) + transcript_text)
    return response.text

# Streamlit UI components
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")
words = st.number_input("How many words required for summary", min_value=1, value=default_words)
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        prompt = prompt_template.format(words=words)
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
