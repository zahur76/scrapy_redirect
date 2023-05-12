import pandas as pd

df = pd.read_json("./output/travelalberta.json")

df.fillna("Nan", inplace=True)

df.to_csv("./output/travelalberta.csv", index=False)