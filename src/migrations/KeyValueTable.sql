CREATE TABLE key_value_store (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id VARCHAR(32) NOT NULL,
    key VARCHAR(32) NOT NULL,
    data TEXT NOT NULL,
    size INT NOT NULL
    ttl INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_time TIMESTAMP DEFAULT ADDTIME(CURRENT_TIMESTAMP(), INTERVAL 7 DAY),
    UNIQUE KEY unique_tenant_key (tenant_id, key)
);
