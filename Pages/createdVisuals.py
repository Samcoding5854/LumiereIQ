import os
import streamlit as st

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            images.append(os.path.join(folder, filename))
    return images

def get_image_name(image_path):
    return os.path.splitext(os.path.basename(image_path))[0]

# Main function
def CREATEDIMAGES():
    st.title("Created Images")
 
    # Path to the folder containing images
    image_folder = "Assets/output/images"

    # Load images from the folder
    images = load_images_from_folder(image_folder)

    # Display images and information in a grid layout with three images per row
    col_width = 350  # Adjust this value according to your preference
    num_images = len(images)
    images_per_row = 3
    num_rows = (num_images + images_per_row - 1) // images_per_row

    st.header('Available Templates', divider='red')

    # Display images and information in a grid layout with three images per row
    for i in range(num_rows):
        cols = st.columns(images_per_row)
        for j in range(images_per_row):
            idx = i * images_per_row + j
            if idx < num_images:
                image_name = get_image_name(images[idx])
                cols[j].image(images[idx], width=col_width)
                cols[j].write(image_name)

if __name__ == "__main__":
    CREATEDIMAGES()
