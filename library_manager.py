import streamlit as st
import json

# File to store library data
LIBRARY_FILE = "library.txt"

# Function to load the library from a file
def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save the library to a file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file)

# Function to add a book
def add_book(library):
    st.subheader("Add a Book")
    title = st.text_input("Enter the book title:")
    author = st.text_input("Enter the author:")
    year = st.number_input("Enter the publication year:", min_value=1800, max_value=2023)
    genre = st.text_input("Enter the genre:")
    read_status = st.radio("Have you read this book?", ("Yes", "No")) == "Yes"

    if st.button("Add Book"):
        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read_status": read_status
        }
        library.append(book)
        save_library(library)
        st.success("Book added successfully!")

# Function to remove a book
def remove_book(library):
    st.subheader("Remove a Book")
    title = st.text_input("Enter the title of the book to remove:")
    if st.button("Remove Book"):
        for book in library:
            if book["title"].lower() == title.lower():
                library.remove(book)
                save_library(library)
                st.success("Book removed successfully!")
                return
        st.error("Book not found!")

# Function to search for a book
def search_book(library):
    st.subheader("Search for a Book")
    search_by = st.radio("Search by:", ("Title", "Author"))
    query = st.text_input(f"Enter the {search_by.lower()}:")

    if st.button("Search"):
        if search_by == "Title":
            matching_books = [book for book in library if query.lower() in book["title"].lower()]
        else:
            matching_books = [book for book in library if query.lower() in book["author"].lower()]

        if matching_books:
            st.write("Matching Books:")
            for i, book in enumerate(matching_books, 1):
                status = "Read" if book["read_status"] else "Unread"
                st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
        else:
            st.warning("No matching books found!")

# Function to display all books
def display_all_books(library):
    st.subheader("Your Library")
    if not library:
        st.warning("Your library is empty!")
        return

    for i, book in enumerate(library, 1):
        status = "Read" if book["read_status"] else "Unread"
        st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

# Function to display statistics
def display_statistics(library):
    st.subheader("Library Statistics")
    total_books = len(library)
    if total_books == 0:
        st.warning("No books in the library!")
        return

    read_books = sum(1 for book in library if book["read_status"])
    percentage_read = (read_books / total_books) * 100

    st.write(f"Total books: {total_books}")
    st.write(f"Percentage read: {percentage_read:.1f}%")

# Main function
def main():
    st.title("📚 Personal Library Manager")
    library = load_library()

    menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add a Book":
        add_book(library)
    elif choice == "Remove a Book":
        remove_book(library)
    elif choice == "Search for a Book":
        search_book(library)
    elif choice == "Display All Books":
        display_all_books(library)
    elif choice == "Display Statistics":
        display_statistics(library)

if __name__ == "__main__":
    main()