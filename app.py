import os
import streamlit as st
from Pages.createVisual import CREATEVISUALS
from Pages.AboutMe import ABOUTUS
from Pages.bgImages import BGIMAGES
from Pages.createdVisuals import CREATEDIMAGES
from Pages.createVideo import CREATEGIF
from Pages.objectRecognize import DETECTIMAGE
from Pages.adScript import CREATEAD


st.set_page_config(
        page_title="LumiereIQ",
        page_icon="📸",
        layout="wide",  # 'centered' or 'wide'
        initial_sidebar_state="expanded"  # 'auto', 'expanded', 'collapsed'
    )

def MAIN():
    weights_dir = 'weights'
    weights_file = os.path.join(weights_dir, 'sam_vit_h_4b8939.pth')

    # Check if the weights file already exists
    if not os.path.exists(weights_file):
        # Create the directory if it doesn't exist
        if not os.path.exists(weights_dir):
            os.makedirs(weights_dir)
        
        # Define the download command
        download_command = f"wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -P {weights_dir}"

        # Execute the download command
        os.system(download_command)
        print("Weights downloaded.")
    else:
        print("Weights file already exists. No download needed.")

    # Verify the file is downloaded
    file_path = os.path.expanduser("~/weights/sam_vit_h_4b8939.pth")
    if os.path.exists(file_path):
        print("File downloaded successfully.")
    else:
        print("File download failed.")

    # Rest of your application code

    st.sidebar.title('LumiereIQ')
    app = st.sidebar.selectbox('', ['Create Visuals','Background Images','Recognize Object', 'Create Script', 'Created Images','Create Video'])
    if app == "Create Visuals":
        CREATEVISUALS()
    elif app == "About Me":
        ABOUTUS()
    elif app == "Background Images":
        BGIMAGES()
    elif app == "Create Video":
        CREATEGIF()
    elif app == "Created Images":
        CREATEDIMAGES()
    elif app == "Recognize Object":
        DETECTIMAGE()
    elif app == "Create Script":
        CREATEAD()
          
MAIN()