-- 模拟消费记录（user_id = 10001）
INSERT INTO expenses (user_id, category_id, amount, description, date, payment_method, created_at) VALUES
(10001, 1, 22.50, '早餐', '2025-05-01', '微信', CURRENT_TIMESTAMP),
(10001, 1, 45.00, '午餐', '2025-05-01', '支付宝', CURRENT_TIMESTAMP),
(10001, 2, 12.00, '打车', '2025-05-01', '现金', CURRENT_TIMESTAMP),
(10001, 3, 58.00, '电影票', '2025-05-02', '支付宝', CURRENT_TIMESTAMP),
(10001, 1, 38.00, '晚餐', '2025-05-02', '微信', CURRENT_TIMESTAMP),
(10001, 4, 19.90, '洗发水', '2025-05-03', '微信', CURRENT_TIMESTAMP),
(10001, 2, 10.00, '地铁', '2025-05-03', '现金', CURRENT_TIMESTAMP),
(10001, 3, 35.00, '网游点卡', '2025-05-03', '支付宝', CURRENT_TIMESTAMP),
(10001, 4, 15.80, '牙膏牙刷', '2025-05-04', '微信', CURRENT_TIMESTAMP),
(10001, 1, 50.00, '聚餐', '2025-05-04', '支付宝', CURRENT_TIMESTAMP),

(10001, 2, 8.00, '公交车', '2025-05-05', '现金', CURRENT_TIMESTAMP),
(10001, 3, 66.00, '游戏充值', '2025-05-05', '支付宝', CURRENT_TIMESTAMP),
(10001, 1, 20.00, '包子早餐', '2025-05-06', '微信', CURRENT_TIMESTAMP),
(10001, 1, 42.00, '自助午餐', '2025-05-06', '微信', CURRENT_TIMESTAMP),
(10001, 4, 26.30, '洗面奶', '2025-05-06', '微信', CURRENT_TIMESTAMP),
(10001, 2, 15.00, '打车回家', '2025-05-07', '支付宝', CURRENT_TIMESTAMP),
(10001, 3, 55.00, 'KTV', '2025-05-07', '支付宝', CURRENT_TIMESTAMP),
(10001, 1, 30.00, '便当', '2025-05-08', '微信', CURRENT_TIMESTAMP),
(10001, 4, 17.50, '垃圾袋', '2025-05-08', '微信', CURRENT_TIMESTAMP),
(10001, 2, 9.50, '共享单车', '2025-05-08', '支付宝', CURRENT_TIMESTAMP);
