#!/usr/bin/env python
# coding: utf-8

# # SIMPLE RETURNS AND LOG RETURNS

# In[339]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# # APPLE RETURNS  

# In[340]:


start="2000-01-01"
end="2024-08-12"
apple=yf.download("AAPL",start=start,end=end,interval="1d")


# In[341]:


apple=apple[["Close"]]


# In[342]:


apple


# #  indexing the dataset for proper data in each day

# In[343]:


start="2000-01-01"
end="2024-08-12"

all_days=pd.date_range(start=start,end=end,freq="D")

all_days


# In[344]:


apple


# In[345]:


apple=apple.reindex(all_days)
apple


# In[346]:


apple=apple.fillna(method="ffill")


# In[347]:


apple


# In[348]:


apple["day"]=apple.index.day_name()
# apple=apple.to_frame()


# In[349]:


apple


# In[350]:


apple=apple["Close"].to_frame()


# In[351]:


apple


# # daily returns and commulative returns

# In[352]:


apple["d_returns"]=np.log(apple.div(apple.shift(1)))


# In[353]:


apple


# In[354]:


apple.dropna(inplace=True)


# In[355]:


apple


# In[356]:


sum=apple.d_returns.sum()


# In[357]:


np.exp(apple.d_returns.sum())


# In[358]:


apple["c_returns"]=np.exp(apple.d_returns.cumsum())


# In[359]:


apple


# In[360]:


apple.c_returns.plot(figsize=(25,12),title="apple cum-sum",fontsize=20)
plt.show()


# In[361]:


apple.d_returns.mean()*252


# In[362]:


apple.d_returns.std()*np.sqrt(252)


# # drawdown

# In[363]:


# which part should the graph goes up to down 
# find the cummulative maximum 


# In[364]:


apple["cum_max"]=apple.c_returns.cummax()


# In[365]:


apple


# In[366]:


apple[["cum_max","c_returns"]].plot(figsize=(10,6),title="Apple cum-sum",fontsize=20 )
plt.show()

# apple.c_returns.plot(figsize=(25,12),title="apple cum-sum",fontsize=20)
# plt.show()


# In[367]:


apple["drawdown"]=apple["cum_max"]-apple["c_returns"]


# In[368]:


apple


# In[369]:


apple.drawdown.max()


# # max drawdown - 57.02

# apple.drawdown.Idxmax()

# In[370]:


apple.drawdown.idxmax()


# # date- >  2023- 01-05 is the date , where apple shocks goes maximum drawdown

# In[371]:


apple.loc[(apple.index=="2023-01-05")]


# In[372]:


apple.loc[(apple.index<="2023-01-05")]


# percentage drawdown

# In[373]:


apple["% draw down"]=(apple["cum_max"]-apple["c_returns" ] )/(apple["cum_max"])


# In[374]:


apple


# In[375]:


apple["% draw down"].max()


# In[376]:


apple["% draw down"].idxmax()


# In[377]:


apple.loc[(apple.index<="2003-04-17")]


# # strategy (SMA )

# In[378]:


data=apple.loc[(apple.index>="2000-01-01")]


# In[379]:


data=data["Close"].to_frame()


# In[380]:


data


# In[381]:


sma_s=40
sma_l=100



# In[382]:


data["sma_s"]=data.Close.rolling(sma_s).mean()
data["sma_l"]=data.Close.rolling(sma_l).mean()


# In[383]:


data


# In[384]:


data[["sma_s","sma_l","Close"]].plot(figsize=(10,6),title="Apple cum-sum",fontsize=20 )
plt.show()



# In[385]:


data.loc["2024"].plot(figsize=(10,6),title="Apple cum-sum",fontsize=20 )
plt.show()



# In[386]:


data.loc["2023"].plot(figsize=(10,6),title="Apple cum-sum",fontsize=20 )
plt.show()



# In[387]:


data.dropna(inplace=True)


# # precision , when sma_s > sma_l

# In[388]:


data["precision"]=np.where(data["sma_s"]>data["sma_l"],1,-1)


# In[389]:


data.head(50)


# In[390]:


data.loc[:,["sma_s","sma_l","precision"]].plot(figsize=(10,6),title="Apple cum-sum",fontsize=20 ,secondary_y="precision")
plt.show()



# In[391]:


data.loc["2024",["sma_s","sma_l","precision"]].plot(figsize=(10,6),title="Apple cum-sum",fontsize=20 ,secondary_y="precision")
plt.show()



# In[392]:


data.loc["2023",["sma_s","sma_l","precision"]].plot(figsize=(10,6),title="Apple cum-sum",fontsize=20 ,secondary_y="precision")
plt.show()



# # BUY AND HOLD

# In[393]:


data["buy_and_hold"]= np.log(data.Close.div(data.Close.shift(1)))


# In[394]:


data["strategy_b_and_h"]=data["buy_and_hold"]*data["precision"].shift(1)


# In[395]:


data.dropna(inplace=True)


# In[396]:


data


# In[397]:


data[["buy_and_hold","strategy_b_and_h"]].sum()


# # buy_and hold is greater than strategy  ==  good strategy 

# In[398]:


data[["buy_and_hold","strategy_b_and_h"]].mean()


# In[399]:


data[["buy_and_hold","strategy_b_and_h"]].std()*np.sqrt(252) #annual std deviation


# In[400]:


data[["buy_and_hold","strategy_b_and_h"]].sum().apply(np.exp)  # 1 doller after long time will be  


# # long bias strategy 

# In[401]:


data["precision2"]=data["precision"]=np.where(data["sma_s"]>data["sma_l"],1,0)


# In[402]:


data["strategy_b_and_h2"]=data["buy_and_hold"]*data["precision2"].shift(1)


# In[403]:


data


# In[404]:


data[["buy_and_hold","strategy_b_and_h2"]].sum().apply(np.exp)  # 1 doller after long time will be  


# In[405]:


data[["buy_and_hold","strategy_b_and_h2"]].std()*np.sqrt(252) #annual std deviation


# # strategy 2 gives the less bias than actual data , means  less risk 

# STRATEGY 2 IS BETTER THAN STRATEGY 1

# In[ ]:




