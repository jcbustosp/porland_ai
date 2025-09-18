# Evaluation Results

## Querying with Context

### patient21

- What are the main drivers behind the high daily liquidity outflows observed during the last two days of June 2025? Look at large-impact negative transactions to explain the outflows.

   Answer:

      I’m ready to help. Please let me know what you’d like to find out about Patient21’s data.

- What is the average variation in end-of-month total liquidity balances during the six-month period before March 2025 ?

   Answer:

      **Key Elements**

      | Period | Avg. Variation in End‑of‑Month Total Liquidity (covenant currency) |
      |--------|-------------------------------------------------------------------|
      | Six months before March 2025 (Sep 2024 – Feb 2025) | **$65,548,171.05** |

      **How the result was obtained**

      1. Queried the `portland.patient21_reference.liquidity` table for all records between 2024‑09‑01 and 2025‑02‑28.  
      2. Aggregated the `lower_bound_balance_in_covenant_currency` per month to get each month’s total liquidity.  
      3. Calculated month‑to‑month changes (current month total minus previous month total).  
      4. Took the absolute value of each change and averaged them across the five month‑to‑month intervals.  

      The final average variation is **$65,548,171.05**.

- What is the change in the trend of transaction outflows from March to May 2025 compared to December 2024 to February 2025 for the client headquarters accounts (i.e., the 'patient21_se' legal entity)?

   Answer:

      **Key result**

      - **Change in trend of transaction outflows (March‑May 2025 vs. December 2024‑February 2025)**:  
        **+ 1,010,918.40 EUR** (outflows became less negative by about 1.01 million EUR).

      **How the result was obtained**

      1. Queried the `portland.patient21_reference.saltedge_transactions` table for the headquarters legal entity **Patient21 SE**.  
      2. Summed the negative `amount` values (outflows) per month for the two periods:
         * December 2024 – February 2025  
         * March 2025 – May 2025  
      3. Calculated the average monthly outflow for each period.  
      4. Subtracted the earlier‑period average from the later‑period average, yielding a positive change of **+1,010,918.40 EUR**.  

      The calculation used the monthly totals:

      | Period | Avg. outflow (EUR) |
      |--------|--------------------|
      | Dec 2024 – Feb 2025 | –6,140,330.89 |
      | Mar 2025 – May 2025 | –5,129,412.49 |

      The positive difference indicates a trend toward lower outflows in the later period.

