import os
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# ==========================================
# 1. PASTE YOUR AUTHENTICATION KEYS HERE
# ==========================================
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REFRESH_TOKEN = "YOUR_REFRESH_TOKEN"  # The token printed in the previous step

# ==========================================
# 2. DEFINE YOUR VIDEO METADATA & SCHEDULE
# ==========================================
# Choose your video's Category ID. Examples: 
# "22" = People & Blogs, "20" = Gaming, "27" = Education, "28" = Science & Technology.
CATEGORY_ID = "22" 

# For scheduled videos, 'privacyStatus' MUST be set to "private"
PRIVACY_STATUS = "private" 

# Setting the Schedule:
# Must be in ISO 8601 format (YYYY-MM-DDThh:mm:ssZ) in UTC time.
# Ensure the date is in the future.
publish_time = datetime.datetime.utcnow() + datetime.timedelta(days=2) # Scheduled for 2 days from now
PUBLISH_AT_ISO = publish_time.strftime("%Y-%m-%dT%H:%M:%SZ")

metadata_body = {
    "snippet": {
        "title": "Programmatic Test Video Title",
        "description": (
            "This video was uploaded programmatically using the YouTube Data API v3!\n\n"
            "Keep up with my automatic postings."
        ),
        "tags": ["automated", "python", "youtube-api", "scheduling"],
        "categoryId": CATEGORY_ID
    },
    "status": {
        "privacyStatus": PRIVACY_STATUS,
        "publishAt": PUBLISH_AT_ISO, # The date and time when the video should become public
        "selfDeclaredMadeForKids": False # Set to True if your content is explicitly for kids
    }
}

# Path to the actual video file on your computer/server
VIDEO_FILE_PATH = "my_video.mp4" 

# ==========================================
# 3. CORE UPLOAD FUNCTIONS
# ==========================================
def get_authenticated_service():
    """Rebuilds the credentials headlessly using the Refresh Token."""
    credentials = Credentials(
        token=None,  # The library will automatically request a temporary access token
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
    return build("youtube", "v3", credentials=credentials)

def upload_video(youtube):
    if not os.path.exists(VIDEO_FILE_PATH):
        print(f"Error: Video file not found at path: {VIDEO_FILE_PATH}")
        return

    print(f"Preparing upload of: {VIDEO_FILE_PATH}")
    print(f"Scheduled to publish at (UTC): {PUBLISH_AT_ISO}")
    
    # We use MediaFileUpload to enable resumable chunk-by-chunk uploads (safer for larger files)
    media = MediaFileUpload(
        VIDEO_FILE_PATH, 
        chunksize=1024 * 1024, # 1MB chunk sizes
        mimetype="video/*", 
        resumable=True
    )
    
    request = youtube.videos().insert(
        part="snippet,status",
        body=metadata_body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploading... {int(status.progress() * 100)}% complete.")
            
    print("\n" + "="*40)
    print("         UPLOAD SUCCESSFUL!         ")
    print("="*40)
    print(f"Video ID: {response.get('id')}")
    print(f"Title: {response.get('snippet', {}).get('title')}")
    print(f"Publish Schedule: {response.get('status', {}).get('publishAt')}")
    print("="*40 + "\n")

if __name__ == "__main__":
    youtube_service = get_authenticated_service()
    upload_video(youtube_service)
