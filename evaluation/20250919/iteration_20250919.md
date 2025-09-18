# Portland AI

The objective is to define a system that enables users to directly query datasets stored in Portland using natural language and receive relevant and accurate results. The main goal of this development is to reduce the time and workload required for ad-hoc analyses.

## Core functionality Evaluation

The core functionality of the system is its ability to interpret natural language input and accurately retrieve relevant data from the database.

To assess the performance of this feature for a given solution, we perform an assessment of its ability to correctly answer a list of frequently asked questions about customer data. The list of questions was derived from those raised during the preparation or execution of OpCo activities.

As a general rule, each response is scored as follows: 1.0 for a correct answer, 0.2 for a partially correct answer, and 0.0 for an incorrect response.

### List of Questions

The questions are the following:

#### Taster

- Does the monthly total order GTV of the top 25 franchisees show signs of plateauing (i.e., flattening or slowing growth) during the six months preceding September 2023 ?

- For the six months before September 2023, what were the quartile values of monthly total order GTV values among the top 25 franchisees each month ?

- How many franchisees had a total monthly order GTV below €20,000 from November 2023 to April 2024 ?

- Among the franchisees that churned (had no orders for 42 consecutive days) before June 2024, how many never reached a monthly total order GTV level above €20,000 at any time before churn ?

- What factors contributed to the decline in the total order GTV level during March 2025? Analyze order activity per country and per franchisee.

#### Patient21

- What are the main drivers behind the high daily liquidity outflows observed during June 2025? List the large-impact transactions that explain significant outflows.

- What is the average monthly change in total cash position, based on end-of-month total liquidity balances, during the 6 months before March 2025 ?

- What is the change in the trend of transaction outflows from March to May 2025 compared to December 2024 to February 2025 for the client headquarters accounts (i.e., the 'patient21_se' legal entity) ?

## Assessment

An assessment was carried out to evaluate the effectiveness and limitations of an off-the-shelf open-source solution in fulfilling the core functional requirements of the Portland AI system.

The assessed solution is the `toolfront` package, which offers native integration with the Portland database and leverages LLMs to translate user natural language questions into queries, generating answers based on the query outputs."

As part of the assessment we compared the following approaches:

- Direct Querying: We query the database without providing any specific context.

- Contextual Querying: We provide some context before querying the database.

- Agent Top-Layer Contextual Querying: We implement an AI agent to handle user queries through a tool that call the `toolfront` package. Context is provided to both the agent and the tool.

To ensure our evaluations were comparable, we used the same LLM (`gpt-oss:20b`) for all tests, and to reduce the variability and randomness of generated responses, temperature parameter was set as 0.Additionally, the context provided to the `toolfront` query was identical across the second and third approaches.

### Results

The table below sums up the iteration results over `taster` and `patient21`.

All results are available [here](/Users/juan-camilo.bustospelaez/projects-perso/portland-analyst/src/portland_ai/evaluation/20250919/evaluation_results_20250919.md).

| Question                                                                                                                                                                                                                     | Client     | No context | Context | Agent + Context |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|------------|---------|-----------------|
| Does the monthly total order GTV of the top 25 franchisees show signs of plateauing (i.e., flattening or slowing growth) during the six months preceding September 2023?                                                   | Taster     | 0          | 0       | 0               |
| For the six months before September 2023, what were the quartile values of monthly total order GTV values among the top 25 franchisees each month?                                                                         | Taster     | 1          | 1       | 1               |
| How many distinct franchisees had a total monthly order GTV below €20,000 from November 2023 to April 2024?                                                                                                                  | Taster     | 1          | 1       | 0               |
| Among the franchisees that churned (had no orders for 42 consecutive days) before June 2024, how many never reached a monthly total order GTV level above €20,000 at any time before churn?                                | Taster     | 0          | 0       | 0               |
| What factors contributed to the decline in the total order GTV level during March 2025 compared with the level observed in February 2025? Analyze order activity of franchisees by country.                                | Taster     | 0          | 0       | 1              |
| What are the main drivers behind the high daily liquidity outflows observed during the last two days of June 2025? Look at large-impact negative transactions to explain the outflows.                                     | Patient21  | 0          | 0       | 1               |
| What is the average variation in end-of-month total liquidity balances during the six-month period before March 2025?                                                                                                       | Patient21  | 0          | 0       | 1               |
| What is the change in the trend of transaction outflows from March to May 2025 compared to December 2024 to February 2025 for the client headquarters accounts (i.e., the ‘patient21_se’ legal entity)?                    | Patient21  | 0          | 1       | 1               |

### Key insights

- The quality of the results is directly tied to the quality of its input. A correct definition of system's instructions and context actively shape the AI’s responses, enabling to obtain more accurate, efficient and reliable answers. Context acts as a guide, enabling you to fine-tune the AI's behavior by setting defaults, steering it to the right data, and clarifying relationships between datasets.
        Semantics - knowledge of what each field, table or entity means
        Lineage - how data flows and where dependencies exist
        Usage patterns - how teams consume and interpret data
        Constraints & rules - what mus always hold true

- An agent-based system acts as a powerful layer on top of basic tools. By managing conversational memory and multi-turn interactions, an agent allows a system to handle more complex, multi-step user queries, going far beyond a simple single-shot lookup.

- AI based system development moves quickly, with many tools but no standard way to measure success. You need to set clear goals, choose what to track, and recognize that building a system is one task, while proving it works is another.

## Next Steps

- Evaluate whether there is an actual need (an actual problem) in ad-hoc data analyses to justify further time investment.

- Conduct the same assessment using a larger model and compare the results (depending on the outcome of the previous evaluation).
