# cortex-and-q-for-business

The materials here show customers how connect Q for Business from AWS with Snowflake Cortex. 

Requirements are:
1. Snowflake account with Cortex Search and/or Analyst
2. AWS account with Q for Business
3. Knowledge of Snowflake and some familiarity with Cortex
4. Knowledge and some experience with Lambda funcitons in AWS

Steps to building this integration:
1. Create Cortex Search service in Snowflake
2. Develop and deploy Lambda Function with API Gateway that handles auth and connects to Snowflake Cortex Service
3. Connect Q to API Gateway and Lambda

## 1. Create Cortex Search Service
Users can set up whatever Search or Analyst service they would like, however the API Schema and the Lambda app.py code here support the AirBnB use cases detailed in the documentation here: 
https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/overview-tutorials

## 2.Lambda Function
The easy method here is to simply use the app.py file provided and authenticate with username and password. Obviously this would be a strict demo set up but it will show you what is possible. You can store a Snowflake key in AWS Secrets Manager and use the app_keypair.py script in your Lambda function. In that .py you will have to update the name of the secrets manager and the Snowflake details. Additionally, you will have to manage permssions and access to Secrets Manager. There can also be some nuance with the API Gateway so please work with your AWS team to make sure the APIGW is configured appropriately. The requirements.txt file should also be included as a layer in your Lambda function.

## 3. Connect Q to API Gateway and Lambda
Create a plugin in Q for Business via the No Auth option. use the API Schema file here to define the call to the APIGW and Lambda function. Update the API url and also the schema (if you are not using the airbnb use case). Once done you can test the integration to get responses from Cortex from Q for Business!

Much thanks to Frank D from AWS and James S from Snowflake for sooo much help on this. Also, be on the lookout for more material on the more integrated method by the beginning of 2025!
