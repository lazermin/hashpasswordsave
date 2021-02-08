import hashlib
import os
import configparser

config = configparser.ConfigParser()  # Создаём объекта парсера
path = 'config.txt'

username = str(input('Введите имя пользователя: '))
password = str(input('Введите пароль: '))


def create_config(path, user, solt, key):
    config = configparser.ConfigParser()
    if not os.path.exists(path):
        config.add_section(user)
        config.set(user, "user", user)
        config.set(user, "solt", solt)
        config.set(user, "key", key)
        with open(path, "w") as config_file:
            config.write(config_file)
        config_file.close()
    else:  # Добавляем в конец или обновляем запись
            config.read(path)
            if config.has_section(user):  # Проверка существования секции
                print('Секция существует! Надо обновить запись.')
                # Написать код обновления
            else:
                print('Секция не найдена. Добавляю запись в конец!')
                config.add_section(user)
                config.set(user, "user", user)
                config.set(user, "solt", solt)
                config.set(user, "key", key)
                with open(path, "a") as config_file:
                    config.write(config_file)
                config_file.close()


def get_config(path, user):
    config = configparser.ConfigParser()
    config.read(path)
    if config.has_section(user):  # Проверка существования секции
        get_user = config.get(user, "user")
        get_solt = config.get(user, "solt")
        get_key = config.get(user, "key")
        return get_user, get_solt, get_key
    else:
        msg1 = 'Такого пользователя не существует!'
        msg2 = 'False'
        return msg1, msg2


salt = os.urandom(32)  # Новая соль для данного пользователя
key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
storage = salt + key

# Получение значений обратно
salt_from_storage = storage[:32]  # 32 является длиной соли
key_from_storage = storage[32:]  # Ключ

create_config(path, username, str(salt_from_storage.hex()), str(key_from_storage.hex()))
#  hex() - преобразовывает объект bytes в его шестнадцатеричное представление


print('Попытка проверки (неправильный пароль)')
username = str(input('Введите имя пользователя: '))
password = str(input('Введите пароль: '))


get_conf_param = get_config(path, username)

if get_conf_param[1] == 'False':
    print(get_conf_param[0])
else:  # Если пользователь существует, то проверяем его пароль
    salt = bytes.fromhex(get_conf_param[1])  # Декодируем строковый объект
    key = bytes.fromhex(get_conf_param[2])
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    if key == new_key:  # Проверка ключей
        print('Пароль совпадает!')
    else:
        print('Пароль неверный!')
