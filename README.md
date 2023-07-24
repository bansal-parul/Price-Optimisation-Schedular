# Price-Optimisation-Schedular
Price Optimasation Algorithm, winning solution for Tractor Supply's AI Hackathon. 

The data here is provided by Hackathon. 

The steps for determining the prices for a given month are as follows:
1. Obtain a relationship between demand, price and time : Estimate an equation between Demand and Price for each  SKU at weekly level 

2. Forecast sales : Forecast Demand for each SKU at weekly level using historical Demand data using Deep Learning using Temporal Fusion Transformer.
   
3. Optimise price with respect to forecast : Find Upper and lower limits of demand at weekly level
Find Optimal Price at weekly level, given Demand-Price Equation, and bounds on Demand forecast and Price.

4. Results : Bin the Optimal Price for each SKU’s. For the consecutive weeks, where the bin price is changing, provide optimum price

Please see the TSC Pricing Optimisation.pptx for more details on the process.





