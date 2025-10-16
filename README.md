# category-service

Requires Docker installed and the following executed

```commandline
docker run --name category-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=yourpassword \
  -e POSTGRES_DB=category_db \
  -p 5432:5432 \
  -d postgres:16
```