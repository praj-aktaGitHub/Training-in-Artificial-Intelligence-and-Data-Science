import pandas as pd

data = {
    "names" : ["Aryan", "Bafnaa", "Chirag"],
    "ages" : [20, 30, 40],
    "married": [True, False, True],
    "Course" : ["AI", "ML", "DS"]
}

df = pd.DataFrame(data)


print(df["names"])
print(df[["names", "married"]])
print(df.iloc[0])
print(df.loc[2, "names"])

adult = df[df["ages"]] > 18
print(adult)