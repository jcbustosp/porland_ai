import os
import sys
import json
import dotenv
import textwrap
import datetime
import logfire

from agent import trino_db, get_model, format_text, agent
from prompts import DATABASE_AGENT_CONTEXT

dotenv.load_dotenv(override=True)

logfire.configure()
logfire.instrument_pydantic_ai()

QUESTIONS = {
    "taster": ["Does the monthly total order GTV of the top 25 franchisees show signs of plateauing (i.e., flattening or slowing growth) during the six months preceding September 2023 ?",
               "For the six months before September 2023, what were the quartile values of monthly total order GTV values among the top 25 franchisees each month?",# Ranges between 60K€-120K€, average 80K€
               "How many distinct franchisees had a total monthly order GTV below €20,000 from November 2023 to April 2024?",  # 55 franchises
               "Among the franchisees that churned (had no orders for 42 consecutive days) before June 2024, how many never reached a monthly total order GTV level above €20,000 at any time before churn?",  # Out of 81 churned 58 were small
               "What factors contributed to the decline in the total order GTV level during March 2025 compared with the level observed in February 2025? Analyze order activity of franchisees by country.", # Significant franchisees closed during March 25 in France (Ramadan month)
               # Overlay GTV trends with consumer confidence data (especially for the 18–30-year-old demographic) over time. Is there a statistically significant correlation between declining consumer confidence and the recent slowdown in GTV?"
    ],
    "patient21": ["What are the main drivers behind the high daily liquidity outflows observed during the last two days of June 2025? Look at large-impact negative transactions to explain the outflows.",
                  "What is the average variation in end-of-month total liquidity balances during the six-month period before March 2025 ?",
                  "What is the change in the trend of transaction outflows from March to May 2025 compared to December 2024 to February 2025 for the client headquarters accounts (i.e., the 'patient21_se' legal entity)?"],
}

def indent(text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)

def format_results_to_md(data_dict: dict, title: str):
    text = f"# {title}\n\n"
    for header, data in data_dict.items():
        text += f"## {header}\n\n### {os.getenv('CLIENT_NAME')}\n\n"
        if type(data) == dict:
            for k, v in data.items():
                text += f"- {k}\n\n   Answer:\n\n"
                text += f"{indent(v, 6)}\n\n"
        else: # This case should not happen.
            pass
    return text

def run_questions(use_context: bool = False, use_agent: bool = False):
    answers = {}

    for i, question in enumerate(QUESTIONS[os.getenv("CLIENT_NAME")]):
        print(f"Processing question number {i+1} ...")
        try:
            if use_agent:
                output = agent.run_sync(question)
                output = output.output
            else:
                if use_context:
                    output = trino_db.ask(question,
                                model=get_model(os.getenv("MODEL_DATABASE_AGENT")),
                                context=format_text(DATABASE_AGENT_CONTEXT.format(CLIENT_NAME=os.getenv("CLIENT_NAME"),
                                                                                CURRENT_DATE=datetime.date.today()))
                            )
                else:
                    output = trino_db.ask(question,
                                model=get_model(os.getenv("MODEL_DATABASE_AGENT"))
                            )
        except RuntimeError:
            output = "Unexpected model behavior: Received empty model response"
        
        answers[question] = output
    
    return answers

if __name__ == "__main__":

    evaluation_date  =  sys.argv[1]
    run_type  =  int(sys.argv[2])

    output_path = f"evaluation/{evaluation_date}"
    file = f"{os.getenv('CLIENT_NAME')}_evaluation_results_{evaluation_date}"
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output = {}
    if run_type == 1:
        print("****** Querying without Context:")
        file = file+"_wo_context"
        results_wo_context = run_questions()
        output["Querying without Context"] = results_wo_context
    elif run_type == 2:
        print("****** Querying with Context:")
        file = file+"_w_context"
        results_w_context = run_questions(use_context=True)
        output["Querying with Context"] = results_w_context    
    elif run_type == 3:
        print("****** Querying with Agent + Context:")
        file = file+"_w_agent_context"
        results_w_agent_context = run_questions(use_agent=True)
        output["Querying with Agent + Context"] = results_w_agent_context    
    else:
        raise ValueError("Please use 1, 2, or 3")
    
    with open(f"{output_path}/{file}.json", "w") as fp:
        json.dump(output, fp)

    output_md = format_results_to_md(output, "Evaluation Results")

    with open(f"{output_path}/{file}.md", "w") as writer:
            writer.writelines(output_md)
