import pandas as pd

df = pd.read_csv('./output_data/smc_data.csv')

df['smell_description'] = df['smell_description'].str.lower()

for x in df['smell_description']:
    print(x)