import matplotlib.pyplot as plt
import pandas as pd

# Load data
df = pd.read_csv("pokemon_gen1_to_6.csv")

x = df["Attack"]
y = df["Defense"]

plt.figure(figsize=(14, 10))
plt.scatter(x, y, color="blue", marker='x', label="Pokemon Data")
plt.xlabel("Pokemon Attack")
plt.ylabel("Pokemon Defense")
plt.legend()
plt.show()