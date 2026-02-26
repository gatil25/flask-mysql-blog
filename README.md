# 🐳 Docker Blog

A beginner-friendly multi-container blog application built with **Flask**, **MySQL**, and **Docker Compose**.

## 📦 Tech Stack

| Service | Technology |
|---------|-----------|
| Web App | Python + Flask |
| Database | MySQL 8.0 |
| Containers | Docker + Docker Compose |

## 🗂️ Project Structure

```
docker-blog/
├── docker-compose.yml       # Defines both containers
├── app/
│   ├── Dockerfile           # Builds the Flask container
│   ├── requirements.txt     # Python dependencies
│   ├── app.py               # Flask application
│   └── templates/
│       ├── base.html        # Shared layout
│       ├── index.html       # Post listing page
│       ├── post.html        # Single post page
│       └── new_post.html    # Create post form
```

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

### Run the App

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/docker-blog.git
cd docker-blog

# 2. Start both containers
docker compose up --build

# 3. Open your browser
# Visit: http://localhost:5000
```

### Stop the App

```bash
docker compose down
```

To also remove the database volume (deletes all posts):
```bash
docker compose down -v
```

## ✨ Features

- View all blog posts on the homepage
- Read individual posts
- Write and publish new posts
- Delete posts
- Data is persisted in a MySQL database across restarts

## 🧠 How It Works

`docker-compose.yml` spins up two containers:

1. **`db`** — A MySQL container that stores blog posts. Data is saved in a Docker volume so it persists even if you restart.
2. **`web`** — A Flask container that serves the blog. It connects to `db` using the service name as the hostname (Docker networking handles this automatically).

The `web` container waits for `db` to be healthy before starting, using Docker Compose's `depends_on` with a `healthcheck`.

## 📚 Learn More

- [Docker Getting Started Guide](https://docs.docker.com/get-started/)
- [Docker Compose Overview](https://docs.docker.com/compose/)
- [Flask Documentation](https://flask.palletsprojects.com/)
