from auth import register_user, login_user
from security_analysis import compare_algorithms
import getpass
import os
from password_policy import validate_password

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("="*40)
    print("    PASSWORD SECURITY SYSTEM")
    print("="*40)

def register_flow():
    """
    Handles registration with 3 password attempts before restarting.
    """
    while True:
        username = input("Enter username: ").strip()
        attempts = 0
        while attempts < 3:
            password = getpass.getpass("Enter password: ")
            policy_check = validate_password(password)
            if policy_check == "Valid":
                register_user(username, password)
                return
            else:
                attempts += 1
                print(f"Invalid password ({attempts}/3): {policy_check}")

        # If user fails 3 times, restart registration
        print("Too many failed attempts. Restarting registration...")

def main():
    while True:
        clear_screen()
        print_banner()
        print("1. Register a new account")
        print("2. Login to your account")
        print("3. Security Analysis (Hash Comparison)")
        print("4. Exit")
        print("-"*40)

        choice = input("Choose an option [1-4]: ").strip()

        if choice == "1":
            register_flow()
            input("\nPress Enter to continue...")

        elif choice == "2":
            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter password: ")
            login_user(username, password)
            input("\nPress Enter to continue...")

        elif choice == "3":
            password = getpass.getpass("Enter password to test hashing algorithms: ")
            compare_algorithms(password)
            input("\nPress Enter to continue...")

        elif choice == "4":
            print("Goodbye! Stay secure!")
            break

        else:
            print("Invalid choice! Please enter 1-4.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()