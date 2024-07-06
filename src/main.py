# Import relevant packages and classes

import os
from colorama import Fore, Style
from book_rec_system import Book, User, Library, Rating, RatingSystem, RecomEngine, UserDatabase, LoginFailedException
import time

# Clear the terminal screen


# Welcome message and software logo 

print("ReBook - Book Recommendation Software")
print("============================================")
print()
print()
print()

print(Fore.LIGHTCYAN_EX + r"""
.--.     .--.           .    
|   )    |   )          |    
|--' .-. |--:  .-.  .-. |.-. 
|  \(.-' |   )(   )(   )|-.' 
'   ``--''--'  `-'  `-' '  `-
      """ + Style.RESET_ALL)
print()
print()
print()
print("Explore. Discover. Read.")
print("============================================")

# Main loop

def main():
        user_db = UserDatabase()

        while True:
            if user_db.logged_in:
                action = input("Would you like to see your profile, edit your profile, log out, or exit? Type \"see profile\", \"edit profile\", \"logout\", or \"exit\" ")
                if action.lower() == "see profile":
                    user_db.see_profile() 
                elif action.lower() == "edit profile":
                    user_db.edit_profile()  
                elif action.lower() == "logout":
                    user_db.logout()
                elif action.lower() == "exit":
                    break
                else:
                    print("Invalid choice. Please try again.")
            else:
                action = input("Would you like to log in, create a profile, or exit? Type \"login\", \"create profile\", or \"exit\" ")
                if action.lower() == "create profile":
                    user_db.create_profile()
                elif action.lower() == "login":
                    try:
                        user_db.login()
                    except LoginFailedException:
                        print("You tried to log in too many times. Please wait for 10 seconds.")
                        for i in range(10, 0, -1):
                            print(i)
                            time.sleep(1)
                elif action.lower() == "exit":
                    break
                else:
                    print("Invalid choice. Please try again.")


#1: Create a user profile: request personal data, desired nickname...
    



#2: Optionen: 1)Einsicht Bücherranking 2)Bücherbewertung einsehen/abgeben (Score + Kommentar) 3)Bücherempfehlung erhalten 4)BookMates (Social Platform) 5)Eigenes Profil einsehen



if __name__ == "__main__":
    main()


main()