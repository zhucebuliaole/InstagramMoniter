import pandas as pd
# import instagram1
import time
import scraper.instagram1 as instagram1

df = pd.read_csv("../data//real/1.csv",usecols=[1],names=['username'])
usernames = df.values.tolist()

for i in range(0,len(usernames)):
    instagram1.main(str(usernames[i][0]))
    time.sleep(5)