import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# 1. .envファイルから環境変数を読み込む
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

def test_api():
    try:
        # 2. YouTube API サービスの構築
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        # 3. 指定した動画IDの情報をリクエスト
        # (例として YouTube 公式の動画 ID '7lC49wQBY6I' を使用)
        request = youtube.videos().list(
            part='snippet',
            id='7lC49wQBY6I'
        )
        response = request.execute()

        # 4. 結果の出力
        if response['items']:
            title = response['items'][0]['snippet']['title']
            print(f"成功: 動画タイトル -> {title}")
        else:
            print("エラー: 動画が見つかりませんでした。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    # 確実に存在する動画ID（例：Rick Astley - Never Gonna Give You Up）
    # または、今YouTubeで開いている動画の ?v= 以降の11文字を入力してください
    target_id = input("テストしたい動画IDを入力（空押しでデフォルトIDを使用）: ") or 'dQw4w9WgXcQ'
    
    # 既存の test_api 関数を少し修正して引数を受け取れるようにするか、
    # 直接 ID を指定して実行
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.videos().list(
            part='snippet',
            id=target_id
        )
        response = request.execute()

        if response['items']:
            snippet = response['items'][0]['snippet']
            print(f"成功！")
            print(f"タイトル: {snippet['title']}")
            print(f"チャンネル: {snippet['channelTitle']}")
        else:
            print(f"エラー: ID '{target_id}' は見つかりませんでした。別のIDを試してください。")
    except Exception as e:
        print(f"実行エラー: {e}")