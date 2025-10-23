# In studybuddy/tools/youtube_tools.py (UPDATED TO USE RELIABLE LIBRARY)

from urllib.parse import urlparse, parse_qs
from langchain_core.tools import tool
from youtube_transcript_api import YouTubeTranscriptApi

def _get_video_id(url: str) -> str | None:
    """A robust way to get the video ID from any YouTube URL."""
    try:
        parsed_url = urlparse(url)
        if "youtu.be" in parsed_url.hostname:
            return parsed_url.path[1:]
        if "youtube.com" in parsed_url.hostname:
            if parsed_url.path == "/watch":
                return parse_qs(parsed_url.query)["v"][0]
            if parsed_url.path.startswith(("/embed/", "/v/")):
                return parsed_url.path.split("/")[2]
        return None
    except Exception:
        return None

@tool
def get_youtube_transcript(url: str) -> str:
    """
    Fetches the full English transcript for a given YouTube video URL.
    Uses the reliable youtube-transcript-api library.
    """
    video_id = _get_video_id(url)
    if not video_id:
        return "Error: Could not extract a valid YouTube video ID from the URL."

    try:
        # Get the transcript using the reliable library
        transcript_api = YouTubeTranscriptApi()
        transcript_list = transcript_api.fetch(video_id, languages=['en'])
        
        if not transcript_list:
            return "Error: No English transcript found for this video."
        
        # Extract just the text from each segment
        transcript_text = " ".join([segment.text for segment in transcript_list])
        
        return transcript_text

    except Exception as e:
        print(f"Error occurred in get_youtube_transcript: {e}")
        return f"Error: Failed to fetch transcript. Details: {e}"