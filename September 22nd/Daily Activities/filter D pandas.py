import pandas as pd
import numpy as np

data = {
    "names" : ["Aryan", "Bafnaa", "Chirag", "Amaal"],
    "ages" : [17, 32, 40, 16],
    "married": [False, False, True, False],
    "Job Role" : ['AI intern', "ML", "DS", 'AI intern']
}

df = pd.DataFrame(data)

adult = df[df["ages"] > 18]
print(adult)

df["Demographics"] = np.where(df["ages"] >= 18, "Adults", "Young Adults")
print(df)

df.loc[df["names"] == "Chirag", "Job Role"] = 'Senior DS'
print(df)