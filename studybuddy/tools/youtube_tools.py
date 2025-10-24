# In studybuddy/tools/youtube_tools.py (DEFINITIVE, BROWSER-MIMICKING VERSION)

import re
import json
import requests
from urllib.parse import urlparse, parse_qs
from langchain_core.tools import tool

# This User-Agent header is non-negotiable. It makes us look like a real browser.
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def _get_video_id(url: str) -> str | None:
    """Extracts the YouTube video ID from any URL."""
    try:
        parsed_url = urlparse(url)
        if "youtu.be" in parsed_url.hostname:
            return parsed_url.path[1:]
        if "youtube.com" in parsed_url.hostname:
            if parsed_url.path == "/watch":
                return parse_qs(parsed_url.query)["v"][0]
        return None
    except Exception:
        return None

@tool
def get_youtube_transcript(url: str) -> str:
    """
    Fetches the full English transcript for a given YouTube video URL.
    This is a robust, custom implementation that bypasses all failing libraries.
    """
    video_id = _get_video_id(url)
    if not video_id:
        return "Error: Invalid YouTube URL."

    try:
        # Step 1: Fetch the watch page HTML with a browser User-Agent
        watch_url = f"https://www.youtube.com/watch?v={video_id}"
        response = requests.get(watch_url, headers=BROWSER_HEADERS, timeout=20)
        response.raise_for_status()

        # Step 2: Extract the player response JSON blob from the HTML. This is the new, robust method.
        match = re.search(r'var ytInitialPlayerResponse = ({.*?});', response.text, re.DOTALL)
        if not match:
            return "Error: Could not find video metadata. Transcripts might be disabled or YouTube's page structure changed."

        player_response = json.loads(match.group(1))
        
        # Step 3: Navigate the complex JSON to find the caption URL
        caption_tracks = player_response.get("captions", {}).get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
        
        if not caption_tracks:
            return "Error: Transcripts are disabled for this video."

        # Find the English ('en') transcript URL
        transcript_url = None
        for track in caption_tracks:
            # We look for simple English captions first, then auto-generated ones
            if track.get("languageCode") == "en":
                transcript_url = track.get("baseUrl")
                break
        
        if not transcript_url:
            return "Error: No English transcript could be found."

        # Step 4: Fetch the actual transcript XML from the URL
        transcript_response = requests.get(transcript_url, headers=BROWSER_HEADERS, timeout=20)
        transcript_response.raise_for_status()
        
        # Step 5: Parse the simple XML text without a fragile XML parser.
        lines = re.findall(r'<text start="[^"]+" dur="[^"]+">(.*?)</text>', transcript_response.text)
        cleaned_lines = [line.replace('&#39;', "'").replace('&amp;', '&').strip() for line in lines]
        
        final_transcript = " ".join(cleaned_lines)
        
        if not final_transcript:
             return "Error: The transcript was found but contained no text."

        return final_transcript

    except Exception as e:
        return f"Error: A critical, unexpected failure occurred during transcript extraction. Details: {str(e)}"