# home.py
import streamlit as st
from textblob import TextBlob
# from pages.history import set_background
import pymongo

# Establish connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["sentiment_analysis"]


# set_background()
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"


def main():
    st.title("know the :blue[sentiment]")
    st.write("analyze the sentiment of the text you input.")
    user_email = st.session_state.email

    if "PROMPTS" not in st.session_state:
        st.session_state.PROMPTS = []
    if "SENTIMENTS" not in st.session_state:
        st.session_state.SENTIMENTS = []

    user_input = st.text_area(":red[Enter text here:]", height=70)
    if st.button("Analyze"):
        if user_input:
            sentiment = analyze_sentiment(user_input)
            st.write("Sentiment:", sentiment)
            st.session_state.PROMPTS.append(user_input)
            st.session_state.SENTIMENTS.append(sentiment)

            # Update user's document in the database with the new prompt and sentiment
            db.my_users.update_one(
                {"email": user_email},
                {"$push": {"prompts": user_input, "sentiments": sentiment}}
            )

            if sentiment == "Positive":
                st.success("😊 This text has a positive sentiment!")
            elif sentiment == "Negative":
                st.error("😞 This text has a negative sentiment.")
            else:
                st.info("😐 This text has a neutral sentiment.")
        else:
            st.warning("Please enter some text.")

    st.page_link("pages/history.py", label="History")


if __name__ == '__main__':
    try:
        main()
    except AttributeError:
        st.switch_page("pages/signin.py")
