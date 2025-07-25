import bcrypt
import mysql.connector
import getpass

db = mysql.connector.connect(
    host="db",
    user="authuser",
    password="authpass",
    database="authdb"
)

cursor = db.cursor()

print("=== Tambah Admin Baru ===")
username = input("Username: ")
password = getpass.getpass("Password: ")
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

try:
    cursor.execute(
        "INSERT INTO users (username, hashed_password, role) VALUES (%s, %s, 'admin')",
        (username, hashed)
    )
    db.commit()
    print(f"✔️ Admin '{username}' berhasil ditambahkan.")
except mysql.connector.Error as err:
    print("❌ Gagal menambahkan admin:", err)

cursor.close()
db.close()
