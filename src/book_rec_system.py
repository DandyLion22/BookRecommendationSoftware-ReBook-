from datetime import datetime
import hashlib
import time
import networkx as nx


class Book:
    def __init__(self, author, title, genre, publish_year, isbn):
        self.author = author
        self.title = title
        self.genre = genre
        self.publish_year = publish_year
        self.isbn = isbn
        self.ratings = {}
    
    def add_rating(self, user, rating):
        self.ratings[user.alias] = rating

    def get_average_rating(self):
        if not self.ratings:
            return 0
        return sum(self.ratings.values()) / len(self.ratings)

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

class User:
    next_id = 1

    def __init__(self, first_name, last_name, alias, password):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = User.next_id
        User.next_id += 1
        self.alias = alias
        self.password_hash = self.hash_password(password)
        self.favourite_book = {}
        self.favourite_quote = None
        self.favourite_author = None
        self.rated_books = {}
        self.current_book = {}
        self.read_books = {}
        self.friends = []
        self.users_backup = {}
        self.users_backup[self.user_id] = self.alias

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.password_hash == self.hash_password(password)

    def rate_book(self):
        pass

    def get_rated_books(self):
        rated_books_str = f"{self.alias} rated the following books: \n"
        for book, rating in self.rated_books.items():
            rated_books_str += f"{book} -> {rating}\n"
        return rated_books_str
    
    def add_friend(self, friend):
        self.friends.append(friend)

class UserDatabase:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.logged_in = False
        self.graph = nx.Graph()

    def add_user(self, user):
        self.users[user.alias] = user

    def create_profile(self):
        first_n = input("What's your first name? ")
        last_n = input("What's your last name? ")
        while True:
            alias = input("What would you like your nickname to be? ")
            if alias not in self.users:
                break
            print("This nickname is already taken. Please choose another one.") 
        password = input("Choose your password: ")
        new_user = User(first_n, last_n, alias, password)
        new_user.nickname = alias
        self.add_user(new_user)
        self.graph.add_node(new_user.user_id)
        print("Your profile has been created successfully! Another bookworm joined the team!")
        return alias

    def login(self, alias=None):
        counter = 0
        if alias is None:
            while True:
                alias = input("Enter your nickname: ")
                if alias in self.users:
                    break
                print("This nickname is not in our database. Please try again.")
        while True:
            password = input("Enter your password: ")
            counter += 1
            if self.users[alias].check_password(password):
                print("You have successfully logged in!")
                self.current_user = self.users[alias]
                self.logged_in = True
                break
            if counter < 3:
                print("Invalid password. Please try again.")
            else:
                raise LoginFailedException
    
    def logout(self):
        self.current_user = None
        self.logged_in = False
        print("You have successfully logged out.")

    def add_friendship(self, user_alias, friend_alias):
        user = self.users[user_alias]
        friend = self.users[friend_alias]
        user.add_friend(friend)
        self.graph.add_edge(user_alias, friend_alias)

    def see_profile(self):
        user = self.current_user
        print(f"Name: {user.first_name} {user.last_name}")
        print(f"Alias: {user.alias}")
        print(f"Favorite Book: {user.favourite_book}")
        print(f"Favorite Quote: {user.favourite_quote}")
        print(f"Favorite Author: {user.favourite_author}")
        print(f"Current Book: {user.current_book}")
        print("Friends: ")
        for friend in user.friends:
            print(friend.alias) 

    def edit_profile(self):
        while True:
            action = input("What would you like to change? Your favourite book, quote or author? What book you are currently reading? Or your friendslist? Or the books you read so far? Or do you want exit? Type \"favourite book\", \"favourite quote\", \"favourite author\", \"current book\", \"friendslist\", \"books read\", \"exit\" ")
            if action.lower() == "favourite book":
                new_book_title = input("Enter the title of your new favourite book: ")
                new_book_author = input("Enter the author of your new favourite book: ")
                new_book_publication_year = input("Enter the publication year of your new favourite book: ")
                new_book_genre = input("Enter the genre of your new favourite book: ")
                self.current_user.favourite_book = {
                    "title": new_book_title,
                    "author": new_book_author,
                    "publication_year": new_book_publication_year,
                    "genre": new_book_genre
                }
            elif action.lower() == "favourite quote":
                new_quote = input("Enter your new favourite quote: ")
                self.current_user.favourite_quote = new_quote
            elif action.lower() == "favourite author":
                new_author = input("Enter your new favourite author: ")
                self.current_user.favourite_author = new_author
            elif action.lower() == "current book":
                new_book = input("Enter the book you are currently reading: ")
                self.current_user.current_book = new_book
            elif action.lower() == "friendslist":
                while True:
                    new_friend_alias = input("Enter the alias of the new friend you want to add, or type 'exit' to cancel: ")
                    if new_friend_alias.lower() == "exit":
                        print("Action cancelled.")
                        break
                    elif new_friend_alias in self.users:
                        self.add_friendship(self.current_user.alias, new_friend_alias)
                        break
                    else:
                        print("This user does not exist. Please try again.")
            elif action.lower() == "books read":
                new_book_title = input("Enter the title of a book you have read: ")
                new_book_author = input("Enter the author of the book you have read: ")
                self.current_user.read_books[new_book_title] = new_book_author
            elif action.lower() == "exit":
                break
            else:
                print("Invalid choice. Please try again.")



class LoginFailedException(Exception):
    pass

class Rating:
    def __init__(self, user, book, score, timestamp):
        self.user = book.user_id
        self.book = user.title
        if not 1 <= score <= 10:
            raise ValueError("Score must be between 1 and 10")
        self.score = score
        self.timestamp = datetime.now()

    def filter_by(self):
        pass

    def show_ranking(self, library):
        books_with_avg_ratings = [(book.title, book.get_average_rating()) for book in library.books]
        books_with_avg_ratings.sort(key=lambda x: x[1], reverse=True)  

        books_ranking = "All books rankings: \n"
        for rank, (title, avg_rating) in enumerate(books_with_avg_ratings, start=1):
            books_ranking += f"{rank}: {title} -> {avg_rating}\n"
        return books_ranking
    
class RecomEngine:
    def __init__(self, library):
        self.library = library
    
    def recom_by_genre(self):
        pass

    def recom_by_similarity(self):
        pass

    def recom_by_top_rated(self):
        pass

class RatingSystem:
    def __init__(self):
        self.users = {}
        self.books = {}

    def add_user(self, user):
        self.users[user.alias] = user
    
    def add_book(self, book):
        self.books[book.title] = book

    def rate_book(self, user, book, score):
        pass

    def get_recommendations(self, user):
        pass

        

