# In studybuddy/tools/youtube_tools.py

import re
from langchain_core.tools import tool
from youtube_transcript_api import YouTubeTranscriptApi

def _extract_video_id(url: str) -> str | None:
    """Extracts the YouTube video ID from a URL."""
    # This regex handles standard, shortened, and embedded YouTube URLs
    match = re.search(r"(?:v=|\/|youtu\.be\/|embed\/)([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    return None

@tool
def get_youtube_transcript(url: str) -> str:
    """
    Fetches the full transcript for a given YouTube video URL.
    Returns the transcript as a single string. If the transcript
    is disabled for the video or the URL is invalid, an error
    message is returned.
    """
    video_id = _extract_video_id(url)
    if not video_id:
        return "Error: Invalid YouTube URL provided. Could not extract video ID."

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all parts of the transcript into a single string
        transcript = " ".join([item['text'] for item in transcript_list])
        return transcript
    
    except Exception as e:
        print(f"Error fetching transcript for video ID {video_id}: {e}")
        return f"Error: Could not fetch transcript. It might be disabled for this video. Details: {str(e)}"