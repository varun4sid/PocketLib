# PocketLib
A personal library management app to maintain the status of books (extended to multiple users)

<br>

# Features

## Home Page
Currently displays top ten books by ratings

https://github.com/luqmaan-k/PersonalLibrary/assets/141229528/a7474966-0f89-4ed0-a20c-950eed121988

<br>

## Login / Signup System
A login/signup system ,currently stores login info in the database (no 2fa).

A guest user login is also provided.


https://github.com/luqmaan-k/PersonalLibrary/assets/141229528/31374bd7-5706-45d5-9a5e-fcbc1bd8f325

<br>

## User Page
Shows the status of books of the currently logged in user.

Use the menu bar to the left to filter and (or) add entries.

https://github.com/luqmaan-k/PersonalLibrary/assets/141229528/bd04bd7c-52e9-4e8b-8ccc-5696333779a3

<br>

# Local Deployment

###### Prerequisites
Make sure to use the database file from the [releases tab](https://github.com/luqmaan-k/PersonalLibrary/releases/)

Drop the database file (library.db in the same directory where you run the below command from)

1. Clone the repo
```bash
git clone https://github.com/varun4sid/PocketLib.git
cd PocketLib
```

2. Create a virtual environment and install required packages
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the app from the virtual environment
```bash
streamlit run app.py
```

<br>

# Contributors
**[luqmaan-k](https://github.com/luqmaan-k)**

<br>

# Misc
+ The project uses [Hydralith](https://github.com/TangleSpace/hydralit) for the navbar
+ The data was aquired from a few sources from [kaggle](https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks) 
+ The database was built using sqlite3 but can be easily swapped to better dbs