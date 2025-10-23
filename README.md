# Category Service

A clean and simple backend API for managing a **hierarchical category tree** with **bidirectional similarity** relationships between categories.  
Designed for clarity, reliability and just-enough engineering — built with **Django 4.2**, **Django REST Framework**, and **PostgreSQL**.

---

## 🚀 Features

- Nested categories with unlimited depth
- CRUD operations for categories and similarities
- Move categories within the tree (reparenting)
- Filter categories by:
  - Parent
  - Depth
  - Subtree of a given node
  - Ancestors of a node
  - Search by name
- Bidirectional category similarity (A ↔ B)
- Rabbit-hole analysis:
  - **Longest rabbit hole** — the longest shortest path between similar categories
  - **Rabbit islands** — connected components of similar categories
- Django Admin integration
- PostgreSQL + `.env` config
- Optional OpenAPI/Swagger docs

---

## 🧱 Tech Stack

- Python 3.12+
- Django 4.2
- Django REST Framework
- PostgreSQL
- python-dotenv
- (optional) drf-spectacular for API docs

---

## ⚙️ Setup

### 1. Clone and install dependencies
```bash
git clone https://github.com/Zarrie/category-service.git
cd category-service
python -m venv venv
source venv/bin/activate     # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

### 2. Requires Docker installed and the following executed

```commandline
docker run --name category-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=yourpassword \
  -e POSTGRES_DB=category_db \
  -p 5432:5432 \
  -d postgres:16
```

### 3. Configure environment

Create a .env file in the project root:

```commandline
DEBUG=True
SECRET_KEY=your_secret_key_here
DB_NAME=category_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### 4. Run migrations and start server
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🐇 Rabbit Analysis Script

```commandline
python manage.py rabbits
```

### Clear, Generate and Run with test data

```commandline
python manage.py shell -c "from categories.models import Category, CategorySimilarity as S; S.objects.all().delete(); Category.objects.all().delete(); print('cleared')"
python manage.py shell -c "import create_test_data; create_test_data.run()"
python manage.py rabbits
```