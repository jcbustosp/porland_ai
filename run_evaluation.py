import os
import json
import dotenv
import datetime
import logfire

from src.portland_ai.agent import trino_db, get_model, format_text, agent
from prompts import DATABASE_AGENT_CONTEXT

dotenv.load_dotenv(override=True)

logfire.configure()
logfire.instrument_pydantic_ai()


QUESTIONS = {
    "kebony":[
        "What is the current total liquidity level ?",
        "What is the current total liquidity level of pledged accounts ?",
        "What is the difference between the current liquidity position and the liquidity position at the end of last month ?",
        "What are the top 3 transactions that had the biggest impact on the liquidity over the past week ?",
        "What is the year-over-year percentage change in average liquidity level for the current month compared to the same month last year ?",
        "Is the current total liquidity level close to the facility liquidity covenant? The facility covenant is equal to 20% of total facility outstanding",
        ],

    "taster":[
        "What is the current total liquidity level ?",
        "What is the current total liquidity level of pledged accounts ?",
        "What is the total GTV level of the current month ?",
        "What it is the total number of customers who placed an order this month ?",
        "What is the difference between the current liquidity position and the liquidity position at the end of last month ?",
        "What are the top 3 transactions that had the biggest impact on the liquidity over the past week ?",
        "Who are the top 3 concepts contributing the most to GTV level this month ?",
        "What is the year-over-year percentage change in average liquidity level for the current month compared to the same month last year ?",
        "Is the current total liquidity level close to the facility liquidity covenant? The facility covenant is equal to 1M €",
    ]
}

if __name__ == "__main__":
    answers = {}
    for i, question in enumerate(QUESTIONS[os.getenv("CLIENT_NAME")]):
        print(f"Question {i+1}...")

        res = trino_db.ask(question,
                    model=get_model(os.getenv("MODEL_DATABASE_AGENT")),
                    #context=format_text(CONTEXT.format(CLIENT_NAME=os.getenv("CLIENT_NAME"), CURRENT_DATE=datetime.date.today()))
                )
        
        #res = agent.run_sync(question)
        answers[i+1] = res#.output

    with open(f"evaluation/{os.getenv('CLIENT_NAME')}_agent_with_context.json", "w") as fp:
        json.dump(answers, fp)
