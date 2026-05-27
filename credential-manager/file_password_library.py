from hashlib import sha256

# Memory to track unlocked files in this session
session_access = {}

def set_file_password(file_name):
    """Set a password for a new credentials file"""
    password = input("Create a password for this employee file: ").strip()
    confirm = input("Confirm password: ").strip()
    if password != confirm:
        print("Passwords do not match. Try again.\n")
        return set_file_password(file_name)
    
    hashed_pass = sha256(password.encode()).hexdigest()
    with open(file_name, "w") as f:
        f.write(f"[PASSWORD]:{hashed_pass}\n")
    print("Password set successfully!\n")
    session_access[file_name] = True
    return hashed_pass

def check_file_password(file_name):
    """Check the password for an existing credentials file"""
    if session_access.get(file_name):
        return True  # already unlocked this session

    try:
        with open(file_name, "r") as f:
            first_line = f.readline().strip()
    except FileNotFoundError:
        print("File not found.")
        return False

    saved_hash = first_line.replace("[PASSWORD]:", "").strip()
    attempt = input("Enter your password to access this file: ").strip()
    attempt_hash = sha256(attempt.encode()).hexdigest()

    if attempt_hash == saved_hash:
        print("Access granted.\n")
        session_access[file_name] = True
        return True
    else:
        print("Incorrect password. Access denied.\n")
        return False
