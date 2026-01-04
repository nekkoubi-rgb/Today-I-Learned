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
    test_api()