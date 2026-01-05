import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

def fetch_youtube_content(video_id):
    try:
        # A. メタデータ取得
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.videos().list(part='snippet', id=video_id)
        response = request.execute()
        snippet = response['items'][0]['snippet']

        # B. 字幕取得 (v1.2.3 新仕様: fetch メソッドを使用)
        print(f"字幕を取得中（v1.2.3 fetch）: {video_id}...")
        try:
            # 1. APIクラスをインスタンス化
            api = YouTubeTranscriptApi()
            
            # 2. fetchメソッドで字幕オブジェクトを取得
            # languagesはリスト形式。日本語(ja)を優先。
            transcript_obj = api.fetch(video_id, languages=['ja', 'en'])
            
            # 3. 字幕データ（リスト形式）を抽出
            # 最新版では to_raw_data() または再度 fetch() を呼ぶ必要があります
            if hasattr(transcript_obj, 'to_raw_data'):
                data = transcript_obj.to_raw_data()
            else:
                data = transcript_obj # すでにリストの場合のフォールバック
            
            transcript_text = "\n".join([t['text'] for t in data])
            print(f"字幕の取得に成功しました。")
            
        except Exception as e:
            # fetchがダメなら list メソッドで詳細に探す
            print(f"fetchで失敗、listメソッドで再試行中... ({e})")
            try:
                transcript_list = api.list(video_id)
                # 日本語（自動生成含む）を探す
                transcript = transcript_list.find_transcript(['ja', 'en'])
                data = transcript.fetch()
                transcript_text = "\n".join([t['text'] for t in data])
                print(f"listメソッドで取得に成功しました。")
            except Exception as e_final:
                print(f"最終エラー: {e_final}")
                transcript_text = f"字幕を取得できませんでした: {e_final}"

        # C. ファイル出力
        filename = f"{video_id}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {snippet['title']}\n\n")
            f.write(f"## Description\n{snippet['description']}\n\n")
            f.write(f"## Transcript\n{transcript_text}\n")
        
        print(f"完了: {filename} を保存しました。")

    except Exception as e:
        print(f"システムエラー: {e}")

if __name__ == "__main__":
    v_id = "Bt761_2_Fgo" 
    fetch_youtube_content(v_id)