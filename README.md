# GitHub/VSCode操作方法

## 基本操作
### PullRequest/branch作成

- git checkout -b 枝名
>ブランチ作成、作業場をブランチに移動

- git add .
>次の動作(commit)の対象(.)を指定  
※ドット=現フォルダの変更があったファイル  
add .の取り消しはgit restore --staged .

- git commit -m "変更内容"
>作業内容を書き加え、**PC上で**保存。

- git push origin ブランチ名
 >ブランチデータを**PC上からGithubに**送る。  
 Github上にも同じブランチ名で作成される。

*GitHubでPull Request作成 → Merge*  

- git checkout main
>mainに戻る

- git pull origin main
>主幹データを**GithubからPCに**同期。

- git branch -d ブランチ名
>PC上のブランチを消す。  
squash mergeの時は-D(強制削除)。

- git fetch --prune
>git(≠Github)上の枝のリストを更新(剪定)。


### 枝名候補
- feat/test
>feature=機能、特徴
- fix/test
>fix=バグ/ミス修正
- docs/readme


## 備忘録

- origin = http://github.com/user/Today-I-Learned.git  
(初回紐付け済み)

- Repository作成後、remote add origin~で指定を間違えた為、commit出来なかった。(ライセンスも作っていなかった)

>→再度紐付けで修正。
Repository作成時に**READMEは必須**、ライセンスは自由度順でMIT→Apache2.0→GPL→ライセンス無し。**MITが無難**。

- githubの画面で後からライセンスファイル作ったらpushできなくなった。
**(非推奨)**

>→万が一github上でファイルいじったら、git pull。

- "git commit"だけで入力した為、Vimが立ち上がってしまった。

>→[I]キーで挿入モードに変更、変更内容入力
[ESC]→ZZで終了。

- Markdown書式の#や-がそのまま表示されていた。

>→#や-は半角スペースを加える。「# 」「- 」

- 誤ってデータを消してしまった場合は、戻す位置のgithubのハッシュ値を拾ってくる
>→git restore --source [ハッシュ値] [ファイル名]  
ファイル名が分からない場合はgit show --name-only [ハッシュ値]