# history.py
import streamlit as st


def main():
    st.set_page_config(page_title="History Page", layout="wide", initial_sidebar_state="expanded")
    # Apply background color to the entire page

    st.title(':cream[HISTORY] :sunglasses:')
    st.write("Chat History and Sentiments:")

    if "PROMPTS" in st.session_state and "SENTIMENTS" in st.session_state:
        table_data = {"Prompt": st.session_state.PROMPTS, "Sentiment": st.session_state.SENTIMENTS}
        st.dataframe(table_data, use_container_width=True)
    else:
        st.write("No history available.")

    # Add a link to the home page in the sidebar
    st.sidebar.page_link("pages/home.py", label="🏠 Home")

    # Show full history when the button is clicked
    st.page_link("pages/full_history.py",label=":blue[full history]")

if __name__ == '__main__':
    try:
        main()
    except(AttributeError):
        st.switch_page("pages/signin.py")

