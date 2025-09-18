# Evaluation Results

## Querying without Context

### taster

- Does the monthly total order GTV of the top 25 franchisees show signs of plateauing (i.e., flattening or slowing growth) during the six months preceding September 2023 ?

   Answer:

      The dataset contains **11,480 rows** in total.

- For the six months before September 2023, what were the quartile values of monthly total order GTV values among the top 25 franchisees each month?

   Answer:

      **Quartile values of monthly total order GTV (top 25 franchisees)**  
      *(six months preceding September 2023 – March – August 2023)*  

      | Month (2023) | Q1 (25th %) | Median (50th %) | Q3 (75th %) |
      |--------------|-------------|-----------------|-------------|
      | 2023‑03‑01   | 97 882.25   | 107 988.16      | 115 571.94  |
      | 2023‑04‑01   | 92 849.22   | 102 684.07      | 112 600.60  |
      | 2023‑05‑01   | 91 257.28   | 100 938.82      | 120 245.77  |
      | 2023‑06‑01   | 89 142.47   | 96 220.13       | 119 222.24  |
      | 2023‑07‑01   | 85 201.96   | 97 006.48       | 117 160.75  |
      | 2023‑08‑01   | 82 283.80   | 102 670.55      | 112 565.23  |

      These values were calculated by:

      1. Summing the `gtv` for each franchisee per month (March – August 2023).  
      2. Selecting the top 25 franchisees by monthly GTV.  
      3. Computing the 25th, 50th, and 75th percentiles of those monthly totals.  

      The data come directly from the `portland.taster_reference.orders` table.

- How many distinct franchisees had a total monthly order GTV below €20,000 from November 2023 to April 2024?

   Answer:

      The query returned **117** distinct franchisees whose total monthly order GTV was below €20,000 for at least one month between **November 2023** and **April 2024**.

- Among the franchisees that churned (had no orders for 42 consecutive days) before June 2024, how many never reached a monthly total order GTV level above €20,000 at any time before churn?

   Answer:

      Unexpected model behavior: Received empty model response

- What factors contributed to the decline in the total order GTV level during March 2025 compared with the level observed in February 2025? Analyze order activity of franchisees by country.

   Answer:

      I’m ready to help. What would you like to know from the data?

