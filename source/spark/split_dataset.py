import pandas as pd 
#from sklearn.model_selection import train_test_split 





df=pd.read_csv("./data/alldata_skab.csv",sep=",")
df_train=df.iloc[:int(len(df)*0.75)]
df_test=df.iloc[int(len(df)*0.75):]


df_train.to_csv("./data/train.csv",index=False)
df_test.to_csv("./data/test.csv",index=False)
