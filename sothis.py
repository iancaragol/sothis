from controllers.goodreads import GoodReads
from controllers.overdrive import OverDrive

user_id = 35083605

def main():
    gr = GoodReads()
    shelf = gr.get_shelf(user_id, 'on-hold')
    isbns = gr.parse_isbns(shelf)
    titles = gr.parse_titles(shelf)

    od = OverDrive()
    auth_token, token_type = od.authorize(4225)
    od.add_library_catalog(auth_token, token_type, 4225)

    print(isbns)
    print(titles)

if __name__ == "__main__":
    main()


