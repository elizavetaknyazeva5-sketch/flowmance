import requests
from sqlalchemy import create_engine, inspect
from app.core.config import DATABASE_URL

# 1️⃣ Проверяем таблицы в базе
engine = create_engine(DATABASE_URL)
inspector = inspect(engine)
tables = inspector.get_table_names()
print("Таблицы в базе:", tables)

if "users" not in tables:
    print("⚠️ Таблица 'users' не найдена! Запусти init_db.py")
else:
    print("✅ Таблица 'users' есть")

# 2️⃣ Проверяем регистрацию и логин
BASE_URL = "http://127.0.0.1:8001"

# регистрация
reg_data = {"email":"test@example.com","password":"12345678"}
r = requests.post(f"{BASE_URL}/auth/register", json=reg_data)
print("Регистрация:", r.status_code, r.json() if r.status_code==200 else r.text)

# логин
login_data = {"username":"test@example.com","password":"12345678"}
r = requests.post(f"{BASE_URL}/auth/jwt/login", data=login_data)
if r.status_code == 200:
    token = r.json().get("access_token")
    print("✅ Логин успешен, JWT:", token)
else:
    print("⚠️ Логин не удался:", r.text)
    token = None

# 3️⃣ Проверяем защищённый роут
if token:
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/protected", headers=headers)
    print("Доступ к /protected:", r.status_code, r.json() if r.status_code==200 else r.text)
