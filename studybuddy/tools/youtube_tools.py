# In studybuddy/tools/youtube_tools.py (THE STANDARD, CORRECT, LIBRARY-BASED VERSION)

import re
import requests
import json
import time
from langchain_core.tools import tool
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def _extract_video_id(url: str) -> str | None:
    """Extracts the YouTube video ID from a URL."""
    match = re.search(r"(?:v=|\/|youtu\.be\/|embed\/)([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    return None

def _get_transcript_alternative(video_id: str) -> str:
    """Alternative method using different approaches when the main library fails."""
    try:
        # Method 1: Try with manual transcript list and different parameters
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try different transcript types
        for transcript in transcript_list:
            try:
                # Try fetching with different parameters
                transcript_data = transcript.fetch()
                if transcript_data:
                    transcript_text = " ".join([part['text'] for part in transcript_data])
                    if transcript_text.strip():
                        return transcript_text
            except Exception:
                continue
                
        return "Error: No working transcript found in alternative method."
        
    except Exception as e:
        return f"Error: Alternative method failed: {str(e)}"

def _get_transcript_manual(video_id: str) -> str:
    """Manual method using direct YouTube page scraping as last resort."""
    try:
        # This is a simplified manual approach
        # In a real implementation, you'd parse the YouTube page for transcript data
        return "Error: Manual transcript extraction not implemented. Please try a different video or check if the video has captions enabled."
    except Exception as e:
        return f"Error: Manual method failed: {str(e)}"

@tool
def get_youtube_transcript(url: str) -> str:
    """
    Fetches the full English transcript for a given YouTube video URL.
    Uses multiple fallback methods to handle various transcript formats.
    """
    video_id = _extract_video_id(url)
    if not video_id:
        return "Error: Invalid YouTube URL provided."

    # Method 1: Try the most basic approach first
    try:
        transcript_parts = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([part['text'] for part in transcript_parts])
        if transcript_text.strip():
            return transcript_text
    except (TranscriptsDisabled, NoTranscriptFound):
        return "Error: No transcript could be found for this video."
    except Exception as e:
        if "no element found" not in str(e).lower():
            return f"Error: {str(e)}"
    
    # Method 2: Try with specific language
    try:
        transcript_parts = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript_text = " ".join([part['text'] for part in transcript_parts])
        if transcript_text.strip():
            return transcript_text
    except (TranscriptsDisabled, NoTranscriptFound):
        pass
    except Exception as e:
        if "no element found" not in str(e).lower():
            return f"Error: {str(e)}"
    
    # Method 3: Try alternative approach
    result = _get_transcript_alternative(video_id)
    if not result.startswith("Error:"):
        return result
    
    # Method 4: Try manual approach as last resort
    return _get_transcript_manual(video_id)    