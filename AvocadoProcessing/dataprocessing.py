import pandas as pd
import matplotlib.pyplot as mtp

data = pd.read_csv("avocado.csv")
data["Date"] = pd.to_datetime(data["Date"])
data = data.set_index("Date")
data = data.sort_values(by=["Date", "region", "type"])
organic = data[data["type"] == "organic"]
conventional = data[data["type"] == "conventional"]
regions = conventional["region"].unique()[0:16]
graph_df = pd.DataFrame()

for region in regions:
    region_df = conventional.copy()[conventional['region'] == region]
    region_df[f"{region}_price25ma"] = region_df["AveragePrice"].rolling(25).mean()

    if graph_df.empty:
        graph_df = region_df[[f"{region}_price25ma"]]  # note the double square brackets! (so df rather than series)
    else:
        graph_df = graph_df.join(region_df[f"{region}_price25ma"])

graph_df.plot(figsize=(8, 5), legend=False)
mtp.show()