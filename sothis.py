from controllers.goodreads import GoodReads
from controllers.overdrive import OverDrive
from controllers.book import Book

user_id = 35083605 # Goodreads user id

def main():
    # Note currently requests have verify=false, this is for debugging and should be changed.
    gr = GoodReads()
    shelf = gr.get_shelf(user_id, 'on-hold')
    books = gr.get_books(shelf)

    od = OverDrive()
    # First, get our circulation authorization token
    auth_token, token_type = od.authorize()
    # Add integration test library to our library dictionary.
    od.add_library_catalog(auth_token, token_type, 4425)

    for book in books: # For book from goodreads "on-hold" shelf
        print()
        # Circulation API
        results = od.search_for_title(auth_token, token_type, 4425, book) # Search for book in library 4225
        if results: # If search results returned something (NOT NECCESSARILY THE CORRECT BOOK)
            metadata = od.get_metadata(auth_token, token_type, book, results)
            # These two calls (availibility, item_id) can be combined but are split for now.
            availibility = od.get_availability(auth_token, token_type, 4225, book, results) # Check availibility
            item_id = od.get_item_id(auth_token, token_type, book, results) # Get item_id

            # Granted authentication is needed for Holds/Checkout API
            patron_auth_token, patron_token_type = od.authorize_granted(4225)
            if item_id and not availibility['available']:
                hold = od.place_hold(auth_token, token_type, item_id, 'iancaragol@gmail.com')
            elif item_id and availibility['available']:
                checkout = od.checkout(auth_token, token_type, item_id)
    print()

if __name__ == "__main__":
    main()


