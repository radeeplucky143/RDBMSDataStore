# RDBMSDataStore
Key-Value data store with advanced functionality supporting CRUD operations.

| Column Name  | Data Type    | Constraints                                          | Description                                                    |
|--------------|--------------|------------------------------------------------------|----------------------------------------------------------------|
| `id`         | `INT`        | `AUTO_INCREMENT PRIMARY KEY`                         | Unique identifier for each record                              |
| `tenant_id`  | `VARCHAR(32)`| `NOT NULL`                                           | Identifier for the tenant                                      |
| `key`        | `VARCHAR(32)`| `NOT NULL UNIQUE`                                    | Unique key for the data                                        |
| `data`       | `TEXT`       | `NOT NULL`                                           | Value associated with the key                                  |
| `ttl`        | `INT`        | `DEFAULT NULL`                                       | Time-to-live for the key-value pair (in seconds)               |
| `created_at` | `TIMESTAMP`  | `DEFAULT CURRENT_TIMESTAMP`                          | Timestamp of when the record was created                       |
| `expiry_time`| `TIMESTAMP`  | `DEFAULT ADDTIME(CURRENT_TIMESTAMP, INTERVAL 7 DAY)` | Expiry time for the entry, defaults to 7 days after creation   |


