# full_history.py
import streamlit as st
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["sentiment_analysis"]  # Replace "sentiment_analysis" with your database name
col1, col2, col3 = st.columns(3)


def show_full_history():
    # Fetch user's email from session state
    user_email = st.session_state.email

    # Query the database to retrieve the user's document based on their email
    user1 = db.my_users.find_one({"email": user_email})

    if user1:
        if "prompts" in user1 and "sentiments" in user1:
            st.session_state.prompts = user1["prompts"]
            st.session_state.sentiments = user1["sentiments"]
            with col2:
                st.write("Full History:")
                table ={"prompts": st.session_state.prompts,
                        "sentiment": user1["sentiments"]
                       }
                st.dataframe(table, width=500, height=500)  # Display prompts
                st.page_link("pages/history.py",label=":blue[show less history]")
        else:
            st.write("No full history available.")
    else:
        st.write("User not found.")


if __name__ == '__main__':

    try:
        show_full_history()
    except(AttributeError):
        st.switch_page("pages/signin.py")
