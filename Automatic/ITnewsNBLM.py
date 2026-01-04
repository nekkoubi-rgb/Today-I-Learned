import os
import datetime
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
import io
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_SERVICE_ACCOUNT_INFO = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON") # JSON string or path
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID") # Target folder ID in Drive

# Search Keywords and Filters
SEARCH_QUERIES = ["IT 最新", "AI ニュース", "エンジニア トレンド"]
EXCLUDE_WORDS = ["ひろゆき", "切り抜き", "副業", "稼げる", "炎上"]
MIN_VIEW_COUNT = 100
MIN_DURATION_SECONDS = 300 # 5 minutes

def get_youtube_service():
    return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_drive_service():
    if not GOOGLE_SERVICE_ACCOUNT_INFO:
        raise ValueError("Google Service Account Info not found.")
    
    try:
        # Try parsing as JSON string first
        info = json.loads(GOOGLE_SERVICE_ACCOUNT_INFO)
        creds = service_account.Credentials.from_service_account_info(info)
    except json.JSONDecodeError:
        # If not JSON string, assume it's a file path
        creds = service_account.Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_INFO)
        
    return build('drive', 'v3', credentials=creds)

def search_videos(youtube):
    videos = []
    # Calculate time 24 hours ago in RFC 3339 format
    published_after = (datetime.datetime.utcnow() - datetime.timedelta(hours=24)).isoformat("T") + "Z"

    for query in SEARCH_QUERIES:
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            publishedAfter=published_after,
            maxResults=10,
            relevanceLanguage="ja",
            regionCode="JP"
        )
        response = request.execute()

        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            
            # Simple word exclusion
            if any(word in title for word in EXCLUDE_WORDS):
                continue
            
            videos.append({
                "id": video_id,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })
    
    return videos

def filter_videos_details(youtube, video_candidates):
    final_videos = []
    if not video_candidates:
        return []

    video_ids = [v["id"] for v in video_candidates]
    # Process in chunks of 50 if needed, but for small daily volume, one batch is likely fine
    request = youtube.videos().list(
        part="statistics,contentDetails",
        id=",".join(video_ids)
    )
    response = request.execute()

    for item in response.get("items", []):
        stats = item["statistics"]
        content_details = item["contentDetails"]
        
        view_count = int(stats.get("viewCount", 0))
        duration_iso = content_details.get("duration", "PT0S")
        
        # Parse duration (Simplified parsing for PT#M#S)
        # For robust parsing, isodate library is recommended, but we keep it simple here or assume standard format
        import re
        match = re.search(r'PT(\d+H)?(\d+M)?(\d+S)?', duration_iso)
        seconds = 0
        if match:
            h = int(match.group(1)[:-1]) if match.group(1) else 0
            m = int(match.group(2)[:-1]) if match.group(2) else 0
            s = int(match.group(3)[:-1]) if match.group(3) else 0
            seconds = h*3600 + m*60 + s

        if view_count >= MIN_VIEW_COUNT and seconds >= MIN_DURATION_SECONDS:
            # Find the original candidate to keep metadata
            for v in video_candidates:
                if v["id"] == item["id"]:
                    final_videos.append(v)
                    break
    
    return final_videos

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ja'])
        full_text = " ".join([t['text'] for t in transcript_list])
        return full_text
    except (NoTranscriptFound, Exception) as e:
        print(f"Transcript error for {video_id}: {e}")
        return None

def summarize_content(text):
    if not text:
        return "字幕が取得できませんでした。"
        
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = f"""
    以下のYouTube動画の字幕テキストを要約し、以下の形式で出力してください。
    
    形式:
    - 5つの要約ポイント (箇条書き)
    
    テキスト:
    {text[:10000]} # Limit characters to avoid token limits if necessary
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Cost-effective model
            messages=[
                {"role": "system", "content": "あなたは優秀なITニュース要約アシスタントです。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"要約生成エラー: {e}"

def upload_to_drive(drive_service, filename, content):
    file_metadata = {
        'name': filename,
        'parents': [DRIVE_FOLDER_ID] if DRIVE_FOLDER_ID else []
    }
    media = MediaIoBaseUpload(io.BytesIO(content.encode('utf-8')), mimetype='text/plain')
    
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    print(f"File ID: {file.get('id')} uploaded.")

def main():
    print("Starting IT News Extraction...")
    try:
        youtube = get_youtube_service()
    except Exception as e:
        print(f"Failed to initialize YouTube service: {e}")
        return

    # 1. Search
    candidates = search_videos(youtube)
    print(f"Found {len(candidates)} candidates.")
    
    # 2. Filter
    targets = filter_videos_details(youtube, candidates)
    print(f"Filtered to {len(targets)} videos.")
    
    if not targets:
        print("No videos matched criteria today.")
        return

    daily_report = f"IT News Summary - {datetime.date.today()}\n\n"
    
    # 3. Extract & Summarize
    for video in targets:
        print(f"Processing: {video['title']}")
        transcript = get_transcript(video['id'])
        
        if transcript:
            summary = summarize_content(transcript)
        else:
            summary = "（字幕なし / 自動生成字幕不可）"
            
        daily_report += f"## {video['title']}\n"
        daily_report += f"URL: {video['url']}\n\n"
        daily_report += f"{summary}\n"
        daily_report += "-"*40 + "\n\n"

    # 4. Upload
    filename = f"{datetime.date.today()}_IT_News.txt"
    try:
        drive = get_drive_service()
        upload_to_drive(drive, filename, daily_report)
        print("Upload complete.")
    except Exception as e:
        print(f"Drive Upload Failed: {e}")
        # Identify if local run, maybe save to file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(daily_report)
        print(f"Saved locally to {filename}")

if __name__ == "__main__":
    main()
