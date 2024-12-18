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
cursor.execute("CREATE DATABASE IF NOT EXISTS konosuba_shop")

# Use the new database
cursor.execute("USE konosuba_shop")

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    image_url VARCHAR(255)
)
""")

# Insert data into tables
cursor.execute("""
INSERT INTO users (username, password) VALUES
('Wiz', '5f4dcc3b5aa765d61d8327deb882cf99'), -- password
('Vanir', '5f4dcc3b5aa765d61d8327deb882cf99') -- password
""")

cursor.execute("""
INSERT INTO products (name, description, price, image_url) VALUES
('Magic Potion', 'Restores 50 HP', 10.00, 'https://example.com/images/magic_potion.jpg'),
('Mana Elixir', 'Restores 30 MP', 15.00, 'https://example.com/images/mana_elixir.jpg'),
('Teleport Scroll', 'Teleports to a known location', 50.00, 'https://example.com/images/teleport_scroll.jpg')
""")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

print("Database and tables created successfully, and data inserted.")


