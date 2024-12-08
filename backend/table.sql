-- 创建表
CREATE TABLE tb_customer_rules_map (
    customer_rules_id SERIAL PRIMARY KEY,  -- 设置为自增字段
    age INTEGER NOT NULL,
    customer_rules TEXT NOT NULL,
    display_rules TEXT NOT NULL  -- show_rules 字段不能为空
);

-- 插入数据
INSERT INTO tb_customer_rules_map (age, customer_rules, display_rules) 
VALUES 
    (10, '', 'default'),
    (10, 'only decimal', 'decimal'),
    (10, 'only fraction', 'fraction'),
    (10, 'only plane geometry', 'geometry'),
    (10, 'only geometric volume', 'geometric volume');

INSERT INTO tb_customer_rules_map (age, customer_rules, display_rules) 
VALUES 
    (6, '', 'default'),
    (7, '', 'default'),
    (8, '', 'default'),
    (9, '', 'default');
