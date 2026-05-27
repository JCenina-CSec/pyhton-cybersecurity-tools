import os
# Need to have file_password_library.py in the same Folder as this code.
from file_password_library import set_file_password, check_file_password

# Start of Program

# Display a welcome message to the user
def welcome():
    print("Welcome to Credentials Manager")

# ROT3 Encryption function
def rot3_encrypt(text):
    result = ""
    for char in text:
        if char.isalpha(): #Encrypt Letters
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + 3) % 26 + base)
        elif char.isdigit(): #Encrypt Numbers
            result += str((int(char) + 3) % 10)
        else:
            result += char
    return result

# ROT3 Decryption function
def rot3_decrypt(text):
    result = ""
    for char in text:
        if char.isalpha(): # Decrypt Letters
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - 3) % 26 + base)
        elif char.isdigit(): # Decrypt Numbers
            result += str((int(char) - 3) % 10)
        else:
            result += char
    return result

""" Add Credentials """
def add_credentials(file_name):

    # Check if file exists
    file_exists = os.path.exists(file_name)

    # Add Headings only if file newly created or empty (after password line)
    if not file_exists:
        print("Error: Credentials file missing password header.")
        return
    # Ensure header exists (in case file was manually modified)
    with open(file_name, "r+") as f:
        lines = f.readlines()
        if len(lines) < 3:
            f.seek(0, os.SEEK_END)
            f.write("Username | Password | URL/Resource\n")
            f.write("-------------------------------------------\n")

    #Get Credentials
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    url = input("Enter URL/Resource: ").strip()

    # Encrypt Credentials
    encrypted_user = rot3_encrypt(username)
    encrypted_pass = rot3_encrypt(password)
    encrypted_url = rot3_encrypt(url)

    # Append to credentials.txt
    with open(file_name, "a") as f:
        f.write(f"{encrypted_user:15}|{encrypted_pass:15}|{encrypted_url:25}\n")

    print("\nCredentials Logged successfully")

""" View Credentials"""
def view_credentials(file_name):
    # If no credentials found
    if not os.path.exists(file_name):
        print("No credentials found.")
        return
    
    # Read all lines
    with open(file_name, "r") as f:
        lines = f.readlines()

    # If file only has password, header, and separator but no data
    if len(lines) <= 3:
        print("\nNo stored credentials to display.\n")
        return
    
    # Added to final code, Option to View all Creds or specific Creds
    '''Sub Menu'''
    while True:
        print("\nDo you want to view all credententials or specific credentials?\n")
        print("1. All credentials")
        print("2. Specific credentials")
        print("3. Return to main menu")
        choice = input("\nEnter your choice (1-3): ").strip()
        
        # Choice 1 View All Creds
        if choice == "1":
            print("\nDisplaying All Stored Credentials\n")
            with open(file_name, "r") as f:
                lines = f.readlines()
            # Printing Lines with Header and Line separation
            if len(lines) >= 3:
                print(lines[1].strip()) # Header
                print(lines[2].strip()) # Separator

            # Decrypting Data only and print lines
            for line in lines [3:]:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    decrypt_user = rot3_decrypt(parts[0].strip())
                    decrypt_pass = rot3_decrypt(parts[1].strip())
                    decrypt_url = rot3_decrypt(parts[2].strip())
                    print(f"{decrypt_user:15} | {decrypt_pass:15} | {decrypt_url:25}\n")
            return # Goes back to Main Menu after showing all

        # Choice 2 Specific Creds
        elif choice == "2":  # Moved to submenu to view specific credential via URL/Resource
            url_to_view = input("Enter the URL/Resource you wish to view: ").strip()
            found = False

            for line in lines[3:]: # Skips file password, header and separator
                parts = line.strip().split("|")
                if len(parts) == 3:
                    encrypted_user, encrypted_pass, encrypted_url = parts
                    decrypt_url = rot3_decrypt(encrypted_url)

                    if decrypt_url.lower() == url_to_view.lower():
                        decrypt_user = rot3_decrypt(encrypted_user)
                        decrypt_pass = rot3_decrypt(encrypted_pass)
                        print("\n~~~ Stored Credential ~~~")
                        print(f"Username: {decrypt_user}")
                        print(f"Password: {decrypt_pass}\n")
                        print(f"URL: {decrypt_url}")
                        found = True
                        break
            if not found:
                print("No matching credentials found.")

        # Choice C Return to Main Menu
        elif choice == "3":
            print("\nReturning to Main Menu\n")
            break
        
        # Otherwise
        else:
            print("\nInvalid choice. Please try again.\n")

    

# Option to delete file at end of Program
def delete_file_confirm(file_name):
    # Ask for confirmation before deleting File_Name.txt
    if os.path.exists(file_name):
        print("\nBefore you go,")
        confirm = input(f"\nWould you like to delete {file_name}? \n(y/n): ").strip().lower()
        if confirm == "y": # Confirmation to knowingly delete file
            confirm = input(f"\nFinal warning.\n  \nYou are about to delete {file_name} \n(y/n) ").strip().lower()
            if confirm == "y": # File Deletion
                os.remove(file_name)
                print(f"\n{file_name} deleted successfully. \nGoodbye!")
            else: # File not deleted into Program Close
                print("\nFile kept.\n \nUntil next time.")
        else: # File not deleted into Program Close
            print("\nFile kept.\n  \nUntil next time.")
    else: # Good bye into Program Close
        print("\nGlad to be of help!")

    
# Main Menu
def menu():
    # Display Welcome Message
    welcome()
    
    # Get Employee name and create personalised file name.
    employee_name = input("Please enter your name: ").strip()
    print(f'Welcome, {employee_name}')

    # Create credentials file name
    file_name = f"{employee_name.strip().lower().replace(' ', '')}_credentials.txt"

    # If file does not exist, prompt to create a password
    # Otherwise, verify password before allowing access
    if not os.path.exists(file_name):
        set_file_password(file_name)
    else:
        if not check_file_password(file_name):
            return  # Exit program if password is wrong

    # Main menu Loop
    while True:
        print("\n----------\nMAIN MENU\n----------\nPlease choose an option: ")
        print("1. Add Credentials")
        print("2. View Credentials")
        print("3. Exit Program")

        # Get user choice
        choice = input("\nEnter your choice (1-3): ").strip()
        # If choice is 1. Add new credentials
        if choice == "1":
            # Calls Global function to input, encrypt , and store credentials
            add_credentials(file_name)

        # If choice is 2. View stored credentials
            # Goes to sub-menu
                # Options to 'view all creds', 'specific creds' or 'return to main menu'
        elif choice == "2":
            # Calls Global function to decrypt and display stored credentials
            view_credentials(file_name)

        # If choice is 3. Exit Exit Program
        elif choice == "3":
            # Thanks user
            print(f"\nThanks {employee_name}")
            # Gives option to delete, then exit Loop
            delete_file_confirm(file_name)
            break

        # Invalid input handling
        else:
            print("Invalid input. Please try again.")
# End Loop

# Stop Program

# Main Execution
menu()
