from scrap import extract_article_text
from quiz import generate_quiz_from_topic,generate_quiz_from_content
import streamlit as st


questions=[]


st.title("Article to Quiz Generator")

# Add a radio button to let the user select between entering a URL or a topic
choice = st.radio("Select input method:", ("Enter URL", "Enter Topic"))

# Conditional input fields based on user's choice
if choice == "Enter URL":
    url = st.text_input("Enter the URL of the article:")
    topic = None
else:
    topic = st.text_input("Enter the topic name to generate quiz:")
    url = None


num_questions = st.number_input("Number of questions:", min_value=1, value=10)

if st.button("Generate Quiz"):
    if url :
        
        article_text = extract_article_text(url)
        if article_text:
            st.write("Generating quiz...")
            quiz_data = generate_quiz_from_content(num_questions,article_text)
            for question in quiz_data:
                st.write(f"**Q{question['question_number']}: {question['question']}**")
                st.write(f"a) {question['option_a']}")
                st.write(f"b) {question['option_b']}")
                st.write(f"c) {question['option_c']}")
                st.write(f"d) {question['option_d']}")
                st.write("")
                st.write(f"Answer: {question['answer']}")
                st.write("---")
        else:
            st.error("Failed to extract text from the article.")
    elif topic:
        
        st.write("Generating quiz...")
        quiz_data = generate_quiz_from_topic(num_questions,topic)
        for question in quiz_data:
            st.write(f"**Q{question['question_number']}: {question['question']}**")
            st.write(f"a) {question['option_a']}")
            st.write(f"b) {question['option_b']}")
            st.write(f"c) {question['option_c']}")
            st.write(f"d) {question['option_d']}")
            st.write("")
            st.write(f"Answer: {question['answer']}")
            st.write("---")
    else:
        st.error("Please enter a valid URL.")

