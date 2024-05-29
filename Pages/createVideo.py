import streamlit as st
import os
import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video

# Function to get the list of images in a specified folder without extensions
def get_image_list(folder_path):
    return [os.path.splitext(f)[0] for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('png', 'jpg', 'jpeg'))]

# Main function
def CREATEGIF():
    st.title("Create Photoshoot Visual Video")

    # Folder containing images
    image_folder = "Assets/output/images"

    # Get the list of images from the folder
    image_list = get_image_list(image_folder)

    # Selectbox to choose an image
    selected_image_name = st.selectbox("Select an image:", image_list)

    # Button to start the video generation
    if st.button("Generate Video"):
        # Full path of the selected image (adding back the extensions for loading the image)
        for ext in ['png', 'jpg', 'jpeg']:
            selected_image_path = os.path.join(image_folder, f"{selected_image_name}.{ext}")
            if os.path.exists(selected_image_path):
                break

        # Load the image and resize it
        image = load_image(selected_image_path)
        image = image.resize((1024, 576))

        # Spinner during video generation
        with st.spinner("Generating video..."):
            pipeline = StableVideoDiffusionPipeline.from_pretrained(
                "stabilityai/stable-video-diffusion-img2vid-xt", torch_dtype=torch.float16, variant="fp16"
            )
            pipeline.enable_model_cpu_offload()

            generator = torch.manual_seed(42)
            frames = pipeline(image, decode_chunk_size=8, generator=generator).frames[0]

            # Create output directory if it doesn't exist
            output_dir = "Assets/output/videos"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, "generated.mp4")
            export_to_video(frames, output_path, fps=7)

        # Display the generated video
        video_file = open(output_path, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

if __name__ == "__main__":
    CREATEGIF()
