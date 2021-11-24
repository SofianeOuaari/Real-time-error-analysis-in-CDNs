#Pre-processing script to get unique timestamps
#Note: the dataframe given in input must be already sorted by timestamp chronological order
import pandas as pd
import datetime

df = pd.read_csv("../CDN Client Error.csv")
df = df.reset_index()
df['timestamp'] =  pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')
previous = datetime.datetime(1, 1, 1, 0, 0)
for idx, col in enumerate(df["timestamp"]):
  if(col<=previous):
    df["timestamp"][idx]=previous+datetime.timedelta(seconds=1) #Adding 1 millisecond if the value already exists
  previous=df["timestamp"][idx]

if(len(df['timestamp'].value_counts())==df.shape[0]):
  df.to_csv("../CDN Client Error.csv", index=False)
  print("Task done")
else:
  print("Task failed")
exit()
