import csv

USER_DATA_FILE = 'users.csv'

def is_email_registered(email):
    with open(USER_DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['email'] == email:
                return True
    return False

def register_user(email, password):
    if is_email_registered(email):
        return False
    with open(USER_DATA_FILE, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([email, password])
    return True

def authenticate_user(email, password):
    with open(USER_DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['email'] == email and row['password'] == password:
                return True
    return False
