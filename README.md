# RDBMSDataStore
Key-value data store with advanced functionality supporting CRUD operations.



### Installing PostgreSQL on Ubuntu/Debian

1. **Update Package Index**:
   ```bash
   sudo apt update
   ```

2. **Install PostgreSQL**:
   ```bash
   sudo apt install postgresql postgresql-contrib
   ```

3. **Start and Enable PostgreSQL Service**:
   ```bash
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

4. **Check PostgreSQL Status**:
   ```bash
   sudo systemctl status postgresql
   ```

5. **Switch to the PostgreSQL User**:
   By default, PostgreSQL creates a user named `postgres`. Switch to this user to manage the database:
   ```bash
   sudo -i -u postgres
   ```

6. **Access PostgreSQL Prompt**:
   ```bash
   psql
   ```

7. **Exit PostgreSQL Prompt**:
   To exit the prompt, type:
   ```sql
   \q
   ```

### Post-Installation Steps

1. **Create a New Role**: After accessing the PostgreSQL prompt, you may want to create a new user role:
   ```sql
   CREATE ROLE radeep WITH LOGIN PASSWORD 'ViratKohli#18';
   ```

2. **Create a Database**: You can also create a new database:
   ```sql
   CREATE DATABASE DataStore WITH OWNER radeep;
   ```

3. **Adjusting Authentication**: By default, PostgreSQL uses "peer" authentication. You might need to adjust the `pg_hba.conf` file located in `/etc/postgresql/<version>/main/` (Ubuntu) or `/var/lib/pgsql/<version>/data/` (CentOS/RHEL) to set up password authentication.

4. **Accessing PostgreSQL Remotely**: If you want to allow remote connections, you'll need to adjust the `postgresql.conf` and `pg_hba.conf` files to allow access and update the firewall settings accordingly.

### Conclusion

After following these steps, you should have a working installation of PostgreSQL on your Linux machine. If you have any specific questions or run into issues, feel free to ask!




| Column Name  | Data Type    | Constraints                                          | Description                                                    |
|--------------|--------------|------------------------------------------------------|----------------------------------------------------------------|
| `id`         | `INT`        | `AUTO_INCREMENT PRIMARY KEY`                         | Unique identifier for each record                              |
| `tenant_id`  | `VARCHAR(32)`| `NOT NULL`                                           | Identifier for the tenant                                      |
| `key`        | `VARCHAR(32)`| `NOT NULL UNIQUE`                                    | Unique key for the data                                        |
| `data`       | `TEXT`       | `NOT NULL`                                           | Value associated with the key                                  |
| `ttl`        | `INT`        | `DEFAULT NULL`                                       | Time-to-live for the key-value pair (in seconds)               |
| `created_at` | `TIMESTAMP`  | `DEFAULT CURRENT_TIMESTAMP`                          | Timestamp of when the record was created                       |
| `expiry_time`| `TIMESTAMP`  | `DEFAULT ADDTIME(CURRENT_TIMESTAMP, INTERVAL 7 DAY)` | Expiry time for the entry, defaults to 7 days after creation   |


