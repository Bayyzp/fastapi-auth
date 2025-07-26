# 🔐 FastAPI Auth REST API (Dockerized)

API ini menyediakan sistem login, register, dan manajemen user berbasis Python (FastAPI) dan MySQL. Sudah termasuk validasi JWT, proteksi endpoint, dan role-based access control. Proyek ini siap produksi dan sudah Dockerized sepenuhnya.

---

## 📦 Fitur

- ✅ Register user baru (`POST /register`)
- 🔐 Login dan generate JWT token (`POST /login`)
-  Lihat profil user login (`GET /me`)
-  Edit profil sendiri (`PATCH /me`)
-  Hapus akun sendiri (`DELETE /me`)
- 🧑‍💼 Admin:
  - Lihat semua user (`GET /admin/users`)
  - Hapus user (`DELETE /admin/users/{id}`)
-  Password di-hash pakai bcrypt
-  JWT-based auth
-  Role-based access: `user` & `admin`

---

## ⚙️ Teknologi

- Python 3.10+
- FastAPI
- SQLAlchemy ORM
- MySQL / MariaDB (via Docker)
- JWT (python-jose)
- bcrypt (passlib)
- Python Dotenv
- Docker + Docker Compose

---

## 🐳 Menjalankan dengan Docker

### 1. Salin `.env` (otomatis sudah disiapkan)

Contoh isi:

```env
DB_HOST=db
DB_PORT=3306
DB_USER=auth_user
DB_PASS=auth_password
DB_NAME=auth_db
SECRET_KEY=your_super_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> `DB_HOST=db` karena service MySQL ada di dalam Docker Compose

---

### 2. Jalankan aplikasi

```bash
docker compose up --build -d
```

- FastAPI → `http://localhost:8000`
- Swagger UI → `http://localhost:8000/docs`
- Redoc → `http://localhost:8000/redoc`

---

## 🔐 Cara Login & Gunakan Bearer Token

1. Login via POST ke `/login`

```json
{
  "username": "admin",
  "password": "admin123"
}
```

2. Dapatkan response:

```json
{
  "access_token": "xxxxx.yyyyy.zzzzz",
  "token_type": "bearer"
}
```

3. Gunakan token di header untuk akses protected route:

```
Authorization: Bearer xxxxx.yyyyy.zzzzz
```

---

## 🧑‍💼 Role-based Access

- Default role saat register: `user`
- Role `admin` bisa mengakses endpoint `/admin/users`
- Kolom `role` disimpan di tabel `users`

---

# 🛡️ Tambah Admin Manual di FastAPI Auth

- Docker container `fastapi_app` harus sudah berjalan.

1. **Masuk ke direktori proyek:**

```bash
cd ~/fastapi-auth
```

2. **(Opsional) Pastikan kontainer sudah berjalan:**

```bash
docker ps
```

3. **Jalankan perintah berikut untuk menambahkan admin:**

```bash
docker exec -it fastapi_app python3 /app/add_admin.py
```

4. **Ikuti petunjuk input:**

```
=== Tambah Admin Baru ===
Username: admin123
Password:
✔️ Admin 'admin123' berhasil ditambahkan.
```

---

## 🧪 Untuk Verifikasi

Coba login via endpoint `/login` menggunakan username dan password admin yang baru.

Gunakan token yang diterima untuk mengakses endpoint yang membutuhkan hak akses admin, misalnya:

```
GET /admin/users
Authorization: Bearer <your_token_here>
```

## 🗃️ Struktur Folder

```
fastapi_auth/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── ...
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🛠️ Untuk Development Lokal (tanpa Docker)

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Buat file `.env` seperti di atas

3. Jalankan dengan Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📜 Lisensi

MIT — Bebas digunakan dan dimodifikasi.

---

## 👤 Dibuat Oleh

> Sistem API login modern berbasis Python FastAPI.  
> Dirancang untuk performa, keamanan, dan kemudahan integrasi.
