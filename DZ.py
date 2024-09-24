import sqlite3


conn = sqlite3.connect('bank.db')
sql = conn.cursor()


sql.execute('''
CREATE TABLE IF NOT EXISTS clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    nomer TEXT NOT NULL UNIQUE,
    balance REAL DEFAULT 0,
    vklad REAL DEFAULT 0
)
''')
conn.commit()


def client_exists(nomer):
    sql.execute('SELECT client_id FROM clients WHERE nomer = ?', (nomer,))
    return sql.fetchone() is not None


def register_client(username, nomer):
    if client_exists(nomer):
        print(f'Клиент с номером {nomer} уже существует.')
    else:
        sql.execute('INSERT INTO clients (username, nomer) VALUES (?, ?)', (username, nomer))
        conn.commit()
        print(f'Клиент {username} успешно зарегистрирован.')

# Функция обновления баланса (пополнение/снятие)
def update_balance(client_id, amount):
    sql.execute('SELECT balance FROM clients WHERE client_id = ?', (client_id,))
    result = sql.fetchone()

    if result is None:
        print(f'Клиент с ID {client_id} не найден.')
    else:
        new_balance = result[0] + amount
        if new_balance < 0:
            print(f'Недостаточно средств для снятия. Баланс: {result[0]}')
        else:
            sql.execute('UPDATE clients SET balance = ? WHERE client_id = ?', (new_balance, client_id))
            conn.commit()
            print(f'Баланс клиента с ID {client_id} успешно обновлен. Новый баланс: {new_balance}')


def view_balance(client_id):
    sql.execute('SELECT balance FROM clients WHERE client_id = ?', (client_id,))
    result = sql.fetchone()

    if result is None:
        print(f'Клиент с ID {client_id} не найден.')
    else:
        print(f'Баланс клиента с ID {client_id}: {result[0]}')


def calculate_deposit(client_id, months):
    sql.execute('SELECT balance FROM clients WHERE client_id = ?', (client_id,))
    result = sql.fetchone()

    if result is None:
        print(f'Клиент с ID {client_id} не найден.')
    else:
        balance = result[0]
        interest_rate = 0.05
        final_amount = balance * (1 + interest_rate) ** (months / 12)
        print(f'Через {months} месяцев сумма составит: {final_amount:.2f} сум.')
        return final_amount


register_client('AKBAR', '+998500035958')  # Регистрация клиента
update_balance(1, 1000000)  # Пополнение баланса
update_balance(1, -4000)  # Снятие средств
view_balance(1)  # Просмотр баланса
calculate_deposit(1, 12)  # Расчет вклада на 12 месяцев


