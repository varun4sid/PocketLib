//Create table

CREATE TABLE IF NOT EXISTS books (
    isbn13 REAL PRIMARY KEY,
	average_rating REAL,
	title TEXT,
	num_pages INTEGER,
	language_code VARCHAR,
	ratings_count INTEGER
);

INSERT INTO books (isbn13,average_rating,title,num_pages,language_code,ratings_count)
SELECT b.isbn13,b.average_rating,b.title,b.num_pages,b.language_code,b.ratings_count
FROM booksdata b;

CREATE TABLE IF NOT EXISTS author (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT UNIQUE
);

INSERT OR IGNORE INTO author (author_name)
SELECT DISTINCT authors
FROM booksdata;

CREATE TABLE IF NOT EXISTS publisher (
    publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    publisher_name TEXT UNIQUE
);

INSERT OR IGNORE INTO publisher (publisher_name)
SELECT DISTINCT publishers
FROM booksdata;

CREATE TABLE IF NOT EXISTS Authoredby (
    isbn13 REAL,
    author_id INTEGER,
    FOREIGN KEY (isbn13) REFERENCES books(isbn13),
    FOREIGN KEY (author_id) REFERENCES author(author_id)
);

INSERT INTO Authoredby (isbn13, author_id)
SELECT b.isbn13, a.author_id
FROM booksdata b
JOIN author a ON b.authors = a.author_name;

CREATE TABLE IF NOT EXISTS publishedby (
    isbn13 REAL,
    publisher_id INTEGER,
    FOREIGN KEY (isbn13) REFERENCES books(isbn13),
    FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id)
);

INSERT INTO publishedby (isbn13, publisher_id)
SELECT b.isbn13, a.publisher_id
FROM booksdata b
JOIN publisher a ON b.publisher = a.publisher_name;

CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
);

INSERT INTO user (username, password) VALUES ('joe', 'joe')

CREATE TABLE IF NOT EXISTS status (
    user_id INTEGER,
    isbn13 REAL,
	status TEXT,
    current_page INTEGER,
    rating INTEGER,
    notes TEXT,
    PRIMARY KEY (user_id, isbn13),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (isbn13) REFERENCES books(isbn13)
);

INSERT INTO status(user_id,isbn13,status,current_page,rating,notes) VALUES(1,9780439785969.0,'R',70,9,NULL);

create table imagedata(
	isbn13 REAL,
	Image_L TEXT,
	Image_M TEXT,
	Image_S TEXT,
	FOREIGN KEY(isbn13) REFERENCES books(isbn13)
);

INSERT OR IGNORE INTO imagedata
select bd.isbn13,"Image-URL-L","Image-URL-M","Image-URL-S" from bookswithimage bi inner join booksdata bd on bi.isbn = bd.isbn;

CREATE TABLE IF NOT EXISTS status_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation TEXT,
    timestamp TEXT,
    user_id INTEGER,
    isbn13 REAL,
    current_page INTEGER,
    rating INTEGER,
    notes TEXT
);

DROP TRIGGER status_insert_trigger;
DROP TRIGGER status_update_trigger;
DROP TRIGGER status_delete_trigger;
CREATE TRIGGER IF NOT EXISTS status_insert_trigger
AFTER INSERT ON status
FOR EACH ROW
BEGIN
    INSERT INTO status_log (operation, timestamp, user_id, isbn13, current_page, rating, notes)
    VALUES ('INSERT', datetime('now'), NEW.user_id, NEW.isbn13, NEW.current_page, NEW.rating, NEW.notes);
END;

CREATE TRIGGER IF NOT EXISTS status_update_trigger
AFTER UPDATE ON status
FOR EACH ROW
BEGIN
    INSERT INTO status_log (operation, timestamp, user_id, isbn13, current_page, rating, notes)
    VALUES ('UPDATE', datetime('now'), NEW.user_id, NEW.isbn13, NEW.current_page, NEW.rating, NEW.notes);
END;

CREATE TRIGGER IF NOT EXISTS status_delete_trigger
AFTER DELETE ON status
FOR EACH ROW
BEGIN
    INSERT INTO status_log (operation, timestamp, user_id, isbn13, current_page, rating, notes)
    VALUES ('DELETE', datetime('now'), OLD.user_id, OLD.isbn13, OLD.current_page, OLD.rating, OLD.notes);
END;

CREATE TRIGGER IF NOT EXISTS prevent_same_username_password
BEFORE INSERT ON user
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.username = NEW.password THEN
            RAISE(ABORT, 'Username and password cannot be the same.')
        ELSE
            NULL
    END;
END;

DELIMITER //

CREATE PROCEDURE InsertStatus(
    IN current_user_name VARCHAR(255),
    IN isbn_13 VARCHAR(255),
    IN new_status VARCHAR(255)
)
BEGIN
    DECLARE user_id_val INT;

    -- Get the user_id based on the provided username
    SELECT user_id INTO user_id_val FROM user WHERE username = current_user_name;

    -- Insert the status record
    INSERT INTO status(user_id, isbn13, status, current_page, rating, notes)
    VALUES(user_id_val, isbn_13, new_status, NULL, NULL, NULL);

END //

DELIMITER ;

CALL InsertStatus('{st.session_state.current_user}', '{isbn13}', '{newstatus}');

DELIMITER //

CREATE PROCEDURE UpdateStatus(
    IN current_user_name VARCHAR(255),
    IN isbn_13 VARCHAR(255),
    IN new_status VARCHAR(255),
    IN new_current_page INT,
    IN new_rating INT,
    IN new_notes VARCHAR(255)
)
BEGIN
    DECLARE user_id_val INT;

    -- Get the user_id based on the provided username
    SELECT user_id INTO user_id_val FROM user WHERE username = current_user_name;

    -- Update the status record
    UPDATE status
    SET status = new_status,
        current_page = new_current_page,
        rating = new_rating,
        notes = new_notes
    WHERE isbn13 = isbn_13 AND user_id = user_id_val;

END //

DELIMITER ;

CALL UpdateStatus('{st.session_state.current_user}', '{isbn13}', '{newstatus}', {newform['current_page']}, {newform['rating']}, '{newform['notes']}');

DELIMITER //

CREATE PROCEDURE DeleteStatus(
    IN current_user_name VARCHAR(255),
    IN isbn_13 VARCHAR(255)
)
BEGIN
    DECLARE user_id_val INT;

    -- Get the user_id based on the provided username
    SELECT user_id INTO user_id_val FROM user WHERE username = current_user_name;

    -- Delete the status record
    DELETE FROM status
    WHERE isbn13 = isbn_13 AND user_id = user_id_val;

END //

DELIMITER ;

CALL DeleteStatus('{st.session_state.current_user}', '{isbn13}');

DELIMITER //

CREATE FUNCTION GetTopRatedBooks()
RETURNS INT
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE image_url VARCHAR(255);
    DECLARE book_title VARCHAR(255);
    DECLARE avg_rating FLOAT;
    DECLARE num_pages INT;
    DECLARE isbn_13 VARCHAR(255);
    
    -- Create a temporary table to store the result
    CREATE TEMPORARY TABLE IF NOT EXISTS temp_top_rated_books (
        Image_L VARCHAR(255),
        title VARCHAR(255),
        average_rating FLOAT,
        num_pages INT,
        isbn13 VARCHAR(255)
    );

    DECLARE cursor_finished CURSOR FOR
        SELECT i.Image_L, b.title, b.average_rating, b.num_pages, b.isbn13
        FROM books b
        INNER JOIN imagedata i ON b.isbn13 = i.isbn13
        ORDER BY b.average_rating DESC;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cursor_finished;

    read_loop: LOOP
        FETCH cursor_finished INTO image_url, book_title, avg_rating, num_pages, isbn_13;
        IF done THEN
            LEAVE read_loop;
        END IF;
        -- Insert the fetched data into the temporary table
        INSERT INTO temp_top_rated_books (Image_L, title, average_rating, num_pages, isbn13)
        VALUES (image_url, book_title, avg_rating, num_pages, isbn_13);
    END LOOP;

    CLOSE cursor_finished;

    -- Return the number of rows inserted into the temporary table
    RETURN (SELECT COUNT(*) FROM temp_top_rated_books LIMIT 100);
END //

DELIMITER ;
