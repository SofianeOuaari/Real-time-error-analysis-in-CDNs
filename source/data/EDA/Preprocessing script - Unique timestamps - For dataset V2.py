#Pre-processing script to get unique timestamps
import pandas as pd
import datetime

if __name__ == "__main__":
  df = pd.read_csv("../CDN Client Error.csv")
  df['timestamp'] =  pd.to_datetime(df['timestamp'], format='%m/%d/%Y %H:%M')
  df.sort_values(by=['timestamp'], inplace=True)
  df.reset_index(drop=True, inplace=True)
  previous = datetime.datetime(1, 1, 1, 0, 0)
  for idx, col in enumerate(df['timestamp']):
    if(col<=previous):
        df['timestamp'][idx]=previous+datetime.timedelta(seconds=1)
    previous=df['timestamp'][idx]

  if(len(df['timestamp'].value_counts())==df.shape[0]):
    df.to_csv("../CDN Client Error.csv", index=False)
    print("Task done")
  else:
    print(df['timestamp'].value_counts())
    print(df.shape[0])
    print("Task failed")
