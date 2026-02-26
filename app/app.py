from flask import Flask, render_template, request, redirect, url_for, g
import pymysql
import os

app = Flask(__name__)

DB_CONFIG = {
    'host':   os.environ.get('MYSQL_HOST', 'localhost'),
    'user':   os.environ.get('MYSQL_USER', 'bloguser'),
    'password': os.environ.get('MYSQL_PASSWORD', 'blogpassword'),
    'db':     os.environ.get('MYSQL_DB', 'blogdb'),
    'cursorclass': pymysql.cursors.DictCursor
}


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(**DB_CONFIG)
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with db.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        db.commit()


@app.route('/')
def index():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM posts ORDER BY created_at DESC")
        posts = cur.fetchall()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        post = cur.fetchone()
    if not post:
        return "Post not found", 404
    return render_template('post.html', post=post)


@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        db = get_db()
        with db.cursor() as cur:
            cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        db.commit()
        return redirect(url_for('index'))
    return render_template('new_post.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    db.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
