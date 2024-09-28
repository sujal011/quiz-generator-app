from scrap import extract_article_text
from quiz import generate_quiz
import streamlit as st
from create_form import create_google_form


st.title("Article to Quiz Generator")

# Add a radio button to let the user select between entering a URL or a topic
choice = st.radio("Select input method:", ("Enter URL", "Enter Topic"))

# Conditional input fields based on user's choice
if choice == "Enter URL":
    url = st.text_input("Enter the URL of the article:")
    if(not url.startswith('http')):
        st.error("Please enter a valid URL.")
    topic = None
else:
    topic = st.text_input("Enter the topic name to generate quiz:")
    url = None


num_questions = st.number_input("Number of questions:", min_value=1, value=10)

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

if st.button("Generate Quiz"):
    if url :
        with st.spinner("Extracting article text..."):
            article_text = extract_article_text(url)
            
        if article_text:
            with st.spinner("Generating quiz..."):
                try:
                    st.session_state.quiz_data = generate_quiz(num_questions,content=article_text)
                    
                    if st.session_state.quiz_data:  # Ensure quiz_data is not empty
                        st.success("Quiz generated successfully!")
                except Exception as e:
                    st.error(f"Failed to generate quiz: {str(e)}")
                    # for question in quiz_data:
                    #     st.write(f"**Q{question['question_number']}: {question['question']}**")
                    #     st.write(f"a) {question['option_a']}")
                    #     st.write(f"b) {question['option_b']}")
                    #     st.write(f"c) {question['option_c']}")
                    #     st.write(f"d) {question['option_d']}")
                    #     st.write("")
                    #     st.write(f"Answer: {question['answer']}")
                    #     st.write("---")
                except Exception as e:
                    st.error(f"Failed to generate quiz: {str(e)}")
        else:
            st.error("Failed to extract text from the article.")
    elif topic:
        with st.spinner("Generating quiz..."):
            try:
                st.session_state.quiz_data = generate_quiz(num_questions,topic=topic)  
                
                if st.session_state.quiz_data:  # Ensure quiz_data is not empty
                    st.success("Quiz generated successfully!")
            except Exception as e:
                    st.error(f"Failed to generate quiz: {str(e)}")
    else:
        st.error("Please enter a valid URL.")
        
  
if  st.session_state.quiz_data:  # Ensure quiz_data is not empty
                    for question in  st.session_state.quiz_data:
                        st.write(f"**Q{question['question_number']}: {question['question']}**")
                        st.write(f"a) {question['option_a']}")
                        st.write(f"b) {question['option_b']}")
                        st.write(f"c) {question['option_c']}")
                        st.write(f"d) {question['option_d']}")
                        st.write("")
                        st.write(f"Answer: {question['answer']}")
                        st.write("---")
                    
                    if st.button("Create Google Quiz"):
                        st.write("Creating Google Form...")

                        # Call form creation logic and display the form URL
                        form_url = create_google_form(st.session_state.quiz_data)
                        if form_url:
                            st.success(f"Google Form created! [Click here to view the form]({form_url})")
                        else:
                            st.error("Failed to create Google Form.")
               
