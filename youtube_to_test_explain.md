```
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
```  

- `import os`  
OSの機能を使用可能にする。  
- `load_dotenv()`  
.envファイル内のAPIキーを読み込む。  
load_**dot**env

- `build`
Youtube Data API用の窓口。

- `YoutubeTranscriptApi`
字幕取得の為のクラスを呼び出し。

```
youtube = build('youtube', 'v3', developerKey=API_KEY)
request = youtube.videos().list(part='snippet', id=video_id)
response = request.execute()
snippet = response['items'][0]['snippet']
```

- `build('youtube', 'v3' developerKey=API_KEY)`
YouTubeAPIのv3(バージョン)を使用  

- `request=youtube.videos().list(part='snippet', id=video_id)`
指定したIDの動画の情報のリクエストを作成  

- `response = request.exeute()`
実際にGoogleサーバーと通信。データを受け取る

- `snippet = response['items'][0]['snippet']`
受け取ったデータからsnippet(タイトル、説明文)を取り出す。

```
api = YouTubeTranscriptApi()  # ①インスタンス化
transcript_obj = api.fetch(video_id, languages=['ja', 'en']) # ②取得
```

- `api = YouTubeTranscriptApi()`
字幕取得用APIのクラスをインスタンス化。

- `transcript_obj = api.fetch(video_id, languages=['ja', 'en'])`
インスタンス化したオブジェクト(api)に日本語か英語字幕の取得を要求

```
data = transcript_obj.to_raw_data()
transcript_text = "\n".join([t['text'] for t in data])
```

- data = transcript_obj.to_raw_data()
取得した字幕オブジェクトをリスト形式(データの羅列。Python仕様)に変換

# 意味不明
- transcript_text = "\n".join([t[''text] for t in data])
内包表記。(Python仕様)

```
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"# {snippet['title']}\n\n")
    f.write(f"## Transcript\n{transcript_text}\n")
```

- `with open(filename, "w", encoding="utf-8") as f:`
ファイルを開く。  
`with` = 書き込み後、自動でファイルを閉じる。  
`w` = Write(書き込みモード。上書き)
`encoding="utf-8"` = 文字化け防止

- `f.write(f"# {snippet['title']}\n\n")`  
タイトル。  
`f.write(...)`  
f(ファイルオブジェクト)に対して書き込む。
`f"#{snippet['title']}"`  
format。  
YouTubeAPIから取得した動画タイトルに置き換わる。  
文字列の中に{変数}を直接埋め込める。  
#は大見出し。

- `f.write(f"## Transcript\n{transcript_text}\n")`  
字幕。
