import json
import os
from collections import Counter

# Save Books and Quotes to JSON files:
def save_data(books, quotes, books_file="books.json", quotes_file="quotes.json"):
    try:
        with open(books_file, 'w') as f:
            json.dump(books, f)
        with open(quotes_file, 'w') as f:
            json.dump(quotes, f)
        print("Data saved successfully!")
    except Exception as e:
        print(f"Error saving data: {e}")

# Load Books and Quotes from JSON files:
def load_data(books_file="books.json", quotes_file="quotes.json"):
    books, quotes = [], []
    try:
        if os.path.exists(books_file):
            with open(books_file, 'r') as f:
                books = json.load(f)
        if os.path.exists(quotes_file):
            with open(quotes_file, 'r') as f:
                quotes = json.load(f)
        print("Data loaded successfully!")
    except Exception as e:
        print(f"Error loading data: {e}")
    return books, quotes

# Add a new Book entry with validation for unique Title + Author:
def add_book(books):
    title = input("Enter Book Title: ").strip().lower()
    author = input("Enter Author: ").strip().lower()
    
    # Check for duplicate Title + Author:
    for book in books:
        if book['title'].lower() == title and book['author'].lower() == author:
            print("Error: Book with this Title and Author already exists.")
            return
    
    try:
        year = input("Enter year published: ").strip()
        year = int(year)
        if year < 0 or year > 2025:  # Assuming current year is 2025
            print("Invalid year. Must be between 0 and 2025.")
            return
    except ValueError:
        print("Invalid year. Must be an integer.")
        return
    
    genres = input("Enter genres (comma-separated): ").strip().lower().split(',')
    genres = set(genre.strip() for genre in genres if genre.strip())  # Remove empty genres
    
    status = input("Enter status (reading/completed/on hold): ").strip().lower()
    if status not in ["reading", "completed", "on hold"]:
        print("Invalid status. Must be 'reading', 'completed', or 'on hold'.")
        return
    
    books.append({
        "title": title,
        "author": author,
        "year": year,
        "genres": list(genres),  # Convert set to list for JSON Serialization
        "status": status
    })
    print("Book added successfully!")

# View all Books sorted by year published:
def view_books(books):
    if not books:
        print("No books found.")
        return
    
    sorted_books = sorted(books, key=lambda x: x['year'])
    print("\nBook List (Sorted by Year):")
    for book in sorted_books:
        print(f"Title: {book['title'].title()}, Author: {book['author'].title()}, "
              f"Year: {book['year']}, Genres: {', '.join(book['genres'])}, Status: {book['status'].title()}")

# Search Books by Genre or Status:
def search_books(books):
    search_type = input("Search by (Genre/Status): ").strip().lower()
    if search_type not in ["genre", "status"]:
        print("Invalid search type. Must be 'genre' or 'status'.")
        return
    
    query = input(f"Enter {search_type}: ").strip().lower()
    found = False
    
    for book in books:
        if search_type == "genre" and query in book['genres']:
            found = True
            print(f"Title: {book['title'].title()}, Author: {book['author'].title()}, "
                  f"Year: {book['year']}, Genres: {', '.join(book['genres'])}, Status: {book['status'].title()}")
        elif search_type == "status" and book['status'].lower() == query:
            found = True
            print(f"Title: {book['title'].title()}, Author: {book['author'].title()}, "
                  f"Year: {book['year']}, Genres: {', '.join(book['genres'])}, Status: {book['status'].title()}")
    
    if not found:
        print(f"No Books found with {search_type} '{query}'.")

# Update a Book's Status or add Genres:
def update_book(books):
    title = input("Enter Book Title to update: ").strip().lower()
    author = input("Enter Author: ").strip().lower()
    
    for book in books:
        if book['title'].lower() == title and book['author'].lower() == author:
            print(f"Found: {book['title'].title()} by {book['author'].title()}")
            action = input("Update (status/genres): ").strip().lower()
            
            if action == "status":
                new_status = input("Enter new Status (reading/completed/on hold): ").strip().lower()
                if new_status not in ["reading", "completed", "on hold"]:
                    print("Invalid Status.")
                    return
                book['status'] = new_status
                print("Status updated!")
            elif action == "genres":
                new_genres = input("Enter Genres to add (comma-separated): ").strip().lower().split(',')
                new_genres = set(genre.strip() for genre in new_genres if genre.strip())
                book['genres'] = list(set(book['genres']) | new_genres)  # Union of genres
                print("Genres updated!")
            else:
                print("Invalid action.")
            return
    
    print("Book not found.")

# Delete a Book entry:
def delete_book(books):
    title = input("Enter Book Title to delete: ").strip().lower()
    author = input("Enter Author: ").strip().lower()
    
    for i, book in enumerate(books):
        if book['title'].lower() == title and book['author'].lower() == author:
            books.pop(i)
            print("Book deleted successfully!")
            return
    
    print("Book not found.")

# Add a new Quote:
def add_quote(quotes, books):
    book_title = input("Enter Book Title for quote: ").strip().lower()
    author = input("Enter Author: ").strip().lower()
    
    # Verify Book exists:
    book_exists = False
    for book in books:
        if book['title'].lower() == book_title and book['author'].lower() == author:
            book_exists = True
            break
    if not book_exists:
        print("Book not found. Please add the book first.")
        return
    
    text = input("Enter Quote: ").strip()
    if not text:
        print("Quote cannot be empty.")
        return
    
    try:
        page = input("Enter page number: ").strip()
        page = int(page)
        if page < 1:
            print("Page number must be positive.")
            return
    except ValueError:
        print("Invalid page number. Must be an integer.")
        return
    
    quotes.append({
        "text": text,
        "book_title": book_title,
        "author": author,
        "page_number": page
    })
    print("Quote added successfully!")

# View all Quotes sorted by Book or Author:
def view_quotes(quotes):
    if not quotes:
        print("No Quotes found.")
        return
    
    sort_by = input("Sort by (Book/Author): ").strip().lower()
    if sort_by not in ["book", "author"]:
        print("Invalid sort option. Using default (Book).")
        sort_by = "book"
    
    sorted_quotes = sorted(quotes, key=lambda x: x['book_title' if sort_by == 'book' else 'author'])
    print("\nQuote List:")
    for quote in sorted_quotes:
        print(f"Quote: {quote['text']}")
        print(f"From: {quote['book_title'].title()} by {quote['author'].title()}, Page: {quote['page_number']}\n")

# Search Quotes by keyword:
def search_quotes(quotes):
    keyword = input("Enter keyword to search: ").strip().lower()
    found = False
    
    for quote in quotes:
        if keyword in quote['text'].lower():
            found = True
            print(f"Quote: {quote['text']}")
            print(f"From: {quote['book_title'].title()} by {quote['author'].title()}, Page: {quote['page_number']}\n")
    
    if not found:
        print(f"No Quotes found with keyword '{keyword}'.")

# Delete a Quote:
def delete_quote(quotes):
    text = input("Enter Quote text to delete (or part of it): ").strip().lower()
    
    for i, quote in enumerate(quotes):
        if text in quote['text'].lower():
            print(f"Found: {quote['text']} (From: {quote['book_title'].title()})")
            confirm = input("Delete this quote? (y/n): ").strip().lower()
            if confirm == 'y':
                quotes.pop(i)
                print("Quote deleted successfully!")
                return
    
    print("Quote not found.")

# List all Books completed in a user-given year:
def books_completed_in_year(books):
    try:
        year = int(input("Enter year: ").strip())
        found = False
        for book in books:
            if book['status'].lower() == "completed" and book['year'] == year:
                found = True
                print(f"Title: {book['title'].title()}, Author: {book['author'].title()}, "
                      f"Genres: {', '.join(book['genres'])}")
        if not found:
            print(f"No Books completed in {year}.")
    except ValueError:
        print("Invalid year. Must be an integer.")

# Find the Book with the most collected Quotes:
def book_with_most_quotes(quotes, books):
    if not quotes:
        print("No Quotes found.")
        return
    
    book_counts = Counter(quote['book_title'].lower() for quote in quotes)
    if not book_counts:
        print("No Quotes found.")
        return
    
    most_common_book = book_counts.most_common(1)[0]
    book_title, count = most_common_book
    
    # Find Author for display:
    author = "Unknown"
    for book in books:
        if book['title'].lower() == book_title:
            author = book['author'].title()
            break
    
    print(f"Book with most Quotes: {book_title.title()} by {author} ({count} Quotes)")

# Find the Author(s) with the most Book entries:
def authors_with_most_entries(books):
    if not books:
        print("No Books found.")
        return
    
    author_counts = Counter(book['author'].lower() for book in books)
    max_count = max(author_counts.values())
    top_authors = [author.title() for author, count in author_counts.items() if count == max_count]
    
    print(f"Author(s) with most entries ({max_count} Books): {', '.join(top_authors)}")

def main():
    books, quotes = load_data()
    
    while True:
        print("\nPersonal Reading Journal Menu:")
        print("1. Add a new Book")
        print("2. View all Books")
        print("3. Search Books by Genre or Status")
        print("4. Update a Book")
        print("5. Delete a Book")
        print("6. Add a new Quote")
        print("7. View all Quotes")
        print("8. Search Quotes by keyword")
        print("9. Delete a Quote")
        print("10. List Books completed in a year")
        print("11. Book with most Quotes")
        print("12. Authors with most entries")
        print("13. Save and exit")
        
        choice = input("Enter your choice (1-13): ").strip()
        
        if choice == "1":
            add_book(books)
        elif choice == "2":
            view_books(books)
        elif choice == "3":
            search_books(books)
        elif choice == "4":
            update_book(books)
        elif choice == "5":
            delete_book(books)
        elif choice == "6":
            add_quote(quotes, books)
        elif choice == "7":
            view_quotes(quotes)
        elif choice == "8":
            search_quotes(quotes)
        elif choice == "9":
            delete_quote(quotes)
        elif choice == "10":
            books_completed_in_year(books)
        elif choice == "11":
            book_with_most_quotes(quotes, books)
        elif choice == "12":
            authors_with_most_entries(books)
        elif choice == "13":
            save_data(books, quotes)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 13.")

if __name__ == "__main__":
    main()