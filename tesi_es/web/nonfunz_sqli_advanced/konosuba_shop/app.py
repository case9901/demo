from flask import Flask, request, render_template_string, redirect, url_for
import pymysql

app = Flask(__name__)

# Database configuration
db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='konosuba_shop',
    unix_socket='/var/run/mysqld/mysqld.sock'
)

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT id, name, description, price, image_url FROM products")
    products = cursor.fetchall()
    return render_template_string("""
        <h1>Welcome to Wiz and Vanir's Magical Shop</h1>
        <ul>
        {% for product in products %}
            <li>
                <img src="{{ product[4] }}" alt="{{ product[1] }}" width="100"><br>
                <strong>{{ product[1] }}</strong><br>
                {{ product[2] }}<br>
                Price: {{ product[3] }} gold<br>
                <a href="/product/{{ product[0] }}">View Details</a>
            </li>
        {% endfor %}
        </ul>
        <a href="/login">Login</a>
    """, products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    cursor = db.cursor()
    cursor.execute("SELECT name, description, price, image_url FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    return render_template_string("""
        <h1>{{ product[0] }}</h1>
        <img src="{{ product[3] }}" alt="{{ product[0] }}" width="200"><br>
        <p>{{ product[1] }}</p>
        <p>Price: {{ product[2] }} gold</p>
        <a href="/">Back to shop</a>
    """, product=product)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        # Simulate SQL injection vulnerability
        sql_query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(sql_query)
        user = cursor.fetchone()
        if user:
            return redirect(url_for('flag'))
        else:
            return "Login failed"
    return render_template_string("""
        <h1>Login</h1>
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    """)

@app.route('/flag')
def flag():
    return render_template_string("""
        <h1>Congratulations!</h1>
        <p>Here is your flag: CTF{magical_shop_flag}</p>
    """)

if __name__ == '__main__':
    app.run(debug=True)




