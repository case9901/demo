import mysql.connector

# Database configuration using auth_socket
db_config = {
    'user': 'root',
    'unix_socket': '/var/run/mysqld/mysqld.sock'  # Path to MySQL socket
}

# Create a new database connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create the database
cursor.execute("CREATE DATABASE IF NOT EXISTS san_magnolia")

# Use the new database
cursor.execute("USE san_magnolia")

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    secret VARCHAR(255)
)
""")

# Insert data into tables
cursor.execute("""
INSERT INTO users (username, password, secret) VALUES
('BloodyRegina', 'reginapass', 'JBSWY3DPEHPK3PXP'), -- Secret for OTP
('undertaker', 'undertakerpass', 'KBQW5Y3AEBG6PXPQ')
""")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

print("Database setup complete.")
