# Conclusion of the analysis:
# Sales are highly correlated to number of Customers.

# The most selling and crowded store type is A.

# StoreType B has the lowest Average Sales per Customer. So i think customers visit this type only for small things.

# StoreTybe D had the highest buyer cart.

# Promo runs only in weekdays.

# For all stores, Promotion leads to increase in Sales and Customers both.

# More stores are opened during School holidays than State holidays.

# The stores which are opened during School Holiday have more sales than normal days.

# Sales are increased during Chirstmas week, this might be due to the fact that people buy more beauty products during a Christmas celebration.

# Promo2 doesnt seems to be correlated to any significant change in the sales amount.

# Absence of values in features CompetitionOpenSinceYear/Month doesn’t indicate the absence of competition as CompetitionDistance values are not null where the other two values are null.


# Drop Subsets Of Data Where Might Cause Bias
# where stores are closed, they won't generate sales, so we will remove that part of the dataset
df = df[df.Open != 0]

# Open isn't a variable anymore, so we'll drop it too
df = df.drop('Open', axis=1)

# Check if there's any opened store with zero sales
df[df.Sales == 0]['Store'].sum()


# see the percentage of open stored with zero sales
df[df.Sales == 0]['Sales'].sum()/df.Sales.sum()

# remove this part of data to avoid bias
df = df[df.Sales != 0]

df_new=df.copy()


df_new = pd.get_dummies(df_new,columns=['StoreType','Assortment'])
df_new.head()

# From plot it can be sen that most of the sales have been on 1st and last day of week
#plot for sales in terms of days ofthe week
plt.figure(figsize=(15,8))
sns.barplot(x='DayOfWeek', y='Sales' ,data=df_new);