import streamlit as st
from hydralit import HydraHeadApp

import sqlite3 as sql
import pandas as pd

def get_all_books():
    database = "library.db"
    books_csv_file = "books.csv"

    # Create a connection to the database
    conn = sql.connect("library.db",check_same_thread=False)
     
    if conn is not None:
        cursor = conn.cursor()

        cursor.execute('SELECT "Image-URL-M",title,average_rating FROM booksdata INNER JOIN bookswithimage ON bookswithimage.ISBN = booksdata.isbn WHERE ratings_count > 1000 ORDER BY average_rating DESC LIMIT 10')
        book_data = cursor.fetchall()
        conn.close()
        return book_data

        # Insert data from CSV file
        #insert_books(conn,books_csv_file)
        #not working for some reason
        # Close the connection
        
    else:
        print("Error! Cannot create the database connection.")
        return None
                 
class HomeApp(HydraHeadApp):


    def __init__(self, title = 'Hydralit Explorer', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title


    #This one method that must be implemented in order to be used in a Hydralit application.
    #The application must also inherit from the hydrapp class in order to correctly work within Hydralit.
    def run(self):

        try:

            st.write("""
                        # Top 10 Books By Rating
                     """)
                     
            bookdata = get_all_books()

            book_clean_df = pd.DataFrame(bookdata, columns=["Cover", "Title", "Rating"])

            columns = st.columns((1, 3, 8, 2))
            
            fields =["Rank","Cover", "Title", "Rating"]
            for col, field_name in zip(columns, fields):
                col.write(field_name)
            for i in book_clean_df.index :
                col1, col2, col3,col4 = st.columns((1, 3, 8, 2))
                col1.write(str(i+1))
                col2.image(book_clean_df["Cover"][i],width = 200)
                col3.write(book_clean_df["Title"][i])
                col4.write(str(book_clean_df["Rating"][i]))
        
        except Exception as e:
            st.error('An error has occurred, someone will be punished for your inconvenience, we humbly request you try again.')
            st.error('Error details: {}'.format(e))