# Data Engineering Project - Cost Lens for shared services cost show back

(END to END flow performing ELT to calculate show back costs for several shared services)

An ETL Data pipeline which processes the shared services (Public or Private (On Prem) Cloud services) Spend/Usage Data

Large, shared services in any organization is growing and expensive and their allocation, calculation has different methods (Even/Split/Partition allocations etc.) Allocating and calculating the spend v/s usage costs metric will provide a great transparency of how much individual teams within an organization or outside of the organization have been spent v/s how much actual their usage is.
Thus, we can hold teams accountable by sharing the cost show back and after proving and providing the transparency we can start charging back the teams who have been used the greatest number of metric units and what service is highly used across which product teams questions can be answered.

**Tools Used** : Airflow, AWS Lambda Functions, S3, Redshift for warehousing, Tableau for visualization

<img width="1000" alt="Screen Shot 2022-10-03 at 12 11 21 AM" src="https://user-images.githubusercontent.com/32167301/204117209-19fe494d-9c8f-434b-9723-1e116f7d8c15.png">

Implemented Architecture followed to implement shared services costs showback

<img width="900" alt="image" src="https://user-images.githubusercontent.com/32167301/204126543-7c34f4c6-5eba-47a4-80e9-2844feca47c5.png">
