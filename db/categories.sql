-- 一级分类
INSERT INTO categories (id, name, parent_id, level)
VALUES (1, '餐饮', NULL, 1),
       (2, '交通', NULL, 1),
       (3, '购物', NULL, 1),
       (4, '居家', NULL, 1),
       (5, '娱乐', NULL, 1),
       (6, '医疗', NULL, 1),
       (7, '教育', NULL, 1),
       (8, '其他', NULL, 1),
       (9, '投资理财', NULL, 1);

-- 餐饮
INSERT INTO categories (id, name, parent_id, level)
VALUES (101, '早餐', 1, 2),
       (102, '午餐', 1, 2),
       (103, '晚餐', 1, 2),
       (104, '零食', 1, 2);

-- 交通
INSERT INTO categories (id, name, parent_id, level)
VALUES (201, '公交', 2, 2),
       (202, '地铁', 2, 2),
       (203, '打车', 2, 2),
       (204, '加油', 2, 2);

-- 购物
INSERT INTO categories (id, name, parent_id, level)
VALUES (301, '衣物', 3, 2),
       (302, '日用', 3, 2),
       (303, '数码', 3, 2),
       (304, '网购', 3, 2);

-- 居家
INSERT INTO categories (id, name, parent_id, level)
VALUES (401, '房租', 4, 2),
       (402, '水电', 4, 2),
       (403, '维修', 4, 2);

-- 娱乐
INSERT INTO categories (id, name, parent_id, level)
VALUES (501, '电影', 5, 2),
       (502, '旅游', 5, 2),
       (503, '聚会', 5, 2);

-- 医疗
INSERT INTO categories (id, name, parent_id, level)
VALUES (601, '门诊', 6, 2),
       (602, '药品', 6, 2),
       (603, '体检', 6, 2);

-- 教育
INSERT INTO categories (id, name, parent_id, level)
VALUES (701, '学费', 7, 2),
       (702, '书籍', 7, 2);

-- 其他
INSERT INTO categories (id, name, parent_id, level)
VALUES (801, '捐赠', 8, 2),
       (802, '杂项', 8, 2);

-- 投资理财
INSERT INTO categories (id, name, parent_id, level)
VALUES (901, '基金', 9, 2),
       (902, '股票', 9, 2),
       (903, '债券', 9, 2),
       (904, '保险', 9, 2),
       (905, '黄金', 9, 2),
       (906, '数字货币', 9, 2),
       (907, '理财产品', 9, 2),
       (908, '其他投资', 9, 2);
