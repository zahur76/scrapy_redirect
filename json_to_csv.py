import pandas as pd

df = pd.read_json("./output/bizify_A.json")

df.fillna("Nan", inplace=True)

df.to_csv("./output/bizify_A.csv", index=False)