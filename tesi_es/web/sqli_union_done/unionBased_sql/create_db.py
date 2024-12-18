import mysql.connector
from mysql.connector import errorcode

db_config = {
    'user': 'root',
    'unix_socket': '/var/run/mysqld/mysqld.sock',
    'database': 'naruto_db'
}

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(db_config['database']))
        print("Database created or already exists.")
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def create_tables(cursor):
    tables = {}
    tables['users'] = (
        "CREATE TABLE IF NOT EXISTS `users` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `username` varchar(50) NOT NULL,"
        "  `password` varchar(255) NOT NULL,"
        "  `role` varchar(50) NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    tables['products'] = (
        "CREATE TABLE IF NOT EXISTS `products` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `name` varchar(100) NOT NULL,"
        "  `description` text NOT NULL,"
        "  `price` decimal(10,2) NOT NULL,"
        "  `image` varchar(255) NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

def populate_tables(cursor):
    add_user = ("INSERT INTO users "
                "(username, password, role) "
                "VALUES (%s, %s, %s)")
    data_user = ('admin', 'flag{secret_flag}', 'admin')

    add_product = ("INSERT INTO products "
                   "(name, description, price, image) "
                   "VALUES (%s, %s, %s, %s)")
    data_products = [
        ('Kunai', 'A small throwing knife used by ninjas.', 10.00, 'images/kunai.jpg'),
        ('Shuriken', 'A star-shaped projectile used by ninjas.', 20.00, 'images/shuriken.jpg'),
        ('Explosive Tag', 'A paper tag that explodes after a set amount of time.', 30.00, 'images/explosive_tag.jpg'),
    ]

    cursor.execute(add_user, data_user)
    for data in data_products:
        cursor.execute(add_product, data)

try:
    cnx = mysql.connector.connect(user=db_config['user'], unix_socket=db_config['unix_socket'])
    cursor = cnx.cursor()

    create_database(cursor)

    cnx.database = db_config['database']
    create_tables(cursor)
    populate_tables(cursor)

    cnx.commit()
    cursor.close()
    cnx.close()
except mysql.connector.Error as err:
    print(err)

