
import pandas as pd
import math

#------------ Reading CSV files into dataframes-------------------------------

path_books = "C:/Users/moham/OneDrive/Documents/books_task/BX-Books.csv"
path_ratings = "C:/Users/moham/OneDrive/Documents/books_task/BX-Book-Ratings.csv"
path_users = "C:/Users/moham/OneDrive/Documents/books_task/BX-Users.csv"
data_books = pd.read_csv(path_books, encoding='latin-1', error_bad_lines=False, low_memory=False, sep=";")
data_ratings = pd.read_csv(path_ratings, encoding='latin-1', error_bad_lines=False, sep=";", engine='python')
data_users = pd.read_csv(path_users, encoding='latin-1', error_bad_lines=False, sep=";", engine='python')

def get_info(id):
    #----- Returns the location and age of a user given the id------
    info = []
    df = pd.DataFrame(data_users)
    info.append(df.loc[id-1].Location.split(", ")[2])
    info.append(df.loc[id-1].Age)
    return info

def recommend_by_same_group(id):
    #------- Returns a recommended book based on what other users of same age and country read-----
    user_info = get_info(int(id))
    user_country = user_info[0]
    user_age = user_info[1]
    if math.isnan(user_age): user_age = 35 # if i don't have the info of the age of the user, i will assume it is 35(Avg age of the pop. of the world)
    df_users = pd.DataFrame(data_users)
    #------- matching the user with another user having same nationality and somehow similar age --------------
    for  row in df_users.values:
        try:
            if list(row)[1].split(", ")[2] == user_country:
                if math.isnan(list(row)[2]):continue
                if list(row)[2]-5 < user_age < list(row)[2]+5 :
                    rec_user_id = list(row)[0]
                    books = books_read(rec_user_id) # returning the books read by the matched user
                    return books[0][0] # returning a the highest rated book among the books read by the matched user

        except IndexError :
            continue


#------------returning a list of books read by a certain user given his ID ----------

def books_read(id):
    book_read= {}
    #------returning the list of books read into a dictionary----------
    df = data_ratings.loc[data_ratings['User-ID'].isin([id])]
    col_name = df.columns[2]
    df = df.rename(columns={col_name: 'RATINGS'})
    isbns = list(df.ISBN)
    ratings = list(df.RATINGS)
    #--------sorting the dict. so that the maxim rating come first--------
    for i in range(len(isbns)):
        if ratings[i] != 0:
            book_read[isbns[i]] = ratings[i]
        else:
            book_read[isbns[i]] = 5 # implicit rating is given as the average rating(5)
    book_read = sorted(book_read.items(), key=lambda kv: kv[1], reverse=True)
    return book_read

def recommend_by_same_author(id):
    #-------getting the books read by the user---------
    book_read = books_read(id)
    #-------getting the highest rated book in the sorted dict-------------
    isbn = book_read[0][0]
    df_books = pd.DataFrame(data_books)
    col_name = df_books.columns[2]
    df_books = df_books.rename(columns={col_name: 'AUTHOR'})
    #---- returning a dataframe with rows only containing books with same author-----
    df= df_books.loc[df_books['ISBN'].isin([isbn])]
    author = df.AUTHOR.values[0]
    df = df_books.loc[df_books['AUTHOR'].isin([author])]
    recommended_books = list(df.ISBN)
    recommended_books.remove(isbn)
    return recommended_books






print("RECOMMENDED BOOKS : ")
print(recommend_by_same_group('14'))
print(recommend_by_same_author('14'))




