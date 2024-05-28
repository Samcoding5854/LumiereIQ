from PIL import Image
import streamlit as st
import os
from Pages.imageBB import run

# Main function
def CREATEVISUALS():
    st.title("Create photoshoot visual")

    # Set the directory where the uploaded images will be saved
    UPLOAD_DIR = 'Assets/uploaded_images'

    # Create the directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Streamlit app title
    st.header("Upload image")

    # File uploader allows user to upload an image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Open the uploaded image
        image = Image.open(uploaded_file)

        # Save the uploaded image to the specified directory
        image_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        image.save(image_path)
        
        st.write(f"Image Saved")
        run(image_path)


    else:
        st.write("No image uploaded yet.")

if __name__ == "__main__":
    CREATEVISUALS()


