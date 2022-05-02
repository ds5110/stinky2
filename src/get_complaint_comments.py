import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

complaints = pd.read_csv('smc_data.csv', encoding = 'ISO-8859-1')

def PreprocessComplaints(df):
  # Update to consistent column name
  df = df.rename(columns={'date & time': 'DATE & TIME'})
  df['DATE & TIME'] = pd.to_datetime(df['DATE & TIME'])

  df = df[df['DATE & TIME'].notnull()]
  df = df[df['additional_comments'].notna()]

  lengths = df['additional_comments'].str.len()
  argmax = np.where(lengths > 10)[0]
  df = df.iloc[argmax]

  # Sorting the dataframe on the basis of Date & Time column as we need sorted dataframe to merge the data
  df = df.sort_values('DATE & TIME', ascending=[False])
  return df

complaints= PreprocessComplaints(complaints)
comments = complaints['additional_comments']
comments.to_csv("complaints_comments.csv", index=False)
