import pandas as pd

df_followerList = pd.read_csv('/data/followerList.csv',names=['userid','username','name'])
df_followingList = pd.read_csv('/data/followingList.csv',names=['userid','username','name'])
# read two csv files
df_followerList_followingList= pd.merge(df_followerList,df_followingList,left_on="userid",right_on = "userid", how = "inner")
# inner join the data and index is userid

df_followerList_followingList.drop(['username_y','name_y'],axis=1, inplace=True)
df_followerList_followingList.to_csv('/data/FocusOnEachOther.csv',index=0)
# save the file and .... remoce the index
