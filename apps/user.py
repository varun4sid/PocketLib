import streamlit as st
from hydralit import HydraHeadApp

import sqlite3 as sql

import pandas as pd

def get_browse():
    database = "library.db"

    # Create a connection to the database
    conn = sql.connect("library.db",check_same_thread=False)
     
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(f"SELECT i.Image_L,b.title,b.average_rating,b.num_pages,b.isbn13 FROM books b inner join imagedata i on b.isbn13 = i.isbn13 ORDER BY b.average_rating DESC LIMIT 100;")
        book_data = cursor.fetchall()
        conn.close()
        return book_data
        # Close the connection
        
    else:
        print("Error! Cannot create the database connection.")
        return None

def get_book_details(isbn13):
    database = "library.db"

    # Create a connection to the database
    conn = sql.connect("library.db",check_same_thread=False)
     
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(f"SELECT b.*,Image_L,a.author_name,p.publisher_name FROM books b INNER JOIN imagedata i on i.isbn13 = b.isbn13  INNER JOIN Authoredby ab on b.isbn13 = ab.isbn13 INNER JOIN author a on a.author_id = ab.author_id INNER JOIN publishedby pb on pb.isbn13 = b.isbn13 INNER JOIN publisher p on p.publisher_id = pb.publisher_id where b.isbn13 = {isbn13};")
        book_data = cursor.fetchall()
        conn.close()
        return book_data
        # Close the connection
        
    else:
        print("Error! Cannot create the database connection.")
        return None
        
def get_status(username):
    database = "library.db"

    # Create a connection to the database
    conn = sql.connect("library.db",check_same_thread=False)
     
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(f"SELECT s.* FROM status s INNER join books b on s.isbn13 = b.isbn13 INNER JOIN imagedata i on i.isbn13 = s.isbn13 where user_id = (select user_id from user where username = '{username}');")
        book_data = cursor.fetchall()
        conn.close()
        return book_data
        # Close the connection
        
    else:
        print("Error! Cannot create the database connection.")
        return None

def get_status_all(username):
    database = "library.db"

    # Create a connection to the database
    conn = sql.connect("library.db",check_same_thread=False)
     
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(f"SELECT i.Image_L,b.title,s.status,b.isbn13 FROM status s LEFT OUTER join books b on s.isbn13 = b.isbn13 LEFT OUTER JOIN imagedata i on i.isbn13 = s.isbn13 where user_id = (select user_id from user where username = '{username}');")
        book_data = cursor.fetchall()
        conn.close()
        return book_data
        # Close the connection
        
    else:
        print("Error! Cannot create the database connection.")
        return None
        
def get_status_completed(username):
    database = "library.db"

    # Create a connection to the database
    conn = sql.connect("library.db",check_same_thread=False)
     
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(f"SELECT i.Image_L,b.title,s.rating,s.notes,b.isbn13 FROM status s LEFT OUTER join books b on s.isbn13 = b.isbn13 LEFT OUTER JOIN imagedata i on i.isbn13 = s.isbn13 where user_id = (select user_id from user where username = '{username}') and s.status = 'C';")
        book_data = cursor.fetchall()
        conn.close()
        return book_data
        # Close the connection
        
    else:
        print("Error! Cannot create the database connection.")
        return None

def get_status_reading(username):
    database = "library.db"

    # Create a connection to the database
    conn = sql.connect("library.db",check_same_thread=False)
     
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(f"SELECT i.Image_L,b.title,s.current_page || ' / ' || b.num_pages,b.isbn13 FROM status s LEFT OUTER join books b on s.isbn13 = b.isbn13 LEFT OUTER JOIN imagedata i on i.isbn13 = s.isbn13 where user_id = (select user_id from user where username = '{username}' and s.status = 'R');")
        book_data = cursor.fetchall()
        conn.close()
        return book_data
        # Close the connection
        
    else:
        print("Error! Cannot create the database connection.")
        return None
        
def get_status_planning(username):
    database = "library.db"

    # Create a connection to the database
    conn = sql.connect("library.db",check_same_thread=False)
     
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(f"SELECT i.Image_L,b.title,s.notes,b.isbn13 FROM status s LEFT OUTER join books b on s.isbn13 = b.isbn13 LEFT OUTER JOIN imagedata i on i.isbn13 = s.isbn13 where user_id = (select user_id from user where username = '{username}' and s.status = 'P');")
        book_data = cursor.fetchall()
        conn.close()
        return book_data
        # Close the connection
        
    else:
        print("Error! Cannot create the database connection.")
        return None
def insert_book(insertform,isbn13,status):
    database = "library.db"
    # Create a connection to the database
    conn = sql.connect("library.db",check_same_thread=False)
    newstatus = 'R'
    if(status == 'Reading'):
        newstatus = 'R'
    elif(status == 'Completed'):
        newstatus = 'C'
    elif(status == 'Planning'):
        newstatus = 'P'
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO status(user_id,isbn13,status,current_page,rating,notes) VALUES((SELECT user_id from user where username = '{st.session_state.current_user}'),{isbn13},'{newstatus}',NULL,NULL,NULL);")
        conn.commit()
        conn.close()
    # Close the connection
        
    else:
        print("Error! Cannot create the database connection.")
        return None

def update_status(newform,isbn13):
    database = "library.db"
    # Create a connection to the database
    conn = sql.connect("library.db",check_same_thread=False)
    if newform['delete']:
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM status WHERE isbn13 = {isbn13} and user_id = (SELECT user_id from user where username = '{st.session_state.current_user}');")
            conn.commit()
            conn.close()
            # Close the connection
            
        else:
            print("Error! Cannot create the database connection.")
            return None

    else:
        newstatus = 'R'
        if(newform['status'] == 'Reading'):
            newstatus = 'R'
        elif(newform['status'] == 'Completed'):
            newstatus = 'C'
        elif(newform['status'] == 'Planning'):
            newstatus = 'P'
            
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE status SET status = '{newstatus}' , current_page = {newform['current_page']} ,rating = {newform['rating']},notes = '{newform['notes']}' WHERE isbn13 = {isbn13} and user_id = (SELECT user_id from user where username = '{st.session_state.current_user}');")
            conn.commit()
            conn.close()
            # Close the connection
            
        else:
            print("Error! Cannot create the database connection.")
            return None

def editbookstatus(isbn13,placeholder,render = 1):
    if render:
        book_details = get_book_details(isbn13)
        with placeholder.container():
            column1,column2 = st.columns((1,5))
            if not book_details[0][6] == None :
                column1.image(book_details[0][6],width = 200)
            column2.header("Name : " + book_details[0][2] )
            column2.subheader("Authored by : " + book_details[0][7])
            column2.subheader("Published by : " + book_details[0][8])
            column2.subheader("Rating : " + str(book_details[0][1]))
            with st.form(key = 'Edit',clear_on_submit = True):
                formstate = {}
                formstate['status'] = st.selectbox('Status',('Reading','Completed','Planning'))
                formstate['current_page'] = st.slider('Number Of Pages Read',0,book_details[0][3],1) 
                formstate['rating'] = st.slider("Rating",0,10,1)
                formstate['notes'] = st.text_input("Notes")
                formstate['delete'] = st.checkbox("🗑 Delete",key = 'Delete')
                formstate['Submitted'] = st.form_submit_button('Update')
                if formstate['Submitted']:
                    update_status(formstate,isbn13)

class UserApp(HydraHeadApp):

    def __init__(self, title = '', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self) -> None:
        """
        Application entry point.
        """
        unique_key = 0
        
        if 'clicked' not in st.session_state :
            st.session_state.clicked = False
        if 'formbutton' not in st.session_state :
            st.session_state.formbutton = False

        menu = ["All", "Reading","Completed","Planning","Insert"]
        choice = st.sidebar.selectbox("Menu", menu)
        placeholder = st.empty()
        enabled = None
        if choice == 'All' :
            with placeholder.container():
                st.title(f"Welcome to your Personal Library 📚 {self.session_state.current_user}")
                bookdata = get_status_all(self.session_state.current_user)
                book_clean_df = pd.DataFrame(bookdata, columns=["Cover", "Title", "Status","isbn13"])
                columns = st.columns((1, 3, 6, 2,1))
                fields =["Rank","Cover", "Title", "Status"]
                for col, field_name in zip(columns, fields):
                    col.write(field_name)
                for i in book_clean_df.index :
                    col1, col2, col3,col4,col5 = st.columns((1, 3, 6, 2,1))
                    col1.write(str(i+1))
                    if not book_clean_df["Cover"][i] == None:
                        col2.image(book_clean_df["Cover"][i],width = 200)
                    col3.write(book_clean_df["Title"][i])
                    col4.write(str(book_clean_df["Status"][i]))
                    if (enabled == None) or (enabled == i):
                        render = col5.checkbox("Edit",key = str(unique_key),disabled = False)
                    else :
                        render = col5.checkbox("Edit",key = str(unique_key),disabled = True)
                    if render :
                        enabled = i
                        editbookstatus(book_clean_df["isbn13"][i],placeholder)
                    unique_key +=1
            
        elif choice == 'Reading' :
            with placeholder.container():
                st.title(f"Reading 📚")
                bookdata = get_status_reading(self.session_state.current_user)
                book_clean_df = pd.DataFrame(bookdata, columns=["Cover", "Title","Current Page","isbn13"])
                columns = st.columns((1, 3, 6, 2,1))
                fields =["Rank","Cover", "Title", "Current/Toal"]
                for col, field_name in zip(columns, fields):
                    col.write(field_name)
                for i in book_clean_df.index :
                    col1, col2, col3,col4,col5 = st.columns((1, 3, 6, 2,1))
                    col1.write(str(i+1))
                    if not book_clean_df["Cover"][i] == None:
                        col2.image(book_clean_df["Cover"][i],width = 200)
                    col3.write(book_clean_df["Title"][i])
                    col4.write(str(book_clean_df["Current Page"][i]))
                    if (enabled == None) or (enabled == i):
                        render = col5.checkbox("Edit",key = str(unique_key),disabled = False)
                    else :
                        render = col5.checkbox("Edit",key = str(unique_key),disabled = True)
                    if render :
                        enabled = i
                        editbookstatus(book_clean_df["isbn13"][i],placeholder)
                    unique_key +=1
        elif choice == 'Completed' :
            with placeholder.container():
                st.title(f"Completed ✔")
                bookdata = get_status_completed(self.session_state.current_user)
                book_clean_df = pd.DataFrame(bookdata, columns=["Cover", "Title", "Rating" ,"Note","isbn13"])
                columns = st.columns((1, 3, 3, 2, 4, 1))
                fields =["Rank","Cover", "Title", "Rating","Note"]
                for col, field_name in zip(columns, fields):
                    col.write(field_name)
                for i in book_clean_df.index :
                    col1, col2, col3,col4,col5,col6 = st.columns((1, 3, 3, 2, 4, 1))
                    col1.write(str(i+1))
                    if not book_clean_df["Cover"][i] == None:
                        col2.image(book_clean_df["Cover"][i],width = 200)
                    col3.write(book_clean_df["Title"][i])
                    col4.write(str(book_clean_df["Rating"][i]))
                    col5.write(book_clean_df["Note"][i])
                    if (enabled == None) or (enabled == i):
                        render = col6.checkbox("Edit",key = str(unique_key),disabled = False)
                    else :
                        render = col6.checkbox("Edit",key = str(unique_key),disabled = True)
                    if render :
                        enabled = i
                        editbookstatus(book_clean_df["isbn13"][i],placeholder)
                    unique_key +=1
        elif choice == 'Planning' :
            with placeholder.container():
                st.title(f"Planning 🕐")
                bookdata = get_status_planning(self.session_state.current_user)
                book_clean_df = pd.DataFrame(bookdata, columns=["Cover", "Title", "Status","isbn13"])
                columns = st.columns((1, 3, 6, 2,1))
                fields =["Rank","Cover", "Title", "Status"]
                for col, field_name in zip(columns, fields):
                    col.write(field_name)
                for i in book_clean_df.index :
                    col1, col2, col3,col4,col5 = st.columns((1, 3, 6, 2,1))
                    col1.write(str(i+1))
                    if not book_clean_df["Cover"][i] == None:
                        col2.image(book_clean_df["Cover"][i],width = 200)
                    col3.write(book_clean_df["Title"][i])
                    col4.write(str(book_clean_df["Status"][i]))
                    if (enabled == None) or (enabled == i):
                        render = col5.checkbox("Edit",key = str(unique_key),disabled = False)
                    else :
                        render = col5.checkbox("Edit",key = str(unique_key),disabled = True)
                    if render :
                        enabled = i
                        editbookstatus(book_clean_df["isbn13"][i],placeholder)
                    unique_key +=1
        elif choice == 'Insert' :
            st.title(f"Browse 🔎")
            book_clean_df = pd.DataFrame(get_browse(),columns = ["Cover","Title","Rating","NumPages","isbn13"])
            
            # with placeholder():
            columns = st.columns((1,2, 6, 1, 1,1))
            fields = ["Rank","Cover","Title","Rating","NumPages","Insert"]
            for col, field_name in zip(columns, fields):
                col.write(field_name)
            for i in book_clean_df.index :
                col1, col2, col3,col4,col5,col6 = st.columns((1,2, 6, 1, 1,1))
                col1.write(str(i+1))
                col2.image(book_clean_df["Cover"][i],width = 150)
                col3.subheader(book_clean_df["Title"][i])
                col4.subheader(str(book_clean_df["Rating"][i]))
                col5.subheader(str(book_clean_df["NumPages"][i]))
                userisbns = [item[1] for item in get_status(self.session_state.current_user)]
                if book_clean_df["isbn13"][i] in userisbns: 
                    insert_f = False 
                    col6.subheader("In Library")
                else :
                    insert_f = col6.checkbox("Insert",key = str(unique_key) )
                unique_key+=1
                if insert_f :
                    placeholder.empty()
                    with st.form(key = 'InserForm',clear_on_submit = True):
                        insertform = {}
                        isbn13 = book_clean_df["isbn13"][i]
                        status = st.selectbox('Status',('Reading','Completed','Planning'))
                        insertform['Submitted'] = st.form_submit_button('Insert')
                        if insertform['Submitted']:
                            insert_book(insertform,isbn13,status)