import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# .envの読み込み
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

def fetch_youtube_content(video_id):
    try:
        # A. メタデータ取得
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.videos().list(part='snippet', id=video_id)
        response = request.execute()

        if not response['items']:
            print("エラー: 動画が見つかりません。")
            return

        snippet = response['items'][0]['snippet']
        title = snippet['title']
        description = snippet['description']

# B. 字幕取得 (Version 1.2.3 以降の書き方)
        print(f"字幕を取得中（v1.2.3 準拠）: {video_id}...")
        try:
            # 1. クラスをインスタンス化する（ここが重要）
            api = YouTubeTranscriptApi()
            
            # 2. インスタンスに対して fetch メソッドまたは get_transcript を呼ぶ
            # 1.2.3 では fetch() でリスト取得、または直接 get_transcript が推奨されます
            transcript_data = api.get_transcript(video_id, languages=['ja', 'en'])
            
            transcript_text = "\n".join([t['text'] for t in transcript_data])
            print("字幕の取得に成功しました。")
            
        except Exception as e:
            print(f"字幕取得不可: {e}")
            transcript_text = f"字幕情報が取得できませんでした: {e}"
            
        # C. ファイル出力 (Markdown形式)
        filename = f"{video_id}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"## Metadata\n- ID: {video_id}\n- Channel: {snippet['channelTitle']}\n\n")
            f.write(f"## Description\n{description}\n\n")
            f.write(f"## Transcript\n{transcript_text}\n")

        print(f"完了: '{filename}' を作成しました。")

    except Exception as e:
        # ここが「外側のtry」に対するexceptです。これが欠けるとSyntaxErrorになります。
        print(f"システム全体でエラーが発生しました: {e}")

if __name__ == "__main__":
    v_id = input("要約したいYouTube動画IDを入力してください: ")
    if v_id:
        fetch_youtube_content(v_id)