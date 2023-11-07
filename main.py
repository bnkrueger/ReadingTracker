import multiprocessing
import os
import time
from multiprocessing import Lock

def login():
    user_id = input("Do you have a user_id? Yes or No\n").lower()

    # find user in user_id.txt
    if user_id == 'yes':
        user_id = input("Please enter your user_id: ")
        if not user_exists(user_id):
            print("User not found. Please create a user_id.")
            return login()

    # create new user in user_id.txt
    elif user_id == 'no':
        user_id = create_user()
    else:
        print("Invalid input. Please enter 'Yes' or 'No'.")
        return login()

    return user_id


def user_exists(user_id):

    # in user_id find the user's name
    with open('user_id.txt', 'r') as file:
        users = file.readlines()
        for user in users:
            if user_id in user:
                return True
    return False


def create_user():
    # create new user and get name then write in user_id.txt
    user_id = input("Please create a user_id: ")
    name = input("What is your name: ")

    with open('user_id.txt', 'a') as file:
        file.write(f"{user_id} {name}\n")

    return user_id

def track_reading_progress(user_id, book_name, progress_percent):
    tracker = ProgressTracker(user_id)
    tracker.add_book(book_name, progress_percent)

class ProgressTracker:
    def __init__(self, user_id, lock):
        self.user_id = user_id
        self.lock = lock

    def add_book(self, book_name, progress_percent):

        # add book name and percentage
        with self.lock:
            while True:
                try:
                    progress_percent = float(progress_percent)
                except ValueError:
                    print("Invalid input for progress. Please enter a number between 0 and 100.")
                    progress_percent = input("Progress as a percentage: ")
                    continue

                # Check if the progress is within the valid range
                if 0 <= progress_percent <= 100:
                    with open(f'book_progress_{self.user_id}.txt', 'a') as file:
                        file.write(f"{book_name}: {progress_percent}%\n")

                    print("Your book has been saved!")
                    break
                else:
                    print("Invalid progress value. Please enter a percentage between 0 and 100.")
                    progress_percent = input("Progress as a percentage: ")

    def update_progress(self):

        # update existing progress by reading the users file and rewriting the progress percentage
        book_to_update = input("Enter the name of the book you want to update: ")
        new_progress = input("Enter the new progress in percent: ")

        file_path = f'book_progress_{self.user_id}.txt'
        with open(file_path, 'r') as file:
            books = file.readlines()

        with open(file_path, 'w') as file:
            for book in books:
                if book_to_update.lower() in book.lower():
                    file.write(f"{book_to_update}: {new_progress}%\n")
                    print(f"{book_to_update}'s progress has been updated to {new_progress}%.")
                else:
                    file.write(book)

    def track_reading_progress(self):
        option = input(
            "Would you like to Add, Update, or Remove a book from the reading progress? Add/Update/Remove:\n").lower()

        if option == 'add':
            book_name = input("Please enter the book you are reading's name: ")
            progress_percent = input("Progress in percent: ")
            self.add_book(book_name, progress_percent)
        elif option == 'update':
            self.update_progress()
        elif option == 'remove':
            self.remove_book()
        else:
            print("Invalid option. Please enter 'Add', 'Update', or 'Remove'.")

    def remove_book(self):

        # delete book and progress from users file that matches input name
        book_to_remove = input("Enter the name of the book you want to remove: ")

        file_path = f'book_progress_{self.user_id}.txt'
        with open(file_path, 'r') as file:
            books = file.readlines()

        with open(file_path, 'w') as file:
            for book in books:
                if book_to_remove.lower() not in book.lower():
                    file.write(book)

        print(f"{book_to_remove} has been removed.")

def see_reading_history(user_id):
    viewer = HistoryViewer(user_id)
    viewer.view_history()

class HistoryViewer:
    def __init__(self, user_id, lock):
        self.user_id = user_id
        self.lock = lock

    # print file of user's books and percentages
    def view_history(self):
        with self.lock:
            file_path = f'book_progress_{self.user_id}.txt'
            with open(file_path, 'r') as file:
                books = file.readlines()
                if not books:
                    print("No reading history found.")
                else:
                    print("Here is your reading history:")
                    for book in books:
                        book_info = book.split(':')
                        book_name = book_info[0].strip()
                        progress_percent = book_info[1].strip() if len(book_info) > 1 else "Unknown"
                        print(f"{book_name}: {progress_percent}")


def see_recommendations():
    RecommendationViewer.see_recommendations()

class RecommendationViewer:
    def __init__(self, lock):
        self.lock = lock

    @staticmethod
    def see_recommendations():
        lock = Lock()
        with lock:
            genre = input(
                "What genre would you like recommendations for? Science Fiction, Fiction, Horror, or Romance:\n").lower()

            if genre == 'science fiction':
                recommendations = [
                    "1: Frankenstein by Mary Shelley",
                    "2: Ace Dune by Frank Herbert",
                    "3: The Martian Chronicles by Ray Bradbury"
                ]
            elif genre == 'fiction':
                recommendations = [
                    "1: The Lord of the Rings by J.R.R. Tolkien",
                    "2: To Kill a Mockingbird by Harper Lee",
                    "3: Lord of the Flies by William Golding"
                ]
            elif genre == 'horror':
                recommendations = [
                    "1: IT by Stephen King",
                    "2: House of Leaves by Mark Danielewski",
                    "3: The Haunting of Hill House by Shirley Jackson"
                ]
            elif genre == 'romance':
                recommendations = [
                    "1: Pride and Prejudice by Jane Austen",
                    "2: Outlander by Diana Gabaldon",
                    "3: Jane Eyre by Charlotte Bronte"
                ]
            else:
                print("Invalid genre. Please enter Science Fiction, Fiction, Horror, or Romance.")
                return

            print(f"Here are your recommendations for {genre}:")
            for recommendation in recommendations:
                print(recommendation)


def main():
    user_id = login()
    with open('user_id.txt', 'r') as file:
        users = file.readlines()
        for user in users:
            if user_id in user:
                name = user.split()[1]
                print(f"Welcome {name}!")

    while True:
        action = input(
            "\nWhat would you like to do? \n1: Track reading progress\n2: See reading history\n3: See recommendations\n(Enter 1, 2, or 3)\nType 'exit' to close:\n").lower()

        if action == 'exit':
            print("Happy Reading!")
            break
        elif action == '1':
            # Create a lock to synchronize output
            lock = Lock()

            # Pass the lock to the ProgressTracker
            tracker = ProgressTracker(user_id, lock)
            tracker.track_reading_progress()
        elif action == '2':
            # Create a lock to synchronize output
            lock = Lock()
            viewer = HistoryViewer(user_id, lock)
            viewer.view_history()
        elif action == '3':
            # Create a lock to synchronize output
            lock = Lock()
            viewer = RecommendationViewer(lock)
            viewer.see_recommendations()
        else:
            print("Invalid option. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
