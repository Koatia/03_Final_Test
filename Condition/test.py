import pandas as pd

data_path = r"ab_stats.csv"
data = pd.read_csv(data_path)

print("Размеры датасета", data.shape)
print(data.head(6))