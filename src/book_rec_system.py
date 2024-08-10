from datetime import datetime
import hashlib
import time
import networkx as nx
import random
import string
import heapq
from rich import print
from rich.table import Table
from colorama import Fore, Back, Style, init
import json


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
    
    def get_ratings(self):
        ratings = list()
        for book in self.books:
            ratings.add(book.average_rating)
        return ratings

class User:
    next_id = 1

    def __init__(self, first_name, last_name, alias, password=None, password_hash=None):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = User.next_id
        User.next_id += 1
        self.alias = alias
        if password_hash is not None:
            self.password_hash = password_hash
        else:
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
        return self.hash_password(password) == self.password_hash

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
        self.save_profiles()
        return alias

    def save_profiles(self):
        profiles = []
        for user in self.users.values():
            profile = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'alias': user.alias,
                'password_hash': user.password_hash,
                'favourite_book': user.favourite_book,
                'favourite_quote': user.favourite_quote,
                'favourite_author': user.favourite_author,
                'rated_books': user.rated_books,
                'current_book': user.current_book,
                'read_books': user.read_books,
                'friends': [friend.alias for friend in user.friends],
                'disliked_books': user.disliked_books,
                'users_backup': user.users_backup
            }
            profiles.append(profile)
        
        with open('profiles.json', 'w') as f: 
            json.dump(profiles, f)

    def load_profiles(self):
        try:
            with open('profiles.json', 'r') as f:
                profiles = json.load(f)
        except FileNotFoundError:
            profiles = []

        for profile in profiles:
            password_hash = profile.get('password_hash')
            if password_hash is None:
                print(f"Warning: profile for {profile['alias']} does not have a password hash. Skipping this profile.")
                continue
            user = User(profile['first_name'], profile['last_name'], profile['alias'], password_hash=password_hash)
            user.favourite_book = profile.get('favourite_book')
            user.favourite_quote = profile.get('favourite_quote')
            user.favourite_author = profile.get('favourite_author')
            user.rated_books = profile.get('rated_books')
            user.current_book = profile.get('current_book')
            user.read_books = profile.get('read_books')
            user.friends = profile.get('friends', [])
            user.disliked_books = profile.get('disliked_books')
            user.users_backup = profile.get('users_backup')
            self.add_user(user)
            self.graph.add_node(user.user_id)


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
            input_password_hash = self.users[alias].hash_password(password)
            if input_password_hash == self.users[alias].password_hash:
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
        user.friends.append(friend)
        self.graph.add_edge(user_alias, friend_alias)
    
    def remove_friendship(self, user_alias, friend_alias):
        user = self.users[user_alias]
        friend = self.users[friend_alias]
        user.friends.remove(friend)
        self.graph.remove_edge(user_alias, friend_alias)

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
            from colorama import Fore, Style

            action = input(Fore.GREEN + "What would you like to change?\n"
                           "1. Your favourite book\n"
                           "2. Your favourite quote\n"
                           "3. Your favourite author\n"
                           "4. What book you are currently reading\n"
                           "5. Your friendslist\n"
                           "6. The books you read so far\n"
                           + Fore.RED +
                           "7. Or do you want exit?\n" + Style.RESET_ALL +
                           "Type the corresponding number: ")

            if action == "1" or action.lower() == "your favourite book":
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
                self.save_profiles()
            elif action == "2" or action.lower() == "your favourite quote":
                new_quote = input("Enter your new favourite quote: ")
                self.current_user.favourite_quote = new_quote
                self.save_profiles()
            elif action == "3" or action.lower() == "your favourite author":
                new_author = input("Enter your new favourite author: ")
                self.current_user.favourite_author = new_author
                self.save_profiles()
            elif action == "4" or action.lower() == "what book you are currently reading":
                new_book = input("Enter the book you are currently reading: ")
                self.current_user.current_book = new_book
                self.save_profiles()
            elif action == "5" or action.lower() == "your friendslist":
                while True:
                    choice = input("Do you want to add a friend, delete a friend, view your friend list, or exit? Type 'add', 'delete', 'view', or 'exit': ")
                    if choice.lower() == "exit":
                        print("Action cancelled.")
                        break
                    elif choice.lower() == "add":
                        new_friend_alias = input("Enter the alias of the new friend you want to add: ")
                        if new_friend_alias in self.users:
                            self.add_friendship(self.current_user.alias, new_friend_alias)
                            self.save_profiles()
                            break
                        else:
                            print("This user does not exist. Please try again.")
                    elif choice.lower() == "delete":
                        friend_alias = input("Enter the alias of the friend you want to delete: ")
                        if friend_alias in self.current_user.friends:
                            self.remove_friendship(self.current_user.alias, friend_alias)
                            self.save_profiles()
                            break
                        else:
                            print("This user is not in your friends list. Please try again.")
                    elif choice.lower() == "view":
                        print("Your current friends are: ")
                        for friend in self.current_user.friends:
                            print(friend.alias)
                    else:
                        print("Invalid choice. Please try again.")
            elif action == "6" or action.lower() == "the books you read so far":
                new_book_title = input("Enter the title of a book you have read: ")
                new_book_author = input("Enter the author of the book you have read: ")
                self.current_user.read_books[new_book_title] = new_book_author
            elif action == "7" or action.lower() == "exit":
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

    def guided_recommendation(self):
        # Initialize scores
        scores = {book['title']: 0 for book in self.library}

        # Define the questions and the attributes they correspond to
        questions = [
            ("genre", "What is your preferred genre?"),
            ("length", "What is your preferred length?"),
            ("topics", "What is your preferred topic?"),
            ("complexity", "What is your preferred complexity?"),
            ("author", "What is your preferred author?"),
            ("purpose", "What is your reading purpose?"),
            ("mood", "What is your preferred mood?"),
            ("average_rating", "What is your preferred minimum rating?"),
            ("year", "What is your preferred minimum publishing year?")
            # Add more questions here
        ]

        for attribute, question in questions:
            if attribute in ["average_rating", "year"]:
                # For rating and year, ask for a minimum value
                answer = float(input(question))
                for book in self.library:
                    if book[attribute] >= answer:
                        scores[book['title']] += 1
            else:
                # For other attributes, get all unique values
                options = set(option for book in self.library for option in (book[attribute] if isinstance(book[attribute], list) else [book[attribute]]))

                while True:
                    # Display the question and the available options to the user
                    print(question)
                    for option in options:
                        print(option)
                    
                    # Get user's answer
                    answer = input()

                    # Check if the answer is valid
                    if answer not in options:
                        print("Invalid option. Please try again.")
                        continue

                    # Update scores
                    for book in self.library:
                        if book[attribute] == answer:
                            scores[book['title']] += 1
                    
                    # Break the loop if the answer is valid
                    break

        # Sort books based on scores and return top-rated books
        sorted_books = sorted(self.library, key=lambda book: scores[book['title']], reverse=True)
        print(sorted_books[:10])

        # Create a table
        table = Table(title="Top 10 Book Recommendations")

        # Add columns
        table.add_column("Rank", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Score", style="green")

        # Add rows
        for i, book in enumerate(sorted_books, start=1):
            table.add_row(str(i), book['title'], str(scores[book['title']]))

        # Print the table
        print(table)

    def recom_by_top_rated(self, n):
        top_books = []
        heap_copy = self.heap.copy()  # create a copy of the heap
        for _ in range(n):
            if not heap_copy:  # use the copy for popping items
                break
            avg_rating, title, book = heapq.heappop(heap_copy)
            top_books.append((title, -avg_rating))
        return top_books
    
    def recom_by_rating(self, min_rating):
        # Get all books
        all_books = [book for book in self.library]
        
        # Filter books based on the minimum rating
        filtered_books = [book for book in all_books if book["average_rating"] >= min_rating]
        
        # Sort the filtered books by rating in descending order
        sorted_books = sorted(filtered_books, key=lambda book: book["average_rating"], reverse=True)
    
        return sorted_books

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

        

