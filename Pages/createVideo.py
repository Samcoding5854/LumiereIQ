import streamlit as st
import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video

# Main function
def CREATEGIF():
    st.title("Create photoshoot visual video")

    pipeline = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid-xt", torch_dtype=torch.float16, variant="fp16"
    )
    pipeline.enable_model_cpu_offload()

    image = load_image("Assets/output/images/overlay_image.png")
    image = image.resize((1024, 576))

    generator = torch.manual_seed(42)
    frames = pipeline(image, decode_chunk_size=8, generator=generator).frames[0]
    export_to_video(frames, "Assets/output/videos/generated.mp4", fps=7)
    video_file = open('Assets/output/videos/generated.mp4', 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)


if __name__ == "__main__":
    CREATEGIF()


