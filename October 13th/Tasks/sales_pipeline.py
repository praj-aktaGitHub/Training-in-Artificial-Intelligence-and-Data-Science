from typing import final

import pandas as pd

def run_pipeline():
    customer_df=pd.read_csv("customers.csv")
    product_df = pd.read_csv("products.csv")
    orders_df=pd.read_csv("orders.csv")

    new_df = orders_df.merge(customer_df, how="outer", on="CustomerID")
    final_df = new_df.merge(product_df, how="outer", on="ProductID")
    #print(final_df)

    final_df['TotalAmount']=final_df['Quantity']*final_df['Price']
    final_df['OrderMonth']=pd.to_datetime(final_df["OrderDate"]).dt.month

    final_df['Quantity'].astype(int)
    filtered_df = final_df[(final_df['Quantity'] > 2) & ((final_df["Country"] == "India") | (final_df["Country"] == "UAE"))]
    print(filtered_df)

    category_revenue = final_df.groupby('Category')['TotalAmount'].sum().reset_index()
    segment_revenue = final_df.groupby('Segment')['TotalAmount'].sum().reset_index()

    customer_revenue = final_df.groupby('Name')['TotalAmount'].sum().reset_index()
    sorted_customers = customer_revenue.sort_values(by='TotalAmount', ascending=False)



    sorted_customers.to_csv("Sales_report.csv",index=False)
    filtered_df.to_csv("filtered_sales_report.csv", index=False)
    category_revenue.to_csv("category_revenue_report.csv", index=False)
    segment_revenue.to_csv("segment_revenue_report.csv", index=False)


if __name__=="__main__":
    run_pipeline()
