import pandas as pd

# Step 1 : Extract - Read CSV
df = pd.read_csv("students.csv")

# Step 2: Transform - Clean and calculate
df.dropna(inplace=True) #remove missing rows
df["Marks"]=df["Marks"].astype(int)
df["Result"]=df["Marks"].apply(lambda x: "Pass" if x > 50 else "Fail")

# Step 3 : Load - Save transformed data
df.to_csv("cleaned_students.csv",index=False)

print("Data pipeline completed. Cleaned data saved to cleaned_students.csv")
