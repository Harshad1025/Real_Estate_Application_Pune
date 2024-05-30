import streamlit as st
import pandas as pd
from pathlib import Path
import sqlite3



DB_FILE = Path("datasets/page_5/feedback.db").resolve()

# Function to create a connection to the SQLite database
def create_connection():
    return sqlite3.connect(DB_FILE)

# Function to create the feedback table if it doesn't exist
def create_feedback_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, feedback TEXT, rating INTEGER)''')
    conn.commit()
    conn.close()

# Function to load feedback from the SQLite database
def load_feedback():
    create_feedback_table()  # Ensure the table exists
    conn = create_connection()
    feedback_df = pd.read_sql_query("SELECT name, feedback, rating FROM feedback", conn)
    conn.close()
    return feedback_df

# Function to save feedback to the SQLite database
def save_feedback(name, feedback, rating):
    create_feedback_table()  # Ensure the table exists
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO feedback (name, feedback, rating) VALUES (?, ?, ?)", (name, feedback, rating))
    conn.commit()
    conn.close()
    # Function to check if feedback has already been submitted
def check_feedback_submitted():
    if "feedback_submitted" not in st.session_state:
        st.session_state.feedback_submitted = False

def main():
    # Check if feedback has already been submitted from this machine
    check_feedback_submitted()

    # Page title and custom CSS
    st.markdown("""
    <style>
    .title {
        color: #1f77b4;
        font-size: 36px;
        text-align: center;
    }
    .header {
        color: #E37546;
        font-size: 24px;
        margin-bottom: 10px;
    }
    .input-box, .feedback-box {
        width: 100%;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 5px;
        border: 1px solid #cccccc;
        box-sizing: border-box;
        font-size: 16px;
    }
    .button {
        background-color: #007bff;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
    .button:hover {
        background-color: #0056b3;
    }
    .rating-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    .rating-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 2px solid #cccccc;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 18px;
        cursor: pointer;
    }
    .rating-circle:hover {
        background-color: #f0f0f0;
    }
    .rating-circle.active {
        border-color: #007bff;
        background-color: #007bff;
        color: white;
    }
    .project-link {
        margin-top: 20px;
        color: #4CAF50;
    }
    .github-repo {
        margin-top: 20px;
        color: #FFFFFF;
        background-color: #24292E;
        padding: 8px 16px;
        border-radius: 5px;
    }
    .rating-numbers {
        display: flex;
        justify-content: space-around;
    }
    </style>
    """, unsafe_allow_html=True)

    # Page title
    st.markdown("<h1 class='title'>📝 Project Overview</h1>", unsafe_allow_html=True)
    st.markdown(" ")

    # Add guideline
    st.markdown("<p style='font-size: 18px; font-weight: bold; color: #F8E85E;'>Guideline: Please review the project overview carefully and provide your feedback below.</p>"
            "<p style='font-size: 18px; font-weight: bold;'>Scroll down to provide your feedback.</p>", unsafe_allow_html=True)




    # Document link
    st.markdown("<h2 class='header'>Project Document Link</h2>", unsafe_allow_html=True)
    doc_link = "https://1drv.ms/w/s!AqcUYeNbwH1Flj_JITuLZVzKO33V?e=uo2dxA"
    st.markdown(f"<a href='{doc_link}' class='project-link' target='_blank'>📄 View Document</a>", unsafe_allow_html=True)

    # GitHub repo link
    st.markdown("<h2 class='header'>Project GitHub Repo</h2>", unsafe_allow_html=True)
    github_link = "https://github.com/Harshad1025/Real_Estate_Application_Pune"
    st.markdown(f"<a href='{github_link}' class='github-repo' target='_blank'>💻 GitHub Repository</a>", unsafe_allow_html=True)

    st.markdown("<p style='font-size: 18px; font-weight: bold; color: #00FF00;'>If you appreciate my work, please consider giving this repository a star on GitHub.</p>"
    , unsafe_allow_html=True)
        # HTML content
    html_content = """
    <h3 style="text-align: center; width: 30px;"></h3>
    <hr>
    <h3 align="center">Hi there, I'm Harshad Thombre! <img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="30px"/></h3>
    <h4 align="center">Data Science | Data Analytics | Machine Learning</h4>

    <p align="center">
      🌏 Location: Pune, India
    </p>

    <p align="center">
      🎓 Currently delving deeper into Data Science 📊
    </p>

    <p align="center">
      💬 Ask me about Python, Data Science/Analytics, Machine Learning
    </p>

    <p align="center">
      ✉️ Contact me at <a href="mailto:harshadthombre25@gmail.com">harshadthombre25@gmail.com</a>
    </p>

    ---

    <h3 align="center">Connect with me:</h3>

    <p align="center">
        <a href="https://github.com/Harshad1025" target="_blank">
    <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/github.svg" alt="Harshad1025" width="40" height="40" style="filter: invert(0.5);" />
    </a>
      <a href="https://www.linkedin.com/in/harshad-thombre-3a97bb280" target="_blank"><img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/linkedin.svg" alt="Harshad Thombre" width="40" height="40" /></a>
      <a href="https://www.hackerrank.com/profile/harshadthombre16" target="_blank"><img src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/hackerrank.svg" alt="Harshad Thombre" width="40" height="40" /></a>
      <a href="https://www.novypro.com/profile_about/harshad-thombre" target="_blank"><img src="https://ik.imagekit.io/novypro/novyPro/novipro%20favicon.png?updatedAt=1705624310687" alt="Novypro" width="40" height="40" ;" /></a>

    </p>

    ---

    <h3 align="center">Languages and Tools:</h3>

    <p align="center">
      <a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" width="40" height="40"/> </a>
      <a href="https://pandas.pydata.org/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="Pandas" width="40" height="40"/> </a>
      <a href="https://seaborn.pydata.org/" target="_blank"> <img src="https://seaborn.pydata.org/_images/logo-mark-lightbg.svg" alt="Seaborn" width="40" height="40"/> </a> 
     <a href="https://scikit-learn.org/stable/" target="_blank"> <img src="https://scikit-learn.org/stable/_static/scikit-learn-logo-small.png" alt="Scikit-learn" width="40" height="40"/> </a>
      <a href="https://git-scm.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="Git" width="40" height="40"/> </a>
      <a href="https://www.mysql.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" alt="MySQL" width="40" height="40"/> </a>
      <a href="https://www.postgresql.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="PostgreSQL" width="40" height="40"/> </a>
    </p>
    """

    # Display HTML content
    st.markdown(html_content, unsafe_allow_html=True)
    # About Me
    st.markdown("<h2 class='header'>About Me</h2>", unsafe_allow_html=True)
    st.write("""
    I am an aspiring Data Science enthusiast with a strong foundation in Data Science and ongoing coursework in Data Science through Almabetter. Proficient in SQL, Python, and key data visualization tools like Matplotlib and Pandas, I am also gaining hands-on experience with Machine Learning Algorithms for predictive analysis. Additionally, I am familiar with database management systems such as MySQL and PostgreSQL.

    As a fresher, I am eager to apply my skills and learn from experienced professionals in a collaborative environment. I am passionate about leveraging data to drive insights and contribute to innovative solutions.

    Open to work:
    - Jr Data Scientist
    - ML Intern
    - Data Analyst
    - Business Analyst
    - Data Science related roles

    """)
    st.markdown("---")

    # Feedback section
    st.markdown("<h2 class='header'>Feedback</h2>", unsafe_allow_html=True)


    if not st.session_state.feedback_submitted:
        with st.form(key='feedback_form'):
            name = st.text_input("Your Name", value="", placeholder="Enter your name", key="name_input")
            feedback = st.text_area("Your Feedback", value="", placeholder="Enter your feedback", key="feedback_input")
            rating = st.slider("Your Rating", 1.0, 5.0, 5.0, step=0.1, format="%.1f")

            submit_button = st.form_submit_button(label='Submit')
            st.markdown("""
            <style>
                .stTextInput>div>div>div>input {
                    border-radius: 5px;
                    border: 1px solid #cccccc;
                    padding: 10px;
                    font-size: 16px;
                    width: 100%;
                }
                .stTextArea>div>textarea {
                    border-radius: 5px;
                    border: 1px solid #cccccc;
                    padding: 10px;
                    font-size: 16px;
                    width: 100%;
                }
            </style>
        """, unsafe_allow_html=True)
    
            if submit_button:
                if name and feedback:
                    save_feedback(name, feedback, rating)
                    st.write("Thank you for your feedback!")
                    st.write(f"Name: {name}")
                    st.write(f"Feedback: {feedback}")
                    st.write(f"Rating: {rating}")
                    st.session_state.feedback_submitted = True
                else:
                    st.write("Please provide your name and feedback.")
    else:
        st.write("You have already submitted feedback.")
                        # CSS styling for input elements
            

           






    # JavaScript to handle rating selection
    st.markdown("""
    <script>
    let rating = null;
    function setRating(ratingValue) {
        rating = ratingValue;
        for (let i = 1; i <= 5; i++) {
            const circle = document.getElementById(`rating-circle-${i}`);
            if (i <= ratingValue) {
                circle.classList.add('active');
            } else {
                circle.classList.remove('active');
            }
        }
    }
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
