import streamlit as st

def main():
    st.title("TalentScout Hiring Platform")
    st.write("Lets get this chatbot running")
    st.sidebar.title("Options")
    user_input = st.text_input("Say hello")
    if user_input:
        st.write(f"You said: {user_input}")

if __name__ =="__main__":
    main()
