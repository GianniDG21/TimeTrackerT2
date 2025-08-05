#data.py
#File di managing dati
import json

#=====USER FUNCTIONS=====
def save_user(user_list):
    with open('users.txt', 'w') as f:
        for user in user_list:
            f.write(user + '\n')

def load_user():
    try:
        with open('users.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []
    
#=====SUBJECT FUNCTIONS=====
def save_subjects(subjects_list):
    with open('subjects.json', 'w') as f:
        json.dump(subjects_list, f, indent=4)

def load_subjects(user):
    try:
        with open('subjects.json', 'r') as f:
            subjects = json.load(f)
            return subjects.get(user, [])
    except FileNotFoundError:
        return []