#  Purpose: This script is used to preprocess the data for the Grossman et al. 2017 dataset.


# Display the first few rows of the Rossman dataset
rossman_df.head()

# Display the last few rows of the Rossman dataset
rossman_df.tail()

#  check the shape of the dataset
rossman_df.shape

#Checking info of data as data types and rows and cols
rossman_df.info()

#Checking Null Values
rossman_df.isnull().sum()

#Summary Statastics
rossman_df.describe()

#No. Of Stores in the Dataset
rossman_df.Store.nunique()

# Value_counts of StateHoliday Column
rossman_df.StateHoliday.value_counts()

print(rossman_df['Date'].min(),'initial')
print(rossman_df['Date'].max(),'final')


# This tells us we have a data of almost 3 years.
# extract year, month, day and week of year from "Date"
rossman_df['Date']=pd.to_datetime(rossman_df['Date'])
rossman_df['Year'] = rossman_df['Date'].apply(lambda x: x.year)
rossman_df['Month'] = rossman_df['Date'].apply(lambda x: x.month)
rossman_df['Day'] = rossman_df['Date'].apply(lambda x: x.day)
rossman_df['WeekOfYear'] = rossman_df['Date'].apply(lambda x: x.weekofyear)

rossman_df.sort_values(by=['Date','Store'],inplace=True,ascending=[False,True])
rossman_df.head(2)

# EDA On Rossman Dataset and handling missing values
# Heatmap of the Rossman Dataset

numeric_cols = rossman_df.select_dtypes(include=['int64', 'float64']).columns
correlation_map = rossman_df[numeric_cols].corr()
obj = np.array(correlation_map)
obj[np.tril_indices_from(obj)] = False
fig,ax= plt.subplots()
fig.set_size_inches(9,9)
sns.heatmap(correlation_map, mask=obj,vmax=.7, square=True,annot=True)

# Since graph given from above line of code dictates that Stores mainly closed on Sunday

sns.countplot(x='DayOfWeek',hue='Open',data=rossman_df)


# Sales Are nearly doubled High When Promo is Running

#Impact of promo on sales
Promo_sales = pd.DataFrame(rossman_df.groupby('Promo').agg({'Sales':'mean'}))
sns.barplot(x=Promo_sales.index, y = Promo_sales['Sales'])

# from the above lines of code We can see that In the month of November and Specially in December Sales is increasing Rapidly every year on the christmas eve.

sns.catplot(x="Month" ,y = "Sales" , data=rossman_df, kind="point", aspect=2,height=10)


# Value Counts of SchoolHoliday Column
rossman_df.SchoolHoliday.value_counts()


# As we can see in the Piechart Sales affected by School Holiday is 18% and Mainly Sales aren't afffected by School Holiday
labels = 'Not-Affected' , 'Affected'
sizes = rossman_df.SchoolHoliday.value_counts()
colors = ['gold', 'silver']
explode = (0.1, 0.0)
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=180)
plt.axis('equal')
plt.title("Sales Affected by Schoolholiday or Not ?",fontsize=20)
plt.plot()
fig=plt.gcf()
fig.set_size_inches(6,6)
plt.show()


#  Transforming Variable StateHoliday
rossman_df["StateHoliday"] = rossman_df["StateHoliday"].map({0: 0, "0": 0, "a": 1, "b": 1, "c": 1})
rossman_df.StateHoliday.value_counts()

# As we can see in the Piechart Sales affected by State Holiday is only 3% means Sales aren't afffected by State Holiday

labels = 'Not-Affected' , 'Affected'
sizes = rossman_df.StateHoliday.value_counts()
colors = ['orange','green']
explode = (0.1, 0.0)
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=180)
plt.axis('equal')
plt.title("Sales Affected by State holiday or Not ?",fontsize=20)
plt.plot()
fig=plt.gcf()
fig.set_size_inches(6,6)
plt.show()

# As Sales isn't much affected by State Holiday so i'm removing this column
rossman_df.drop('StateHoliday',inplace=True,axis=1)

# Histogram Representation of Sales. Here 0 is showing because most of the time store was closed.

#distribution of sales
fig, ax = plt.subplots()
fig.set_size_inches(11, 7)
sns.distplot(rossman_df['Sales'], kde = False,bins=40);


# Sales vs Customers
# linear relation between sales and customers
sns.lmplot(x= 'Sales' , y ='Customers',data=rossman_df, palette='seismic', height=5,aspect=1, line_kws={'color':'blue'})

# Analysing the Store Dataset
store_df.head(5)
store_df.tail()


# Checking Information about Dataset
store_df.shape

#Checking info of data as data types and rows and cols
store_df.info()

#Checking Null Values
store_df.isnull().sum()

# creating heatmap for null values
plt.figure(figsize=(10,6))
sns.heatmap(store_df.isnull(),yticklabels= False, cbar= False, cmap= 'gnuplot')


labels = 'a' , 'b' , 'c' , 'd'
sizes = store_df.StoreType.value_counts()
colors = ['orange', 'green' , 'red' , 'pink']
explode = (0.1, 0.0 , 0.15 , 0.0)
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=180)
plt.axis('equal')
plt.title("Distribution of different StoreTypes")
plt.plot()
fig=plt.gcf()
fig.set_size_inches(6,6)
plt.show()


# Remove features with high percentages of missing values
# we can see that some features have a high percentage of missing values and they won't be accurate as indicators, so we will remove features with more than 30% missing values.
# remove features
store_df = store_df.drop(['CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear','Promo2SinceWeek',
                     'Promo2SinceYear', 'PromoInterval'], axis=1)



# CompetitionDistance is distance in meters to the nearest competitor store
# let's first have a look at its distribution


# Replace missing values in features with low percentages of missing values
sns.distplot(store_df.CompetitionDistance.dropna())
plt.title("Distributin of Store Competition Distance")

# The distribution is right skewed, so we'll replace missing values with the median.
# replace missing values in CompetitionDistance with median for the store dataset

store_df.CompetitionDistance.fillna(store_df.CompetitionDistance.median(), inplace=True)


# Pairplot for Store Dataset
#pairplot for store dataset
sns.set_style("whitegrid", {'axes.grid' : False})
pp=sns.pairplot(store_df,hue='StoreType')
pp.fig.set_size_inches(10,10);


# Checking stores with their assortment type
#checking stores with their assortment type
sns.set_style("whitegrid")
fig, ax = plt.subplots()
fig.set_size_inches(11, 7)
store_type=sns.countplot(x='StoreType',hue='Assortment', data=store_df,palette="inferno")

for p in store_type.patches:
    store_type.annotate(f'\n{p.get_height()}', (p.get_x()+0.15, p.get_height()),ha='center', va='top', color='white', size=10)

# Since We can see that there is not such significant differences in these 3 years in terms of sales.
#plotting year vs sales
sns.catplot(x='Year',y='Sales',data=rossman_df, height=4, aspect=4 );


# Merging Two Datasets
df = pd.merge(rossman_df, store_df, how='left', on='Store')
df.head()

df.shape
