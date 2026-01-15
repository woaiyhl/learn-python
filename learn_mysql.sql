-- MySQL 常用命令学习脚本 (基础 + 进阶版)
-- 建议使用 source learn_mysql.sql; 命令导入，或者逐行复制执行

-- ==========================================
-- 0. 环境初始化 (确保可以反复执行)
-- ==========================================
-- 创建一个名为 learn_mysql 的数据库
CREATE DATABASE IF NOT EXISTS learn_mysql CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE learn_mysql;

-- 为了方便反复练习，我们先清理旧表 (注意顺序：先删从表 orders，再删主表 users)
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS users;

-- 展示当前数据库下有哪些表
SHOW TABLES;

-- 展示 users 表的字段结构
DESCRIBE users;

-- 展示 orders 表的字段结构
DESCRIBE orders;


-- ==========================================
-- 1. 表结构操作 (DDL)
-- ==========================================

-- 创建用户表 users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    email VARCHAR(100) UNIQUE COMMENT '邮箱',
    age INT DEFAULT 18 COMMENT '年龄',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户信息表';

-- 创建订单表 orders (新增，用于进阶查询)
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单ID',
    user_id INT NOT NULL COMMENT '关联用户ID',
    order_no VARCHAR(20) NOT NULL COMMENT '订单号',
    amount DECIMAL(10, 2) NOT NULL COMMENT '订单金额',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '下单时间',
    -- 外键约束：当用户被删除时，对应的订单也删除
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- ==========================================
-- 2. 数据准备 (DML)
-- ==========================================

-- 2.1 插入用户
INSERT INTO users (username, email, age) VALUES 
('张三', 'zhangsan@example.com', 25),
('李四', 'lisi@example.com', 30),
('王五', 'wangwu@example.com', 28),
('赵六', 'zhaoliu@example.com', 22);

-- 2.2 插入订单 (注意：这里使用子查询获取 user_id，确保 ID 匹配)
INSERT INTO orders (user_id, order_no, amount, created_at) VALUES
((SELECT id FROM users WHERE username='张三'), 'ORD20230101', 100.00, '2023-01-01 10:00:00'),
((SELECT id FROM users WHERE username='张三'), 'ORD20230105', 50.50, '2023-01-05 14:00:00'),
((SELECT id FROM users WHERE username='李四'), 'ORD20230201', 300.00, '2023-02-01 09:00:00'),
((SELECT id FROM users WHERE username='李四'), 'ORD20230210', 20.00, '2023-02-10 11:30:00');
-- 注意：王五和赵六没有订单，用于演示 LEFT JOIN

-- ==========================================
-- 3. 基础查询回顾
-- ==========================================

-- 简单条件查询
SELECT * FROM users WHERE age > 25;

-- 模糊查询
SELECT * FROM users WHERE username LIKE '张%';

-- 排序与分页
SELECT * FROM users ORDER BY age DESC LIMIT 2;

-- ==========================================
-- 4. 进阶查询实战 (核心重点)
-- ==========================================

-- 4.1 多表关联查询 (JOIN)
-- 场景：查询“谁”买了“什么”，需要关联 users 和 orders 表

-- INNER JOIN (内连接)
-- 只返回两张表都有匹配的数据 (即：只显示有订单的用户)
SELECT u.username, o.order_no, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN (左连接)
-- 返回左表(users)所有数据，即使没有订单 (王五、赵六会显示，订单字段为 NULL)
SELECT u.username, o.order_no, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- 4.2 分组统计 (GROUP BY)
-- 场景：统计每个用户的“订单总数”和“总消费金额”

SELECT 
    u.username, 
    COUNT(o.id) as order_count,  -- 订单数
    IFNULL(SUM(o.amount), 0) as total_amount -- 总金额 (如果为NULL显示0)
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username;

-- 4.3 结果过滤 (HAVING)
-- 场景：找出消费总额超过 200 的用户
-- 区别：WHERE 过滤原始行，HAVING 过滤聚合后的统计结果
SELECT u.username, SUM(o.amount) as total
FROM users u
JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username
HAVING total > 200;

-- 4.4 复杂子查询
-- 场景：找出消费金额最高的那个订单属于谁
SELECT * FROM users 
WHERE id = (
    -- 子查询：先查出金额最高的那笔订单的 user_id
    SELECT user_id FROM orders ORDER BY amount DESC LIMIT 1
);

-- 4.5 日期处理
-- 场景：查询最近 30 天内的订单 (假设当前是动态时间)
SELECT * FROM orders 
WHERE created_at > DATE_SUB(NOW(), INTERVAL 30 DAY);

-- 4.6 窗口函数 (MySQL 8.0+ 特性)
-- 场景：查询每个用户的“最新”一笔订单
-- 原理：按 user_id 分组，按时间倒序排名，取排名第一的
SELECT * FROM (
    SELECT 
        u.username, 
        o.order_no, 
        o.created_at,
        ROW_NUMBER() OVER (PARTITION BY u.id ORDER BY o.created_at DESC) as rn
    FROM users u
    JOIN orders o ON u.id = o.user_id
) as temp_table
WHERE temp_table.rn = 1;

-- ==========================================
-- 5. 索引优化 (进阶)
-- ==========================================

-- 查看查询计划 (EXPLAIN)
-- 在查询前加上 EXPLAIN，MySQL 会告诉你它打算怎么执行这条 SQL
-- 重点看 type (ALL表示全表扫描，不好; ref/range/const 表示用了索引，好)
EXPLAIN SELECT * FROM users WHERE username = '张三';

-- 创建索引 (提升 username 查询速度)
CREATE INDEX idx_username ON users(username);

-- 再次查看计划 (type 应该变好了)
EXPLAIN SELECT * FROM users WHERE username = '张三';

-- 联合索引 (同时按 username 和 email 查询时优化)
CREATE INDEX idx_name_email ON users(username, email);
