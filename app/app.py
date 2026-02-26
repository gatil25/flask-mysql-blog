from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# MySQL configuration from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'bloguser')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'blogpassword')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'blogdb')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


def init_db():
    """Create the posts table if it doesn't exist."""
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        mysql.connection.commit()
        cur.close()


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cur.fetchall()
    cur.close()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cur.fetchone()
    cur.close()
    if not post:
        return "Post not found", 404
    return render_template('post.html', post=post)


@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('new_post.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
