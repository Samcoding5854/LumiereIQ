from segment_anything import sam_model_registry, SamPredictor
import torch
import streamlit as st
from Pages.streamlit_img_label import st_img_label
from Pages.streamlit_img_label.manage import ImageManager
import os
from PIL import Image
import cv2
import numpy as np

@st.cache_data
def get_masks(rect, img_path):
    CHECKPOINT_PATH = os.path.join("weights", "sam_vit_h_4b8939.pth")
    DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    MODEL_TYPE = "vit_h"
    sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH).to(device=DEVICE)
    mask_predictor = SamPredictor(sam)

    rect = np.array([
        rect['left'],
        rect['top'],
        rect['left'] + rect['width'],
        rect['top'] + rect['height']
    ])
    image_bgr = cv2.imread(img_path)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    mask_predictor.set_image(image_rgb)

    masks, scores, logits = mask_predictor.predict(
        box=rect,
        multimask_output=False
    )
    return masks

def run(img_path):
    st.set_option("deprecation.showfileUploaderEncoding", False)

    im = ImageManager(img_path)
    resized_img = im.resizing_img()
    resized_rects = im.get_resized_rects()

    if "rects" not in st.session_state:
        st.session_state.rects = resized_rects

    # Only display st_img_label if Save button hasn't been clicked
    if not st.session_state.get("saved"):
        rects = st_img_label(resized_img, box_color="red", rects=st.session_state.rects)
        st.session_state.rects = rects
    else:
        st.image(resized_img, caption="Uploaded Image", width=300, use_column_width=True)

        for rect in st.session_state.rects:
            with st.spinner('Please wait while the product image is being extracted...'):
                masks = get_masks(rect, img_path)

                save_dir = "Assets/saved_masks"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                for i, mask in enumerate(masks):
                    inverted_mask = 255 - (mask * 255).astype(np.uint8)
                    file_path = os.path.join(save_dir, f"inverted_mask_{i}.png")
                    cv2.imwrite(file_path, inverted_mask)

                print(f"Inverted masks saved to directory: {save_dir}")

            image_files = [f for f in os.listdir("Assets/bgImages") if os.path.isfile(os.path.join("Assets/bgImages", f))]

            st.header("Template Selection")
            # Create a dropdown with the list of image files
            selected_image = st.selectbox("Select an image file", image_files)

            if selected_image:
                # Display the selected image
                image_pathBG = os.path.join("Assets/bgImages", selected_image)
                image = Image.open(image_pathBG)
                st.image(image, width=300, caption=f"Selected image: {selected_image}")

                if st.button("Create Image"):
                    st.session_state.create_image = True

        if st.session_state.get("create_image"):
            # Read the base image and background image
            image_bgr = cv2.imread(img_path)
            background_bgr = cv2.imread(image_pathBG)

            # Resize the background image to match the size of image_bgr
            background_bgr = cv2.resize(background_bgr, (image_bgr.shape[1], image_bgr.shape[0]))

            # Convert the base image to RGB format for mask prediction if it's not already in RGB
            if image_bgr.shape[2] == 3:  # No alpha channel, standard BGR image
                image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image_bgr[:, :, :3]  # Drop alpha channel if it exists

            # Assuming masks is a binary mask, convert it to uint8 format
            mask = (masks[0] > 0).astype(np.uint8) * 255

            # Apply a Gaussian blur to the mask to smooth the edges
            mask = cv2.GaussianBlur(mask, (3, 3), 0)

            # Ensure the image has an alpha channel
            if image_bgr.shape[2] == 3:  # If no alpha channel, add one
                b, g, r = cv2.split(image_bgr)
                alpha_channel = mask  # Use the blurred mask as the alpha channel
                image_bgra = cv2.merge((b, g, r, alpha_channel))
            else:
                image_bgra = image_bgr

            # Get the dimensions of the images
            masked_height, masked_width = image_bgra.shape[:2]
            background_height, background_width = background_bgr.shape[:2]

            # Calculate the coordinates to place the masked image in the center of the background image
            x_offset = (background_width - masked_width) // 2
            y_offset = (background_height - masked_height) // 2

            # Resize the masked image if it is larger than the background area
            if masked_width > background_width or masked_height > background_height:
                scaling_factor = min(background_width / masked_width, background_height / masked_height)
                new_size = (int(masked_width * scaling_factor), int(masked_height * scaling_factor))
                image_bgra = cv2.resize(image_bgra, new_size, interpolation=cv2.INTER_AREA)
                masked_height, masked_width = image_bgra.shape[:2]
                x_offset = (background_width - masked_width) // 2
                y_offset = (background_height - masked_height) // 2

            # Create a copy of the background image and convert it to BGRA
            background_bgra = cv2.cvtColor(background_bgr, cv2.COLOR_BGR2BGRA)

            # Overlay the masked image onto the center of the background image
            overlay_image = background_bgra.copy()

            # Only update the region where the segmented image will be placed
            overlay = np.zeros_like(background_bgra)
            overlay[y_offset:y_offset + masked_height, x_offset:x_offset + masked_width] = image_bgra

            # Create the alpha mask for blending
            alpha_mask = overlay[:, :, 3] / 255.0
            alpha_inv = 1.0 - alpha_mask

            # Modify alpha channel for smoother blending
            alpha_mask = alpha_mask ** 0.5  # Applying square root for smoother blending

            # Blend the images
            for c in range(0, 3):
                overlay_image[:, :, c] = (alpha_mask * overlay[:, :, c] + alpha_inv * overlay_image[:, :, c])

            # Set the alpha channel
            overlay_image[:, :, 3] = np.clip(overlay[:, :, 3] + background_bgra[:, :, 3], 0, 255)

            # Prompt user for the filename
            filename = st.text_input("Enter a name to save the image:")
            if filename and st.button("Save Image"):
                output_path = f'Assets/output/images/{filename}.png'
                cv2.imwrite(output_path, overlay_image)

                # Display the overlay image
                st.image(output_path, caption="Created Image", use_column_width=True, width=300)

    def annotate():
        st.session_state.saved = True

    if st.session_state.rects:
        st.button(label="Save", on_click=annotate)

# Example of calling the function
# run("path/to/your/image.jpg")
