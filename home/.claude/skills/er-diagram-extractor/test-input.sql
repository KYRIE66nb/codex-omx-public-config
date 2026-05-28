-- 测试场景：旅游景点管理系统数据库
-- 目的：测试 agent 在没有 skill 时如何处理表分类和关系抽取

CREATE TABLE scenic_spot (
    id BIGINT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description LONGTEXT,
    location VARCHAR(200),
    ticket_price DOUBLE,
    addtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tourist (
    id BIGINT PRIMARY KEY,
    username VARCHAR(200) NOT NULL,
    password VARCHAR(200),
    email VARCHAR(200),
    phone VARCHAR(50),
    addtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE booking (
    id BIGINT PRIMARY KEY,
    tourist_id BIGINT,
    scenic_spot_id BIGINT,
    booking_date DATE,
    visit_date DATE,
    ticket_quantity INT,
    total_price DOUBLE,
    status VARCHAR(50),
    addtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tourist_id) REFERENCES tourist(id),
    FOREIGN KEY (scenic_spot_id) REFERENCES scenic_spot(id)
);

CREATE TABLE review (
    id BIGINT PRIMARY KEY,
    tourist_id BIGINT,
    scenic_spot_id BIGINT,
    rating INT,
    comment LONGTEXT,
    addtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tourist_id) REFERENCES tourist(id),
    FOREIGN KEY (scenic_spot_id) REFERENCES scenic_spot(id)
);

CREATE TABLE tourist_favorite (
    tourist_id BIGINT,
    scenic_spot_id BIGINT,
    addtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (tourist_id, scenic_spot_id),
    FOREIGN KEY (tourist_id) REFERENCES tourist(id),
    FOREIGN KEY (scenic_spot_id) REFERENCES scenic_spot(id)
);
