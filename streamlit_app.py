import streamlit as st
import streamlit_chat as chat

# Initialize session state variables if they do not exist
if 'user' not in st.session_state:
    st.session_state.user = []

if 'bot' not in st.session_state:
    st.session_state.bot = []

# Function to handle chat interaction
def chat1(q):
    l =len(st.session_state.user)
    st.session_state.user.append(q)
    st.session_state.bot.append("Hi! how can I help you? " + q)

    # Display messages in chat
    for i, j,k in zip(st.session_state.user, st.session_state.bot,range(l)):
        chat.message(i, is_user=True, key=f"user_{i+str(k)}")
        chat.message(j, is_user=False, key=f"bot_{j+str(k)}")

# Input field and button
q = st.text_input("Please write:")
if st.button("Hello"):
    if q:  # Ensure input is not empty
        chat1(q)
