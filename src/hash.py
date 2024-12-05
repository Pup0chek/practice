import hashlib
import os

def hash_password(password):
    # Генерируем случайную соль
    salt = os.urandom(16)  # 16 байт (128 бит) - стандартный размер соли
    # Конкатенируем пароль и соль и хешируем результат
    hash_object = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    # Возвращаем соль и хеш в виде пары (salt, hash)
    return salt, hash_object

def verify_password(stored_password, stored_salt, provided_password):
    # Хешируем предоставленный пароль с той же солью
    hash_object = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), stored_salt, 100000)
    # Сравниваем хеши
    return hash_object == stored_password

# Пример использования:
password = 'my_secure_password'
salt, hashed_password = hash_password(password)

print(f"Salt: {salt.hex()}")
print(f"Hashed Password: {hashed_password.hex()}")

# Проверка пароля
is_valid = verify_password(hashed_password, salt, 'my_secure_password')
print(f"Password is valid: {is_valid}")

is_valid_wrong = verify_password(hashed_password, salt, 'wrong_password')
print(f"Password is valid: {is_valid_wrong}")