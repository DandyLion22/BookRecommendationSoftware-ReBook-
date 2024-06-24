# Import relevant packages and classes

import os
from colorama import Fore, Style
from book_rec_system import Book, User, Library, Rating, RatingSystem, RecomEngine, UserDatabase

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
    pass

#1: Create a user profile: request personal data, desired nickname...
    while True:
        signup_or_in = input("Would you like to log in or create a profile? Type \"login\" or \"create profile\" ")
        user_db = UserDatabase()


        if signup_or_in.lower() == "create profile":
            alias = user_db.create_profile()
            user_db.login(alias)
        elif signup_or_in.lower() == "login":
            user_db.login(user_db)
        else:
            print("Invalid choice. Please try again.")



#2: Optionen: 1)Einsicht Bücherranking 2)Bücherbewertung einsehen/abgeben (Score + Kommentar) 3)Bücherempfehlung erhalten 4)BookMates (Social Platform) 5)Eigenes Profil einsehen



if __name__ == "__main__":
    main()


main()