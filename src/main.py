# Import relevant packages and classes

import os
from pprint import pprint
from colorama import Fore, Back, Style, init
init(autoreset=True)
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
        recom_engine = RecomEngine(main_library.get_book_dicts())
        user_db.load_profiles()


        while True:
            if user_db.logged_in:
                action = input(Fore.GREEN + "Would you like to:\n"
                           + "1. See your profile\n"
                           + "2. Edit your profile\n"
                           + "3. Log out\n"
                           + Fore.BLUE + "Or:\n"
                           + "4. See book rankings\n"
                           + "5. See/edit book ratings or book comments\n"
                           + "6. Receive a book recommendation\n"
                           + "7. Engage on BookMate\n"
                           + Fore.RED + "Or:\n"
                           + "8. Exit\n" + Style.RESET_ALL
                           + "Type the corresponding number or function name: ")
                if action.lower() == "see profile" or action.lower() == "1":
                    user_db.see_profile() 
                elif action.lower() == "edit profile" or action.lower() == "2":
                    user_db.edit_profile()  
                elif action.lower() == "logout" or action.lower() == "3":
                    user_db.logout()
                elif action.lower() == "exit" or action.lower() == "8":
                    break
                elif action.lower() == "see book rankings" or action.lower() == "4":
                    print(main_library.show_ranking())
                elif action.lower() == "see/edit book ratings or book comments" or action.lower() == "5":
                    while True:
                        action = input(Fore.GREEN + "Would you like to:\n"
                    + "1. Rate book\n"
                    + "2. See rating\n"
                    + "3. Comment book\n"
                    + "4. See book comments\n"
                    + Fore.RED + "Or:\n"
                    + "5. Exit\n" + Style.RESET_ALL
                    + "Type the corresponding number or function name: ")
                        if action.lower() == "rate book" or action.lower() == "1":
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
                        elif action.lower() == "see rating" or action.lower() == "2":
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
                        elif action.lower() == "comment book" or action.lower() == "3":
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
                        elif action.lower() == "see book comments" or action.lower() == "4":
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
                        elif action.lower() == "exit" or action.lower() == "5":
                            break
                elif action.lower() == "receive a book recommendation" or action.lower() == "6":
                    while True:
                        action = input(Fore.GREEN + "Would you like to:\n"
                    + "1. Receive recommendation based on genre\n"
                    + "2. Receive recommendation based on rating\n"
                    + "3. Receive a guided recommendation\n"
                    + Fore.RED + "Or:\n"
                    + "4. Exit\n" + Style.RESET_ALL
                    + "Type the corresponding number or function name: ")
                        if action.lower() == "receive recommendation based on genre" or action.lower() == "1":
                            while True:
                                genres = main_library.get_unique_genres()
                                print("Available genres: " + ", ".join(genres))
                                genre = input("Enter your preferred genre or \"exit\" to go back: ")
                                if genre.lower() == "exit":
                                    break
                                elif genre in genres:
                                    recommended_books = recom_engine.recom_by_genre(genre)
                                    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
                                    for i, book in enumerate(recommended_books):
                                        print(colors[i % len(colors)] + book['title'] + '\n')
                                        pprint(book)
                                        print(Style.RESET_ALL) #Color selection for books is based on their index, using modulo operation with the number of colors, causing color repetition if books outnumber colors.
                                else:
                                    print("Genre not found. Please try again.")
                        elif action.lower() == "receive recommendation based on rating" or action.lower() == "2":
                            recommended_books_1 = None
                            recommended_books_2 = None
                            while True:
                                rating_option = input(Fore.GREEN + "Do you want to:\n"
                                    + Fore.YELLOW + "1. " + Fore.CYAN + "See the top-rated books\n"
                                    + Fore.YELLOW + "2. " + Fore.CYAN + "Choose by minimum rating\n"
                                    + Fore.RED + "Or:\n"
                                    + Fore.YELLOW + "3. " + Fore.CYAN + "Exit\n" + Style.RESET_ALL
                                    + "Type the corresponding number or function name: ")
                                if rating_option.lower() == "exit" or rating_option.lower() == "3":
                                    break
                                elif rating_option.lower() == "see the top-rated books" or rating_option.lower() == "1":
                                    try:
                                        num_books = int(input("How many top-rated books do you want to see? "))
                                        recommended_books_1 = recom_engine.recom_by_top_rated(num_books)
                                        colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
                                        if recommended_books_1:
                                            for i, book in enumerate(recommended_books_1):
                                                print(colors[i % len(colors)] + book[0] + ' - Rating: ' + str(book[1]) + '\n')
                                                print(Style.RESET_ALL)
                                    except ValueError:
                                        print("Invalid input. Please enter a number.")
                                elif rating_option.lower() == "choose by minimum rating" or rating_option.lower() == "2":
                                    try:
                                        min_rating = float(input("Enter your minimum preferred rating: "))
                                        recommended_books_2 = recom_engine.recom_by_rating(min_rating)
                                        colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
                                        if recommended_books_2:
                                            for i, book in enumerate(recommended_books_2):
                                                print(colors[i % len(colors)] + book['title'] + '\n')
                                                pprint(book)
                                                print(Style.RESET_ALL)
                                    except ValueError:
                                        print("Invalid input. Please enter a number.")
                                else:
                                    print("Invalid option. Please try again.")
                                    continue

                        elif action.lower() == "receive a guided recommendation" or action.lower() == "3":
                            recom_engine.guided_recommendation()
                        elif action.lower() == "exit" or action.lower() == "4":
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