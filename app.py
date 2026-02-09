import streamlit as st
from utils import get_ai_response


def main():
    st.set_page_config(page_title="TalentScout AI", page_icon="🤖")
    st.title("🤖 TalentScout Hiring Assistant")
    st.markdown("Welcome! I am here to help you with your initial screening.")
    # 1. Initialize Chat History
    # We check if 'messages' exists in session_state. If not, we create it.
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Adding an initial greeting from the bot automatically
        first_greeting = "Hello! I am the TalentScout Hiring Assistant. I'd love to learn a bit about you. To start, could I get your full name?"
        st.session_state.messages.append({"role": "assistant", "content": first_greeting})

    # 2. Display Chat History
    # This loop draws the previous messages every time the app refreshes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. Handle User Input
    # st.chat_input creates the text box at the bottom
    if user_input := st.chat_input("Type your answer here..."):
        
        # A. Display User Message immediately
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # B. Save User Message to History
        st.session_state.messages.append({"role": "user", "content": user_input})

        # C. Get AI Response
        # We show a "spinner" while waiting for the AI to think
        with st.spinner("Thinking..."):
            ai_reply = get_ai_response(st.session_state.messages)

        # D. Display AI Message
        with st.chat_message("assistant"):
            st.markdown(ai_reply)
        
        # E. Save AI Message to History
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

if __name__ =="__main__":
    main()
