from controllers.goodreads import GoodReads

user_id = 35083605

def main():
    gr = GoodReads()
    shelf = gr.get_shelf(user_id, 'on-hold')
    print(shelf)
    isbns = gr.parse_isbns(shelf)
    print(isbns)

if __name__ == "__main__":
    main()
    

