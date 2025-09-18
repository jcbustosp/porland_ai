# Evaluation Results

## Querying with Context

### taster

- Does the monthly total order GTV of the top 25 franchisees show signs of plateauing (i.e., flattening or slowing growth) during the six months preceding September 2023 ?

   Answer:

      Here’s a straightforward SQL statement that will create the table you described:

      ```sql
      CREATE TABLE people (
          id   INT PRIMARY KEY,
          name VARCHAR(255),
          age  INT
      );
      ```

      - **`id`** is an integer and the primary key of the table.  
      - **`name`** is a variable‑length string (you can adjust the length if needed).  
      - **`age`** is an integer.

      Just run this statement in your database client, and the `people` table will be ready for use.

- For the six months before September 2023, what were the quartile values of monthly total order GTV values among the top 25 franchisees each month?

   Answer:

      **Quartile values of monthly total order GTV (top 25 franchisees)**  

      | Month (2023‑MM‑01) | Q1 (25th %) | Median (50th %) | Q3 (75th %) |
      |--------------------|-------------|-----------------|-------------|
      | 2023‑03‑01 | 102,157.40 | 109,148.90 | 115,571.94 |
      | 2023‑04‑01 | 94,174.51 | 102,710.83 | 112,600.60 |
      | 2023‑05‑01 | 93,903.47 | 101,105.28 | 120,245.77 |
      | 2023‑06‑01 | 91,151.02 | 98,220.50 | 119,222.24 |
      | 2023‑07‑01 | 88,064.67 | 98,543.95 | 117,160.75 |
      | 2023‑08‑01 | 85,357.51 | 102,670.55 | 105,208.85 |

      ---

      ### How the results were obtained  

      1. **Data source** – `portland.taster_reference.orders` table (contains `date`, `franchisee_id`, `gtv`, etc.).  
      2. **Time window** – March 1 2023 to August 31 2023 (the six months preceding September 2023).  
      3. **Monthly aggregation** – summed `gtv` per `franchisee_id` for each month.  
      4. **Top‑25 selection** – for each month, ranked franchisees by monthly GTV and kept the top 25 (`ROW_NUMBER() ≤ 25`).  
      5. **Quartile calculation** – used `percentile_cont` (continuous percentile) on the `total_gtv` of the top‑25 set for each month to get Q1, median, and Q3.  
      6. **Result** – returned one row per month with the three quartile values.

- How many distinct franchisees had a total monthly order GTV below €20,000 from November 2023 to April 2024?

   Answer:

      **Answer**

      - **Number of distinct franchisees with total monthly GTV < €20,000 (Nov 2023 – Apr 2024):** **117**

      **How the result was obtained**

      1. Queried the `portland.taster_reference.orders` table.  
      2. Filtered rows to the date range 2023‑11‑01 to 2024‑04‑30.  
      3. Aggregated GTV per `franchisee_id` for each month (`DATE_TRUNC('month', date)`).  
      4. Counted distinct `franchisee_id` values where the monthly GTV sum was below 20,000.  
      5. The query returned 117 distinct franchisees.

- Among the franchisees that churned (had no orders for 42 consecutive days) before June 2024, how many never reached a monthly total order GTV level above €20,000 at any time before churn?

   Answer:

      I’m ready to help!  
      What would you like to know or analyze from the Taster data?

- What factors contributed to the decline in the total order GTV level during March 2025 compared with the level observed in February 2025? Analyze order activity of franchisees by country.

   Answer:

      I’m ready to help!  
      Could you let me know what specific information you’d like to retrieve from the **taster** database?  
      For example, you might ask for:

      - Total GTV for a particular date or franchisee  
      - Liquidity balances for a given day  
      - Order counts or revenue figures  
      - Any other metric you’re interested in

      Once I know the exact question, I’ll query the relevant tables and provide the answer.

