import torch
from diffusers import AutoPipelineForText2Image
from PIL import Image
import os
import streamlit as st

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            images.append(os.path.join(folder, filename))
    return images

# Main function
def BGIMAGES():
    st.title("Background Images")

    st.header('Create a template', divider='orange')

    prompt = st.text_input("Prompt for a Background")
    if prompt:
        # Load the pipeline
        with st.spinner("Loading model..."):
            pipeline = AutoPipelineForText2Image.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16"
            ).to("cuda")

        # Set the generator seed
        generator = torch.Generator("cuda").manual_seed(31)

        # Generate the image
        with st.spinner("Generating image..."):
            image_prompt = f"{prompt}, muted colors, detailed, 8k"
            image = pipeline(image_prompt, generator=generator).images[0]

        # Save the image
        output_dir = "Assets/bgImages"
        os.makedirs(output_dir, exist_ok=True)
        image_path = os.path.join(output_dir, f"{prompt}.png")
        image.save(image_path)

        # Display the image
        st.image(image, caption=f"Generated image for: {prompt}")

    else:
        st.write("Please enter a movie title to generate an image.")

    # Path to the folder containing images
    image_folder = "Assets/bgImages"

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
                image_path = images[idx]
                image_name = os.path.splitext(os.path.basename(image_path))[0]  # Get the file name without extension
                cols[j].image(image_path, width=col_width)
                cols[j].write(image_name)

if __name__ == "__main__":
    BGIMAGES()
