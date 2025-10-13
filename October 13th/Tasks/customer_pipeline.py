import pandas as pd
from datetime import datetime

def run_pipeline():
    df=pd.read_csv("customers.csv")
    df['AgeGroup']=df["Age"].apply(lambda x: "Young" if x < 30 else "Adult" if 30<= x <50 else "Senior")


    customer_less_20_df = df[df["Age"] < 20]
    print(customer_less_20_df)


    df.to_csv("customer_report.csv",index=False)


if __name__=="__main__":
    run_pipeline()
