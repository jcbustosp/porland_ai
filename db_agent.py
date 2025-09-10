import os
import datetime
from dataclasses import dataclass
from dotenv import load_dotenv

from pydantic_ai.models import ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.messages import ModelMessage
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider

from database import db

load_dotenv(override=True)

def format_text(text:str):
    return '\n'.join(line.strip() for line in text.splitlines()).strip()


def get_model(model_name: str):
    return OpenAIChatModel(
        model_name=model_name,
        provider=OllamaProvider(base_url=os.getenv("OLLAMA_BASE_URL")),
    )

async def keep_recent_messages(messages: list[ModelMessage]) -> list[ModelMessage]:
    """Keep only the last 5 messages to manage token usage."""
    return messages[-5:] if len(messages) > 5 else messages


async def summarize_chat_messages(messages: list[ModelMessage]):
    """Summarize the history of messages and return relevant context for follow up interactions. 
    Expected input is the agent's history of messages."""
    
    if len(messages) > 5:
        messages = messages[-5:]

    summary = await summarize_agent.run(message_history=messages)
    return summary.new_messages() 


agent = Agent(
    model=get_model(os.getenv("MODEL_ROOT_AGENT")),
    system_prompt=format_text(f"""
    You are a helpful assistant tasked with translating user requests about the client / company named {os.getenv('CLIENT_NAME')}. Your sole purpose is to translate user requests into precise natural language questions for a database retrieval tool named `enquiry_database` to obtain the answers.
   
    <TASK>
    Your primary task is to analyze a user's intent regarding the {os.getenv('CLIENT_NAME')} database and convert it into a well-structured, clear question that the enquiry_database tool can process. You must be concise and direct.

    <RULES>
    - Never answer the user directly. You always formulated question for the enquiry_database tool, and based on its output provide an answer.
    - You do NOT have access to the database, if you need any information to answer the user ask for it to the `enquiry_database` tool. 
    - Never hallucinate data or supplement answers with general knowledge.
    - ALWAYS ask for the MOST RECENT available data, unless the user specifies otherwise. Today's date is {datetime.date.today()}.
    - The questions asked to the `enquiry_database` tool MUST be in natural language - do not use SQL or any other code format.
    - Handle multiple intents. If a user's request has multiple parts / is complex (e.g., "How many active users are there and what is their average age?"), you should create separate, distinct questions for each part.
    - If you call multiple times the `enquiry_database` tool, always use ALL the returned outputs to compose your answer.
    - If the user's query is out of scope, too broad or vague, answer directly and prompt the user for clarification 

    <EXAMPLES>
    ** Example 1 **
        - User Input: "How many customers do we have in total?"
        - Your Output: Ask "What is the total number of customers?" to the `enquiry_database` tool
        
    ** Example 2 **
        - User Input: "What it is the year-on-year growth sales for this month?"
        - Your Output: "What are the total sales for this month, compared to the same month last year?"
    
    """),

    # < CONSTRAINTS >
    #     * ALL user's request are about the {os.getenv('CLIENT_NAME')} company.
    #     * If the user's request is too broad or vague (e.g., refers to 'the data' without specifics, lacks of date ranges), ALWAYS use `enquiry_database` tool to tray obtaining more information on her request.
    #     * If the user's request is direct and specific, AVOID modifying it and pass it exactly as provided for the `question` parameter of the `enquiry_database` tool.
    #     * If the user's request is a follow-up question on a previous one: First use the `summarize_chat_messages` to retrieve relevant context before using the `enquiry_database` tool.
    #     * If the user's request is too complex or refers to multiple elements (e.g. comparison), break it into separated questions. Use tools accordingly to get answers, one request at a time.
    #     * If the `enquiry_database` tool does not return structured results and asks for clarification, modify / refine the `question` parameter based on user's initial request and message history.
    #     * If the user requests explanations or additional information about results, inspect the message tool's output message history to answer.
    # </ CONSTRAINTS >
    history_processors=[keep_recent_messages],
    model_settings=ModelSettings(temperature=0.0,),
)

@agent.tool_plain(retries=2)
def enquiry_database(question: str, context: str | None = None):
    """Get structured responses from a database using natural language questions. 
    
    Parameters:
        question (str): A precise and well-formulated natural language question, NOT an SQL query
        context (str): Useful context to complement the questions, it can be instructions or details 
            about the expected answer or how to approach a question
    
    Returns:
        answer (str):  An natural language answer to the input question
    """

    context_augmented = f"""
    * ALWAYS provide your the key elements of your answer first followed by a brief summary on how results were obtained (e.g. used query).
    * All user's questions about the 'client' or 'company' refer to data in this database - the client name is {os.getenv('CLIENT_NAME')}
    * By default ALWAYS consider data for MOST RECENT available date, unless the user specifies otherwise - for information today's date is {datetime.date.today()}
    * If uncertain about the correct table or column name to use, prompt the user for clarification - provide a direct response with a clear overview of the available data based on the tables schema.
    * Liquidity related questions refer to the DAILY aggregated cash position, DEFAULT to using lower bound balances in covenant currency, unless the user specifies otherwise.
    * Questions involving 'total' values refer to using aggregated data (e.g. via SUM).
    * Keep in mind that transaction data is used to compute client's liquidity data, for questions on transaction data USE ONLY transactions table.
    * NEVER perform any filtering on the data unless the user specifies otherwise (e.g. AVOID filtering by legal entity).
    """

    if context:
        context_augmented = f"{context_augmented}\n" + f"{context}"

    return db.ask(
        question,
        model=get_model(os.getenv("MODEL_DATABASE_AGENT")),
        context=format_text(context_augmented),
        # TODO: add output_type
    )

summarize_agent = Agent(
    model=get_model(os.getenv("MODEL_ROOT_AGENT")),
    instructions=format_text("""
    Summarize a chat message history that captures all relevant context from prior messages to support for follow-up interactions.
    
    The summary should capture:
    - Only related conversation threads.
    - Last user's intent or question.
    - Any details of previous requests if relevant (e.g. column names, dates ranges aggregations).
    - Relevant clarifications or assumptions.
    - Provide a clear next step.
    
    * If no coherent thread exists, return a minimal or empty summary. Output should be concise, clear, and suitable as input for another tool.
    * If two or more exchanges don’t appear to follow the same topic or build on each other, treat them as unrelated.
    """),
)

# #@agent.tool_plane
# async def summarize_chat_messages(messages: list[ModelMessage]):
#     """Summarize the history of messages and return relevant context for follow up interactions. 
#     Expected input is the agent's history of messages."""
    
#     if len(messages) > 5:
#         messages = messages[-5:]

#     summary = summarize_agent.run(message_history=messages)
#     return summary.new_messages() 


# if __name__ == "__main__":
#     while True:
#         user_input = input("🧑 You: ").strip()
#         if user_input.lower() in ("exit", "quit"):
#             print("👋 Goodbye!")
#             break
#         print(db.ask(user_input, model=get_model(os.getenv("MODEL_DATABASE_AGENT"))))
