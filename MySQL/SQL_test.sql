-- 1. まずデータベースを作成（既にある場合は消す）
DROP DATABASE IF EXISTS training_db;
CREATE DATABASE training_db;

-- 2. 使用するDBを指定（これを行わないと以降の操作ができない）
USE training_db;

-- 3. テーブル作成
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price INT,
    stock_count INT DEFAULT 0
);

-- 4. 作成されたか確認（ここで表が表示されるはず）
SHOW TABLES;

-- 5. テストデータの挿入（表示を確認するために追加）
INSERT INTO products (name, category, price) VALUES ('テスト商品', 'テストカテゴリ', 1000);

-- 6. データの抽出（これが最も確実に「表示」を確認できる命令）
SELECT * FROM products;

-- 1. データの挿入（DML: Data Manipulation Language）
INSERT INTO products (name, category, price, stock_count) 
VALUES ('商品A', 'カテゴリA', 5000, 10);

-- 2. データの確認（ここで「No data」が「1行のデータ」に変わる）
SELECT * FROM products;

SELECT * FROM training_db.products;
