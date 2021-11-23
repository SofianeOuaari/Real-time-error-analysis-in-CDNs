import pandas as pd 
#from sklearn.model_selection import train_test_split 





df=pd.read_csv("./data/CDN Client Error.csv",sep=",")
'''df=df[["timestamp","channel_id","host_id","content_type","protocol","content_id","geo_location","user_id"]]

print(df.head())

df.to_csv("./data/CDN Client Error.csv",index=False)'''
'''df_train=df.iloc[:int(len(df)*0.75)]
df_test=df.iloc[int(len(df)*0.75):]'''
df_train_cdn=df.iloc[:50000]
df_test_cdn=df.iloc[50000:70000]

'''df_train.to_csv("./data/train_cdn.csv",index=False)
df_test.to_csv("./data/test_cdn.csv",index=False)'''

df_train_cdn=df_train_cdn.to_csv("./data/train_cdn.csv",index=False)
df_test_cdn=df_test_cdn.to_csv("./data/test_cdn.csv",index=False)
