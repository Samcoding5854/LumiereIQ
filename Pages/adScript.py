import streamlit as st
import google.generativeai as genai

def CREATEAD():
    st.title("Create a script/idea")

    prompt = st.text_input("Write about product/Advertisement Idea you already have.")

    if prompt:

        # Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel('gemini-1.5-flash')

        response = model.generate_content(f"Write a funny short advertisement script for this {prompt}", stream=True)
        response.resolve()

        st.write(response.text)


if __name__ == "__main__":
    CREATEAD()


