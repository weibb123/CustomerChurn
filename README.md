# CustomerChurn

## Table of Contents

  - [Business problem](#business-problem)
  - [Data source](#data-source)
  - [Methods](#methods)
  - [Tech Stack](#tech-stack)
  - [Lessons learned and recommendation](#lessons-learned-and-recommendation)
  - [Limitation and what can be improved](#limitation-and-what-can-be-improved)
  - [Evaluation](#evaluation)
  - [Reference](#reference)

    ## Business problem
    Attracting new customers are always an expensive approach such as ads or sales. What am I interested in is to figure out a way to retain customers or understand why customers leave. Next, I want to build a machine learning model that classify customers who churn or not churn.

    ## Data source
    Thanks to Github: nicknochnack, for providing this dataset to help building this project.\
    
    Columns:\
    <b>State_code:</b> Abbreviate letter of each State, MA, NH, MN
    
    <b>tenure:</b> The length of time customer remains as customer 
    
    <b>Promotions_offered:</b> categorical data yes or no, whether promotion is offered
    
    <b>remaining_term:</b> remaining term of subscription end
    
    <b>last_nps_rating:</b> net promoter score based on market metric, the likelihood of recommending products, services, company
    
    <b>contract_length:</b> The length of the contract between customers and the company
    
    <b>area_code:</b> Area code. area_code_510 = East Bay of San Francisco, area_code_508 = San Jose, area_code_415 = Greater area of San Francisco
    
    <b>internation_plan:</b> Categorical data yes or no, whether customer has international plan
    
    <b>voice_plan:</b> Categorical data yes or no, whether customer has voice plan
    
    <b>number_vmail_message:</b> numerical data, number of voice messages customer send, showing how often customer sends voicemessages.
    
    <b>voice_plan:</b> Categorical data yes or no, whether customer has voice plan
    
    <b>number customer calls:</b> Number of times customers need to contact customer assistant
    
    <b>Prediction:</b> binary categorical data, churn or not churn
    
    
    ## Methods
      1. Split data into train and testsets: Splitting dataset apart at early stage prevent data bias to avoid making assumptions about whole dataset.
      2. Data preprocessing such as filling Null values with "missing" on categorical column, Imputator: average on numerical column
      3. feature engineering: create unhappy customers column based on low remaining term + low net promotor rating
      4. feature engineering: notice skew data distribution, perform log transform to approximate normal distribution
      5. feature engineering: create new feature to decorrelate columns, ML model performs better with decorrelated features
      6. Onehot encoding to encode categorical data
      7. Notice that dataset is unbalanced, utilized scikitlearn to resample in order to achieve balanced dataset
      8. ML pipeline: Search for hyperparameters, tested RFclassifier, XGBoost, GBclassifier, sgdclassifier, ridgeclassifier

    ## Tech Stack
    - Streamlit
    - Python
    - Scikit Learn
    - Pandas/Seaborn/Matplotlib
    
    ## Lessons learned and recommendation
    Key lesson: Customers who are likely to churn are those who have less remaining terms. Reason: subscriptions cost, not satisfying with product, altnerative good deals option\
      - Look into customers who gave bad rating + remaining term is short, perhaps better off offer them promotions
      ![image](https://github.com/weibb123/CustomerChurn/assets/84426364/5cbfc9b4-2cbd-4bb7-a7a8-d357c157ddb0)

    
    ## what can be improved
      Survey to ask about what customers are feeling. Use the survey as an aid to guide the data analysis.\

      Putting customers first, seeing what features customers love or hate.
    
    
    ## Evaluation

      Metric used: recall_score, precision_score
      ![image](https://github.com/weibb123/CustomerChurn/assets/84426364/a335c59d-88d4-4764-9c2e-896e88b38c36)

      In this case, XGBoost gave the highest recall_score and precision_score. This model will be used when deploying the classification web app.
    
