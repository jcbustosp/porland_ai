import os
import datetime
from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.models import ModelSettings
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from database import trino_db
from prompts import (
    ROOT_AGENT_INSTRUCTION_PROMPT,
    SUMMARIZER_AGENT_INSTRUCTION_PROMPT,
    DATABASE_AGENT_CONTEXT,
)

load_dotenv(override=True)

def format_text(text: str):
    return "\n".join(line.strip() for line in text.splitlines()).strip()

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

    summary = await summarizer_agent.run(message_history=messages)
    return summary.new_messages()


summarizer_agent = Agent(
    model=get_model(os.getenv("MODEL_SUMMARIZER_AGENT")),
    instructions=format_text(SUMMARIZER_AGENT_INSTRUCTION_PROMPT),
)

agent = Agent(
    model=get_model(os.getenv("MODEL_ROOT_AGENT")),
    system_prompt=format_text(
        ROOT_AGENT_INSTRUCTION_PROMPT.format(
            CLIENT_NAME=os.getenv("CLIENT_NAME"), 
            CURRENT_DATE=datetime.date.today()
        )
    ),
    history_processors=[keep_recent_messages],
    model_settings=ModelSettings(
        temperature=0.0,
    ),
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

    context_augmented = DATABASE_AGENT_CONTEXT.format(
        CLIENT_NAME=os.getenv("CLIENT_NAME"), CURRENT_DATE=datetime.date.today()
    )

    if context:
        context_augmented = f"{context_augmented}\n" + f"{context}"

    # TODO: Add output_type
    return trino_db.ask(
        question,
        model=get_model(os.getenv("MODEL_DATABASE_AGENT")),
        context=format_text(context_augmented),
    )


# #@agent.tool_plane
# async def summarize_chat_messages(messages: list[ModelMessage]):
#     """Summarize the history of messages and return relevant context for follow up interactions.
#     Expected input is the agent's history of messages."""

#     if len(messages) > 5:
#         messages = messages[-5:]

#     summary = summarize_agent.run(message_history=messages)
#     return summary.new_messages()
