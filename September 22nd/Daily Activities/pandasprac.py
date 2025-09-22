import pandas as pd

data = {
    "names" : ["Aryan", "Bafnaa", "Chirag"],
    "ages" : [20, 30, 40],
    "married": [True, False, True],
    "Course" : ["AI", "ML", "DS"]
}

df = pd.DataFrame(data)
print(df)
