from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
# from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.environ.get('groq_api_key')

llm = ChatGroq(
    temperature=0.7,
    groq_api_key=groq_api_key,
    model_name="llama-3.1-70b-versatile"
).with_structured_output(dict,method="json_mode")



quiz_template_content = PromptTemplate.from_template(
   """
    generate {number} multiple-choice questions from the following content in JSON format with the structure: 
    questions:[{{"question_number", "question", "option_a", "option_b", "option_c", "option_d", "answer"}}]:
    
    {content}
    
    Output only valid JSON without any preamble or commentary.
    """
)



quiz_template_topic = PromptTemplate.from_template(
    """
    generate {number} multiple-choice questions on the topic "{topic}" in JSON format with the structure: 
    questions:[{{"question_number", "question", "option_a", "option_b", "option_c", "option_d", "answer"}}]:
    
    Output only valid JSON without any preamble or commentary.
    """
)


def generate_quiz(num, content=None, topic=None):
    if content:
        template = quiz_template_content
        quiz_chain = template | llm
        quiz_result = quiz_chain.invoke({'number': num, 'content': content})
    elif topic:
        template = quiz_template_topic
        quiz_chain = template | llm
        quiz_result = quiz_chain.invoke({'number': num, 'topic': topic})
    else:
        raise ValueError("Either content or topic must be provided")
    
    try: 
        return quiz_result['questions']
    except KeyError:
        raise OutputParserException("Unable to parse: 'questions' key not found in response.")