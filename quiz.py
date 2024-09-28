from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.environ.get('groq_api_key')

llm = ChatGroq(
    temperature=0.7,
    groq_api_key=groq_api_key,
    model_name="llama-3.1-70b-versatile"
)

# quiz_template = PromptTemplate.from_template(
#     """
#     ### generate a {number} mcq based quiz on following:
#     {content}
    
#     also separate each option with new line character for better visibility
#     """
# )



# quiz_chain = quiz_template | llm
# quiz_result = quiz_chain.invoke({'number':10,'topic': 'next js'})
# print(quiz_result.content)


quiz_template_content = PromptTemplate.from_template(
    """
    generate a {number} numbers of mcq based quiz from following content in JSON format similar to : questions:[{{ question_number, question, option_a,option_b,option_c,option_d, answer }}]:
    
    {content} 
    
    output should only contain VALID JSON and NO PREAMBLE
    """
)


def generate_quiz_from_content(num,content):
    quiz_chain = quiz_template_content | llm
    quiz_result = quiz_chain.invoke({'number':num,'content': content})
    
    try: 
        json_parser = JsonOutputParser()
        res = json_parser.parse(quiz_result.content)
        return res['questions']
    except OutputParserException:
        raise OutputParserException("Unable to parse")


quiz_template_topic = PromptTemplate.from_template(
    """
    generate a {number} numbers of mcq based quiz on {topic} in JSON format similar to : questions:[{{ question_number, question, option_a,option_b,option_c,option_d, answer }}]
    
    output should only contain VALID JSON and NO PREAMBLE
    """
)


def generate_quiz_from_topic(num,topic):
    quiz_chain = quiz_template_topic | llm
    quiz_result = quiz_chain.invoke({'number':num,'topic': topic})
    
    try: 
        json_parser = JsonOutputParser()
        res = json_parser.parse(quiz_result.content)
        return res['questions']
    except OutputParserException:
        raise OutputParserException("Unable to parse")

