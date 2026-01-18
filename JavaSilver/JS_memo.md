# Java関連メモ


- ファイル名とclassは同じ(Main.java=Main)  
- **クラス名**、**パッケージ名**(ファイル名、フォルダ名)に[-]使用不可  
- Javaの配列は**0から始まる**  


## 基本仕様

### コード作成
- ソースコード=人が読める状態(public~)  
- ソースファイル(.java)  

### コンパイル
- **コンパイラ**(**ソースファイル→クラスファイル**に変換、**文法チェック**)
- バイトコード=0と1
- クラスファイル(.class)

### 実行
- **インタプリタ**(**バイトコード→マシン語**に変換。
**JVM(Java Virtual Machine)内蔵**)

>Javaコンパイラで出力したバイトコード(.classファイル)は、特定のCPUに依存しない中間コードの為、汎用性◎  
**"Write Once,Run Anywhere"**

## コード記述
### 大まかな流れ
1:変数宣言
`int var;`  
2:計算、結果を変数に代入
`var = 3 + 5;`  
3:命令実行
`println(var)`  

### 仕様
データ型の種類

|型名|格納データ|補足|
|:---|:---|:---|
|byte|整数(極小)|8bit|
|short|整数(小)|16bit|
|int|整数|**基本使用** 32bit|
|long|整数(大)|Lを付ける 64bit|
|float|小数|Fを付ける 曖昧な数値|
|double|小数|**基本使用** 64bit|
|boolean|真偽値|true/false|
|char|文字|**'1文字'**|
|**S**tring|文字|**"文字列"** <br>参照型の為大文字|
|final|**定数**|final int conVar = 15;|

- `_`(アンダースコア)
数値を読みやすくする為に使用  
先頭、末尾、記号前後にはNG  
`int var = 1_000_000;`  

### 注意事項

- 変数名  
**小文字**で開始。2つ目の単語以降の頭文字を大文字
数字で始めるのはNG
publicやclass等はJavaですべて使われてる為NG
使える記号は「_」と「$」のみ  
`varCount1`

- `float型`、`double型`は誤差有り

- 変数の初期化  
宣言と同時に値を代入  
`int var = 8;`

- インデントと改行  
{}の位置で合わせるのではなく、コードの最初の文字と「}」を合わせる。
「{」は行の末尾に置く(エジプト式)

#### 良い例
```
public class Main{
    public static void main(String[] args){
        System.out.println("良い例");
    }
}
```

#### 悪い例
```
public class Main{
    public static void main(String[] args){
        System.out.println("悪い例");}
                }
```

# JavaSilver黒本用メモ


#### パッケージ
- クラスを整理してる**ディレクトリ**  
- ソースコードの**一番上**に書く  
**package パッケージ名(JavaSilver);**

- ドメイン名の逆にするのが一般的  
    - (google.com → com.google.xxx)  

- フォルダ構造とパッケージ名は一致させる  
    - (package **com.google.xxx**;  
    → src/**com/google/xxx**/main.java)


#### クラスブロック
`public class クラス名{}`

- ファイル名=クラス名.java
- 大文字アルファベット開始。  
- オブジェクトを作る為の**役割の定義/設計図**  
    - 属性(フィールド):そのオブジェクトが持っているデータ
    - 操作(メソッド):そのオブジェクトが出来る事。振る舞い    
    
- 完全修飾クラス名    (FQCN:Fully Qualified Class Name)  
    - **パッケージ名を含む**、クラスの正式なフルネーム  
    >java.util.xxx  
    >java.lang.xxx
    
- メンバ変数
    - フィールド部で変数を宣言する。 **(メソッドの外)**
    - オブジェクトがメモリ上に存在する間は値を保持  
    int xxx;  (初期値0)  
    String yyy;  (初期値null)  

#### メソッドブロック(メインブロック)  
```public static void main(String[] args)```
```
public            公開  
static            静的。共有。  
void              戻り値無し  
main              javaのメソッドの1つ  
(String[] args)   引数(argsはただの変数名)  
```

- ローカル変数
    - メソッド内で変数を宣言する  
    - メソッド実行中のみ保持する。一時的なデータ。  
    **初期値を入れないとエラー**になる。
    
```
    //属性（フィールド）：データ = 社員
    public class Employee {  
    int id;        // 社員番号  
    String name;   // 氏名  

    //操作（メソッド）：振る舞い = 挨拶する
        public void SayHello() {
        System.out.println("私の社員番号は " + id + "、 
        名 前は " + name + " です。");
        }
    }
```
