import streamlit as st

def ABOUTUS():
    st.title('About Me')
    st.write("""
    Welcome to the Streamlit app for making a photoshoot visual! We are a team of developers passionate about creating 
    innovative solutions using Streamlit.
    """)

# Project description
    project_description = """
    **Project Title: Detective Mastermind**

    **Description:**
    Detective Mastermind is an interactive murder mystery game that immerses players in a captivating storyline filled with suspense and intrigue. Through a combination of storytelling and gameplay mechanics, players become detectives tasked with solving a complex homicide case. Key features include:

    - **Engaging Narrative:** Dive into a gripping storyline filled with twists and turns, driven by vivid descriptions and character interactions.
    - **Dynamic Suspects:** Investigate a cast of unique suspects, each with their own motives, alibis, and relationships with the victim.
    - **Progressive Hint System:** Receive subtle hints to guide the investigation without giving away the solution, encouraging critical thinking and deduction.
    - **Interactive Gameplay:** Explore crime scenes, gather evidence, and interview suspects through interactive elements such as multiple-choice questions and decision-making scenarios.
    - **Stable Diffusion Integration:** Visualize the crime scene with lifelike images generated using Stable Diffusion technology, enhancing the immersive experience.

    **Objective:**
    Challenge your problem-solving skills and analytical thinking as you unravel the mystery behind the murder. Piece together clues, examine evidence, and make informed decisions to identify the culprit and bring them to justice.

    **Audience:**
    Designed for players who enjoy solving puzzles and engaging in immersive storytelling, Detective Mastermind appeals to a broad audience of casual gamers and mystery enthusiasts.

    **Platform:**
    Accessible as a web-based application on desktop and mobile devices, Detective Mastermind offers seamless gameplay across various platforms with a user-friendly interface and intuitive controls.

    **Conclusion:**
    Prepare to embark on a thrilling journey filled with mystery and suspense in Detective Mastermind. Whether you're a novice detective or a seasoned sleuth, test your investigative skills and uncover the truth behind the murder in this immersive murder mystery game.
    """

    # Display project description
    st.title("Detective Mastermind: Solve the Murder Mystery")
    st.image('App/logo.jpg', caption='Our Logo', width = 400)
    st.write(project_description)

    
    st.subheader('Team Members')
    st.write("""
    Meet the minds behind this project:
    """)
    
    # Member 1
    st.write("*Darsh Baxi*")
    st.image('App/darsh.jpg', width=200)
    st.write("GitHub: [Darsh Baxi](https://github.com/darshbaxi)")
    st.write("LinkedIn: [Darsh Baxi](https://www.linkedin.com/in/darsh-baxi-81350124a/)")
    
    # Member 2
    st.write("*Samarth Sahu*")
    st.image('App/samarth.jpg', width=200)
    st.write("GitHub: [Samarth Sahu](https://github.com/Samcoding5854/)")
    st.write("LinkedIn: [Samarth Sahu](https://www.linkedin.com/in/samarth-sahu/)")

    st.write("""
    Feel free to explore our app and reach out to us for any questions or feedback!
    """)