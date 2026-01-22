CREATE DATABASE retail_analysis;
USE retail_analysis;

-- 店舗マスターテーブル
CREATE TABLE stores (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    staff_name VARCHAR(50),               -- 担当者名
    contract_type ENUM('Direct', 'Agency') -- 契約区分（例）
);

-- 訪問ログテーブル（実務的な活動記録）
CREATE TABLE visit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    store_id INT,
    visit_date DATE NOT NULL,             -- 訪問日
    dwell_time_minutes INT,               -- 滞留時間（分単位で管理）
    FOREIGN KEY (store_id) REFERENCES stores(store_id)
);
-- 店舗の登録
INSERT INTO stores (store_name, staff_name) VALUES 
('Store-K-001', 'Sato'),
('Store-L-002', 'Suzuki'),
('Store-O-003', 'Takahashi');

-- 訪問記録の挿入（1月分の稼働を想定）
INSERT INTO visit_logs (store_id, visit_date, dwell_time_minutes) VALUES 
(1, '2026-01-10', 45),
(1, '2026-01-20', 60),
(2, '2026-01-12', 30),
(3, '2026-01-15', 120);

-- 店舗別の月間集計レポート
SELECT 
    s.store_name, 
    s.staff_name,
    COUNT(v.log_id) AS monthly_visit_count,      -- 訪問回数を集計
    SUM(v.dwell_time_minutes) AS total_dwell_min, -- 合計滞留時間を集計
    AVG(v.dwell_time_minutes) AS avg_dwell_min    -- 平均滞留時間を算出
FROM stores s
LEFT JOIN visit_logs v ON s.store_id = v.store_id
WHERE v.visit_date BETWEEN '2026-01-01' AND '2026-01-31'
GROUP BY s.store_id;

-- 余計な条件を入れず、中身を全て見る
SELECT * FROM stores;