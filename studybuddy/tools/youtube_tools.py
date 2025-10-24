# In studybuddy/tools/youtube_tools.py (THE STANDARD, CORRECT, LIBRARY-BASED VERSION)

import re
from langchain_core.tools import tool
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def _extract_video_id(url: str) -> str | None:
    """Extracts the YouTube video ID from a URL."""
    match = re.search(r"(?:v=|\/|youtu\.be\/|embed\/)([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    return None

@tool
def get_youtube_transcript(url: str) -> str:
    """
    Fetches the full English transcript for a given YouTube video URL.
    This uses the industry-standard youtube-transcript-api library.
    This is the definitive and stable implementation.
    """
    video_id = _extract_video_id(url)
    if not video_id:
        return "Error: Invalid YouTube URL provided."

    try:
        # THE CORRECT METHOD: Use the official library that is now installed correctly.
        transcript_parts = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        
        # Join the transcript text parts into a single, continuous string.
        transcript = " ".join([part['text'] for part in transcript_parts])
        
        if not transcript:
             return "Error: The video has a transcript, but it's empty."
             
        return transcript
    
    except TranscriptsDisabled:
        return f"Error: Transcripts are disabled for this video."
    except NoTranscriptFound:
        return f"Error: No English transcript could be found for this video."
    except Exception as e:
        return f"Error: A critical library error occurred: {str(e)}"