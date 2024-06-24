from datetime import datetime
import hashlib



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
        self.favourite_books = {}
        self.rated_books = {}
        self.current_book = {}
        self.read_books = {}
        self.users = {}
        self.users[self.user_id] = self.alias

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
    
class UserDatabase:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.user_id] = user

    def create_profile(user_db):
        first_n = input("What's your first name? ")
        last_n = input("What's your last name? ")
        while True:
            nickn = input("What would you like your nickname to be? ")
            if nickn not in user_db.users:
                break
            print("This nickname is already taken. Please choose another one.") 
        password = input("Enter your password: ")
        new_user = User(first_n, last_n, nickn, password)
        user_db.add_user(new_user)
        print("Your profile has been created successfully! Another bookworm joined the team!")
        return nickn

    def login(user_db, alias=None):
        if alias is None:
            while True:
                alias = input("Enter your nickname: ")
                if alias in user_db.users:
                    break
                print("This nickname is not in our database. Please try again.")
        while True:
            password = input("Enter your password: ")
            if user_db.users[alias].check_password(password):
                print("You have successfully logged in!")
                break
            print("Invalid password. Please try again.")

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

        

