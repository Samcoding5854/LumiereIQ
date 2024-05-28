import PIL.Image
import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

def DETECTIMAGE():
    st.title("Create photoshoot visual")

    # Set the directory where the uploaded images will be saved
    UPLOAD_DIR = 'Assets/uploaded_images'

    # Create the directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Streamlit app title
    st.header("Upload Image")

    # File uploader allows user to upload an image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        with st.spinner('Processing the image...'):
            # Open the uploaded image
            image = Image.open(uploaded_file)

            # Save the uploaded image to the specified directory
            image_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            image.save(image_path)

            img = PIL.Image.open(image_path)
            st.image(img, caption="Uploaded Image")

            # Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
            GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

            genai.configure(api_key=GOOGLE_API_KEY)

            model = genai.GenerativeModel('gemini-1.5-flash')

            # Generate content
            response = model.generate_content(["Is the image anything from this list? (Shoe,Sneaker, Bottle, Cup, Sandal, Perfume, Toy, Sunglasses, Car, Water Bottle,Chair, Office Chair, Can, Cap, Hat, Couch, Wristwatch, Glass, Bag, Handbag, Baggage, Suitcase, Headphones, Jar, Vase) If yes then give only the object name, if no simply say 'Not Recognized' and dont give any fullstop at the end.", img], stream=True)
            response.resolve()

            st.subheader(f"Output: {response.text}")

if __name__ == "__main__":
    DETECTIMAGE()
