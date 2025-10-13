import pandas as pd
import numpy as np

def run_pipeline():
    df=pd.read_csv("inventory.csv")
    df['RestockNeeded'] = np.where(df["Quantity"] < df["ReorderLevel"], "Yes", "No")

    df['TotalValue'] = df["Quantity"] * df["PricePerUnit"]


    df.to_csv("restock_report.csv",index=False)


if __name__=="__main__":
    run_pipeline()
