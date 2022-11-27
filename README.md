DATA ENGINEERING PROJECT -  Cost Lens for shared services cost show back

(END to END flow performing ELT to calculate show back costs for several shared services)


An ETL Data pipeline which processes the shared services (Public or Private (On Prem) Cloud services) Spend/Usage Data

Large, shared services in any organization is growing and expensive and their allocation, calculation has different methods (Even/Split/Partition allocations etc.) Allocating and calculating the spend v/s usage costs metric will provide a great transparency of how much individual teams within an organization or outside of the organization have been spent v/s how much actual their usage is.
Thus, we can hold teams accountable by sharing the cost show back and after proving and providing the transparency we can start charging back the teams who have been used the greatest number of metric units and what service is highly used across which product teams questions can be answered.

Tools Used : Airflow, AWS Lambda Functions, S3, Redshift for warehousing, Tableau for visualization

![image](https://user-images.githubusercontent.com/32167301/204116916-e62ff43f-c986-4d47-ad94-573061e34ee5.png)

