/*
CREATE DATABASE retail_analysis;        -- [retail_analysis]という名前の関係データベースを作成。RDB。
↑2回目以降実行する時にエラー出る。既に存在する為。
*/
CREATE DATABASE IF NOT EXISTS retail_analysis;      -- retail_analysisが「もしなければ作る」(IF NOT EXISTS)
USE retail_analysis;                    -- 使用

-- 既存のテーブルを削除。IDが自動割り振りの為、同じ店名でも1,2,3,4,5,6と増えていく為、起動時に削除。子(visit_logs)から消す。
DROP TABLE IF EXISTS visit_logs;
DROP TABLE IF EXISTS stores;
-- もっと良い方法有りそう。


-- 店舗マスターテーブル
/*
CREATE TABLE stores (       -- テーブルを作成。店舗情報。変更しないデータ群。マスターテーブル。
データベースと一緒で、2回目以降エラー出る。IF NOT EXISTSに変更。
*/
CREATE TABLE IF NOT EXISTS stores (
    store_id INT AUTO_INCREMENT PRIMARY KEY,    -- 変数を宣言。店舗ID。AUTO_INCREMENT:自動で番号を振る。PRIMARY KEY:主キー。[数値]。
    store_name VARCHAR(100) NOT NULL,       -- 変数を宣言。店舗名。100文字まで。NULL禁止。[可変長]
    staff_name VARCHAR(50),               -- 担当者名。50文字まで。[可変長]
    contract_type ENUM('Direct', 'Agency') -- コントラクト:契約。[選択式]。→ENUMは定義変更が大変。JOIN推奨
);

-- 訪問ログテーブル（活動記録）
/*
CREATE TABLE visit_logs (       -- [Visit_logs]テーブルを作成。日々更新されるデータ群。トランザクションテーブル。
データベース、storesテーブルと一緒でエラー出る。IF NOT EXISTSに変更。
*/
CREATE TABLE IF NOT EXISTS visit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,      -- 変数を宣言。自動で番号割り振り。主キー。[数値]
    store_id INT,                               -- 変数を宣言。店舗ID。[数値]。
    visit_date DATE NOT NULL,             -- 変数を宣言。訪問日。NULL禁止。[日付]。
    dwell_time_minutes INT,               -- 変数を宣言。滞在時間。分単位。[数値]。
    FOREIGN KEY (store_id) REFERENCES stores(store_id)  -- 外部キー。visit_logs(store_id)はstores(store_id)を参照。
);
-- 店舗の登録
INSERT INTO stores (store_name, staff_name) VALUES      -- 店舗名と担当者名を追加(stores)。
('Store-K-001', 'Sato'),
('Store-L-002', 'Suzuki'),
('Store-O-003', 'Takahashi');

-- 訪問記録の挿入（1月分の稼働を想定）
INSERT INTO visit_logs (store_id, visit_date, dwell_time_minutes) VALUES        -- 店舗ID、訪問日、滞在時間を追加(visit_logs)。
(1, '2026-01-10', 45),
(1, '2026-01-20', 60),
(2, '2026-01-12', 30),
(3, '2026-01-15', 120);

-- 店舗別の月間集計レポート
SELECT 
    s.store_name,   -- 店名。s.=storesテーブルの別名(エイリアス)。40行目で指定。[sテーブルのstore_name]。
    s.staff_name,   -- 担当者名。
    COUNT(v.log_id) AS monthly_visit_count,      -- 訪問回数を集計
    SUM(v.dwell_time_minutes) AS total_dwell_min, -- 合計滞在時間を集計
    AVG(v.dwell_time_minutes) AS avg_dwell_min    -- 平均滞在時間を算出
FROM stores s                                     -- storesテーブルをsという別名(エイリアス)で指定。
LEFT JOIN visit_logs v ON s.store_id = v.store_id -- visit_logsテーブルをvというエイリアスで指定。店舗情報に訪問記録を店舗IDで結合(JOIN)。
WHERE v.visit_date BETWEEN '2026-01-01' AND '2026-01-31'    -- 絞り込み(WHERE)。1月中。
GROUP BY s.store_id,
    s.store_name,
    s.staff_name;            -- 店舗IDで情報を仕分け(グループ化)。表示したい項目は全て書く(店名、担当者名)。

-- 余計な条件を入れず、中身を全て見る
-- SELECT * FROM stores;