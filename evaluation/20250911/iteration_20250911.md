# Portland AI

The objective is to define a system that enables users to directly query the datasets stored in Portland using natural language, and obtain relevant and correct results.

## Core functionality Evaluation

The core functionality of the system is its ability to interpret natural language input and accurately retrieve relevant data from the database.

To assess the performance of this feature for a given solution, we perform an assessment of its ability to correctly answer a list of frequently asked questions about customer data. The list of questions was derived from those commonly raised during the preparation or execution of OpCo activities.

Questions are grouped according to their query complexity and the required data. The table below serves as a guide for determining each question's difficulty level.

| Difficulty Level| Characteristics |
| :--- | :--- |
| **Easy** | Answering this kind of question requires a single calculation, such as adding values or computing an average. |
| **Medium** | Answering this kind of question requires more than a single calculation, such as comparing data points or ranking groups. |
| **Hard** | Answering this question requires complex calculations, such as multi-step processes, cross-referencing different datasets or integrating business knowledge. |

As a general rule, each response is scored as follows: 1.0 for a correct answer, 0.2 for a partially correct answer, and 0.0 for an incorrect response.

Currently, the difficulty level of the question **does not** influence the final score.

### List of Questions

Some questions apply only to DRCF clients, as they involve non-liquidity data from a shared dataset used across all clients.

#### Easy

- What is the current total liquidity level ?
- What is the current total liquidity level of pledged accounts ?
- What is the current sales/orders/GTV level ?

#### Medium

- What it is the total number of customers who placed an order this month ?

- What is the difference between the current liquidity position and the liquidity position at the end of last month ?

- What are the top 3 transactions that had the biggest impact on the liquidity over the past week?

- Who are the top 3 clients contributing the most to revenue/sales/GTV level this month ?

#### Hard

- What is the year-over-year percentage change in average liquidity level for the current month compared to the same month last year ?

- Is the current total liquidity level close to the facility liquidity covenant? The facility covenant is equal to < DEFINITION >

## Initial Iteration

An initial iteration on the Portland AI system's core functionality to validate its feasibility was conducted. In this iteration, the usage of off-the-shelf open-source tools was prioritized to streamline implementation and testing.

During this iteration, we evaluated the following approaches. All the evaluated approaches leverage on open-source LLMs and the `toolfront` package to perform natural language queries on the Portland database.

Note: Behind the scenes, an AI agent powers toolfront. This agent inspects the database, translates user questions into queries, and then uses that data to provide an accurate answer.

- Direct query: We query the database without providing any specific context.

- Contextual Query: We provide some context before querying the database.

- Agent-Based System: We implement an agent is implemented to manage user queries through a tool that query Portland database via toolfront. Context is provided to both the agent and the tool.

To ensure our evaluations were comparable, we used the same LLM (`gpt-oss:20b`) for all tests, and to reduce the variability and randomness of generated responses, temperature parameter was set as 0.Additionally, the context provided to the toolfront query was identical across the second and third approaches.

### Results

The table below sums up the iteration results over `kebony` and `taster` datasets.

| Question                                                                                          | Difficulty | Client  | No context | Context | Agent + Context |
|---------------------------------------------------------------------------------------------------|------------|---------|------------|---------|-----------------|
| What is the current total liquidity level?                                                        | Easy       | Kebony  | 0          | 1       | 1               |
|                                                                                                   |            | Taster  | 0          | 1       |               |
| What is the current total liquidity level of pledged accounts?                                    | Easy       | Kebony  | 0          | 1       | 1               |
|                                                                                                   |            | Taster  | 1          | 1       |                |
| What is the current sales/orders/GTV level?                                                       | Easy       | Kebony  | N/A        | N/A     | N/A             |
|                                                                                                   |            | Taster  | 0          | 1       |                |
| What is the total number of customers who placed an order this month?                             | Medium     | Kebony  | N/A        | N/A     | N/A             |
|                                                                                                   |            | Taster  | 0          | 1       |                |
| What is the difference between the current liquidity position and the liquidity position at the end of last month? | Medium     | Kebony  | 0          | 1       | 1               |
|                                                                                                   |            | Taster  | 0          | 1       |                |
| What are the top 3 transactions that had the biggest impact on the liquidity over the past week?  | Medium     | Kebony  | 0          | 0     | 0.2               |
|                                                                                                   |            | Taster  | 0          | 0.2     |                |
| Who are the top 3 clients contributing the most to revenue/sales/GTV level this month?            | Medium     | Kebony  | N/A        | N/A     | N/A             |
|                                                                                                   |            | Taster  | 0          | 1       |                |
| What is the year-over-year percentage change in average liquidity level for the current month compared to the same month last year? | Hard       | Kebony  | 0          | 1       | 0               |
|                                                                                                   |            | Taster  | 1          | 1       |                |
| Is the current total liquidity level close to the facility liquidity covenant? The facility covenant is equal to < DEFINITION > | Hard       | Kebony  | 0          | 1       | 1               |
|                                                                                                   |            | Taster  | 1          | 1       |                |

All results are available [here](/Users/juan-camilo.bustospelaez/projects-perso/portland-analyst/src/toolfront/results/initial_iteration_results.md).

### Key insights

- The quality of the results is directly tied to the quality of its input. A correct definition of system's instructions and context actively shape the AI’s responses, enabling to obtain more accurate, efficient and reliable answers. Context acts as a guide, enabling you to fine-tune the AI's behavior by setting defaults, steering it to the right data, and clarifying relationships between datasets.

- An agent-based system acts as a powerful layer on top of basic tools. By managing conversational memory and multi-turn interactions, an agent allows a system to handle more complex, multi-step user queries, going far beyond a simple single-shot lookup.

- AI based system development moves quickly, with many tools but no standard way to measure success. You need to set clear goals, choose what to track, and recognize that building a system is one task, while proving it works is another.

### Next steps

- Run of a new evaluation round enriching the context (e.g. tables descriptions, client's activity basic knowledge).
- Continue working on a first ready-to-use conversational prototype.
