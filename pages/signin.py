import time

import streamlit as st
from pymongo import MongoClient
from passlib.hash import bcrypt


# Function to connect to MongoDB
def connect_to_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['sentiment_analysis']

    return db


# Function to check if user exists
def user_exists(email):
    user = db.my_users.find_one({'email': email})
    return user is not None


# Function to create a new user
def create_user(name, email, password):
    hashed_password = bcrypt.hash(password)
    db.my_users.insert_one({'name': name, 'email': email, 'password': hashed_password, 'prompts': [], 'sentiments':[]})


# Function to verify password
def verify_password(stored_password, password):
    return bcrypt.verify(password, stored_password)



# Main function
def main():
    st.title("Login Page")

    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Login", "Sign Up"],horizontal= True)

    # Connect to MongoDB
    global db
    db = connect_to_mongodb()

    if page == "Login":
        st.subheader("Login")


        st.session_state.email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = db.my_users.find_one({'email': st.session_state.email})
            if user and verify_password(user['password'], password):
                st.success("Logged in successfully!")
                time.sleep(2)
                st.switch_page("pages/home.py")


            else:
                st.error("Invalid email or password.")

    elif page == "Sign Up":
        st.subheader("Sign Up")

        name = st.text_input("Name")
        st.session_state.email= st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Sign Up") :
            if not "@gmail.com" in st.session_state.email:
                st.error("enter valid email address")
            elif user_exists(st.session_state.email):
                st.error("User already exists with this email.")
            else:
                create_user(name, st.session_state.email, password)
                st.success("User created successfully! You can now login.")
                time.sleep(1)

# create logout function



# Render the main function
if __name__ == "__main__":
    main()
