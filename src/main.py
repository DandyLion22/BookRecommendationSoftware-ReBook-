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
        main_library = Library()
        main_library.add_real_books()


        while True:
            if user_db.logged_in:
                action = input("Would you like to see your profile, edit your profile, log out, or exit? Or use the main functions: see book rankings, see/edit your book ratings or book comments, receive a book recommendation, engage on BookMate? Type \"see profile\", \"edit profile\", \"logout\", or \"exit\". The other functions are: \"see book rankings\", \"see/edit book ratings\", \"book recommendation\", \"BookMate\".")
                if action.lower() == "see profile":
                    user_db.see_profile() 
                elif action.lower() == "edit profile":
                    user_db.edit_profile()  
                elif action.lower() == "logout":
                    user_db.logout()
                elif action.lower() == "exit":
                    break
                elif action.lower() == "see book rankings":
                    print(main_library.show_ranking())
                elif action.lower() == "see/edit book ratings":
                    while True:
                        action = input("Would you like to rate a book, see a book's rating, comment on a book, or see a book's comments? Type \"rate book\", \"see rating\" ,\"comment book\", \"see book comments\", or \"exit\" to go back. ")
                        if action.lower() == "rate book":
                            while True:
                                title = input("Enter the title of the book you want to rate or \"exit\" to go back: ")
                                if title.lower() == "exit":
                                    break
                                book = main_library.get_book_by_title(title)
                                if book:
                                    rating = float(input("Enter your rating for the book (0 to 10, decimals allowed): "))
                                    user_db.current_user.rate_book(main_library, title, rating)
                                    break
                                else:
                                    print("Book not found. Please try again.")
                        elif action.lower() == "see rating":
                            while True:
                                title = input("Enter the title of the book whose rating you want to see or \"exit\" to go back: ")
                                if title.lower() == "exit":
                                    break
                                book = main_library.get_book_by_title(title)
                                if book:
                                    print(book.get_average_rating())
                                    break
                                else:
                                    print("Book not found. Please try again.")
                        elif action.lower() == "comment book":
                            while True:
                                title = input("Enter the title of the book you want to comment on or \"exit\" to go back: ")
                                if title.lower() == "exit":
                                    break
                                book = main_library.get_book_by_title(title)
                                if book:
                                    comment = input("Enter your comment: ")
                                    user_db.current_user.comment_book(main_library, title, comment)
                                    break
                                else:
                                    print("Book not found. Please try again.")
                        elif action.lower() == "see book comments":
                            while True:
                                title = input("Enter the title of the book you want to see comments for or \"exit\" to go back: ")
                                if title.lower() == "exit":
                                    break
                                book = main_library.get_book_by_title(title)
                                if book:
                                    print(book.get_comments())
                                    break
                                else:
                                    print("Book not found. Please try again.")
                        elif action.lower() == "exit":
                            break

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