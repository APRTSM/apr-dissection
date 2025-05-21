import pandas as pd 

df = pd.read_pickle("EXP7-sourcerercc.pkl")
df.to_html("output.html")
