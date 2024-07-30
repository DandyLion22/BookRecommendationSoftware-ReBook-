from datetime import datetime
import hashlib
import time
import networkx as nx
import random
import string
import heapq


class Book:
    def __init__(self, author, title, genre, publish_year, isbn, topics, length, complexity, purpose, mood, average_rating):
        self.author = author
        self.title = title
        self.genre = genre
        self.publish_year = publish_year
        self.isbn = isbn
        self.ratings = {}
        self.average_rating = average_rating
        self.comments = []
        self.topics = topics
        self.length = length
        self.complexity = complexity
        self.purpose = purpose
        self.mood = mood
    
    def add_rating(self, user, rating):
        self.ratings[user.alias] = rating

    def add_comment(self, user_alias, comment):
        self.comments.append({"user": user_alias, "comment": comment})

    def get_average_rating(self):
        return self.average_rating
    
    def get_comments(self):
        return self.comments
    
    def get_title(self):
        return self.title

    def rate_book(self, user_alias, rating):
        self.ratings[user_alias] = rating
        self.average_rating = sum(self.ratings.values()) / len(self.ratings)
    
class Library:
    def __init__(self):
        self.book_dicts = []  # list to store book dictionaries
        self.books = []  # list to store Book objects

    def add_book(self, book):
        self.books.append(book)

    def add_real_books(self):
        real_books = [
            {'author': 'J.K. Rowling', 'title': 'Harry Potter and the Philosopher\'s Stone', 'genre': 'Fantasy', 'year': 1997, 'topics': ['Magic', 'Coming of Age'], 'length': 'Long', 'complexity': 'Medium', 'purpose': 'Entertainment', 'mood': 'Exciting'},
            {'author': 'George R.R. Martin', 'title': 'A Game of Thrones', 'genre': 'Fantasy', 'year': 1996, 'topics': ['Politics', 'War'], 'length': 'Long', 'complexity': 'High', 'purpose': 'Entertainment', 'mood': 'Dark'},
            {'author': 'J.R.R. Tolkien', 'title': 'The Hobbit', 'genre': 'Fantasy', 'year': 1937, 'topics': ['Adventure', 'Mythology'], 'length': 'Medium', 'complexity': 'Medium', 'purpose': 'Entertainment', 'mood': 'Adventurous'},
            {'author': 'Agatha Christie', 'title': 'Murder on the Orient Express', 'genre': 'Mystery', 'year': 1934, 'topics': ['Crime', 'Detective'], 'length': 'Short', 'complexity': 'Low', 'purpose': 'Entertainment', 'mood': 'Suspenseful'},
            {'author': 'Stephen King', 'title': 'The Shining', 'genre': 'Horror', 'year': 1977, 'topics': ['Supernatural', 'Psychology'], 'length': 'Long', 'complexity': 'High', 'purpose': 'Entertainment', 'mood': 'Terrifying'},
            {'author': 'Isaac Asimov', 'title': 'Foundation', 'genre': 'Science Fiction', 'year': 1951, 'topics': ['Technology', 'Future'], 'length': 'Medium', 'complexity': 'High', 'purpose': 'Learning', 'mood': 'Intriguing'},
            {'author': 'Jane Austen', 'title': 'Pride and Prejudice', 'genre': 'Romance', 'year': 1813, 'topics': ['Society', 'Marriage'], 'length': 'Medium', 'complexity': 'Medium', 'purpose': 'Entertainment', 'mood': 'Romantic'},
            {'author': 'Mark Twain', 'title': 'The Adventures of Tom Sawyer', 'genre': 'Adventure', 'year': 1876, 'topics': ['Youth', 'Friendship'], 'length': 'Short', 'complexity': 'Low', 'purpose': 'Entertainment', 'mood': 'Fun'},
            {'author': 'Ernest Hemingway', 'title': 'The Old Man and the Sea', 'genre': 'Fiction', 'year': 1952, 'topics': ['Nature', 'Aging'], 'length': 'Short', 'complexity': 'Medium', 'purpose': 'Entertainment', 'mood': 'Melancholic'},
            {'author': 'F. Scott Fitzgerald', 'title': 'The Great Gatsby', 'genre': 'Fiction', 'year': 1925, 'topics': ['Wealth', 'American Dream'], 'length': 'Short', 'complexity': 'Medium', 'purpose': 'Entertainment', 'mood': 'Reflective'}
        ]

        for book in real_books:
            isbn = ''.join(random.choice('1234567890') for _ in range(13))  # Generate a random 13-digit ISBN
            book['isbn'] = isbn
            book['ratings'] = {"User1": random.randint(0, 10)}  # Initialize ratings as a dictionary with an initial randomized value
            average_rating = sum(book['ratings'].values()) / len(book['ratings']) if book['ratings'] else 0
            book['average_rating'] = average_rating
            book['comments'] = []  # Initialize comments as an empty list
            self.book_dicts.append(book)

            new_book = Book(book['author'], book['title'], book['genre'], book['year'], isbn, book["topics"], book["length"], book["complexity"], book["purpose"], book["mood"], average_rating)
            self.books.append(new_book)


    def show_ranking(self):
        # Create a max heap with the negative average ratings as the priorities
        heap = [(-sum(book['ratings'].values()) / len(book['ratings']) if book['ratings'] else 0, book['title']) for book in self.book_dicts]
        heapq.heapify(heap)

        books_ranking = "All books rankings: \n"
        rank = 1
        while heap:
            avg_rating, title = heapq.heappop(heap)
            books_ranking += f"{rank}: {title} -> {-avg_rating}\n"  # Negate the average rating to get the original value
            rank += 1

        return books_ranking
    
    
    def get_book_by_title(self, title):
        for book in self.books:
            if book.get_title() == title:
                return book
        return None
    
    def get_book_dicts(self):
        return self.book_dicts
    
    def get_unique_genres(self):
        genres = set()
        for book in self.books:
            genres.add(book.genre)
        return list(genres)

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
        self.disliked_books = {}
        self.users_backup = {}
        self.users_backup[self.user_id] = self.alias
        

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.password_hash == self.hash_password(password)

    def rate_book(self, library, title, rating):
        for book in library.books:
            if book.get_title() == title:
                book.rate_book(self.alias, rating)
                break

        for book_dict in library.book_dicts:
            if book_dict['title'] == title:
                book_dict['ratings'][self.alias] = rating
                book_dict['average_rating'] = sum(book_dict['ratings'].values()) / len(book_dict['ratings'])
                break

    def comment_book(self, library, title, comment):
        for book in library.books:
            if book.get_title() == title:
                book.add_comment(self.alias, comment)
                break

        for book_dict in library.book_dicts:
            if book_dict['title'] == title:
                book_dict["comments"].append({"user": self.alias, "comment": comment})
                break

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
    
class RecomEngine:
    def __init__(self, library):
        self.library = library
        self.heap = self.create_heap()

    def create_heap(self):
    # Create a max heap with the negative average ratings as the priorities
        heap = [(-sum(book['ratings'].values()) / len(book['ratings']) if book['ratings'] else 0, book['title'], book) for book in self.library]
        heapq.heapify(heap)
        return heap
    
    def recom_by_genre(self, genre):
        return [book for book in self.library if book['genre'] == genre]

    def recom_by_similarity(self):
        pass

    def recom_by_top_rated(self, n):
    # Return the top n books
        top_books = []
        for _ in range(n):
            if not self.heap:
                break
            avg_rating, title, book = heapq.heappop(self.heap)
            top_books.append((title, -avg_rating))
        return top_books
        

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

        

