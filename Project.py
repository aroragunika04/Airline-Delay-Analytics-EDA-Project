import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from statsmodels.stats.weightstats import ztest
import warnings
warnings.filterwarnings('ignore')
#Loading Dataset
df = pd.read_excel(r"C:\Users\Gunika\OneDrive\Desktop\work\Notes\ot_delaycause1_DL\Airline_Delay_Cause.xlsx")

#Columns and their data types
cols = df.info()
print(cols)

#Check for missing data
is_null = df.isnull().sum()
print(is_null)

#Handling null values
delay_cols = ['carrier_delay','weather_delay','nas_delay','security_delay','late_aircraft_delay']
df[delay_cols] = df[delay_cols].fillna(0)

df['arr_delay'] = df['arr_delay'].fillna(0)
df['arr_diverted']=df['arr_diverted'].fillna(0)
df['arr_cancelled'] = df['arr_cancelled'].fillna(0)

count_cols = ['carrier_ct','weather_ct','nas_ct','security_ct','late_aircraft_ct']
df[count_cols] = df[count_cols].fillna(0)

df['arr_flights'] = df['arr_flights'].fillna(0)
df['arr_del15']=df['arr_del15'].fillna(df['arr_del15'].mean())

check_null = df.isnull().sum()
print("After Handling Null values: \n")
print(check_null)

#Statiscal Analysis
print("Statiscal Analysis: \n",df.describe())

#Checking Skewness of data
print("Skewness: \n")
numeric_cols = df.select_dtypes(include=[np.number])
skewness = numeric_cols.skew()
print(skewness)

#Airline performance
plt.figure(figsize=(8,6))
d = df.groupby('carrier')[['arr_flights','arr_del15']].sum()
sns.lineplot(data = d,marker='o',palette ='tab10')
plt.title("Airline Performance (Scheduled vs Delayed Flights)")
plt.xticks(rotation=90)
plt.xlabel("Airlines")
plt.ylabel("Count of flights(in Lakhs)")
plt.xticks(rotation = 90)
plt.show()

top10 = df.groupby('carrier')['arr_del15'].mean().sort_values().head(10).reset_index()
sns.barplot(data=top10, x='arr_del15', y='carrier', palette='rocket')
plt.title("Top 10 Airlines with Least Arrival Delays")
plt.xlabel("Average Delay")
plt.ylabel("Airline")
plt.grid(axis='x')
plt.show()

#distribution of arrival delay times
df[delay_cols].hist(bins=30,color='blue',edgecolor='black')
plt.suptitle("Frequency of Arrival Delay Times (in Minutes)")
plt.show()

# Identifying the primary cause for delay (carrier, weather, NAS, security, late aircraft).
total = df[count_cols].sum()
major_cause = total.idxmax()
print(f'Major Cause for delay in various Airline: {major_cause}')
plt.figure(figsize=(8,6))
plt.pie(total,autopct="%2.2f%%",labels = count_cols,colors= sns.color_palette('muted'))
plt.title("No of flights Delayed")
plt.show()

plt.figure(figsize=(8,6))
plt.pie(df[delay_cols].sum(),autopct = "%2.2f%%",labels=delay_cols,colors=sns.color_palette("hls"))
plt.title("Time Delayed(in minutes)")
plt.show()

# Compare Airport Performance
df_sorted = df.sort_values('arr_delay', ascending=False)
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x='airport', y='arr_delay', hue='airport', errorbar=None)
plt.title('Average Arrival Delay by Airport')
plt.ylabel('Average Arrival Delay (minutes)')
plt.xlabel('Airport')
plt.xticks(rotation=90)
plt.show()

#Seasonal Trend
monthly = df.groupby('month')['arr_del15'].mean().reset_index()
sns.lineplot(data=monthly,x='month',y='arr_del15',marker='o',color='b')
plt.title('Monthly Average Arrival Delays') 
plt.xlabel('Month')
plt.ylabel('Average Flights Delayed')
plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.grid()
plt.show()

yearly = df.groupby('year')['arr_del15'].mean().reset_index()
sns.lineplot(data=yearly,x='year',y='arr_del15',marker ='o',color='g')
plt.title("Yearly Average Arrival Delays")
plt.xlabel("Years")
plt.ylabel("Average Flights Delayed")
plt.xticks([2020, 2021, 2022, 2023,2024])
plt.grid()
plt.show()

#Interdependencies between delay types
correlation_matrix = df[count_cols].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Between Different Delay Types')
plt.show()

# Relationship Between Number of Flights and Delay Counts
plt.figure(figsize=(8,6))
sns.scatterplot(x=df['arr_flights'],y=df['arr_del15'],alpha=0.6,color= 'red')
plt.title("Relationship Between Number of Flights and Delay Counts")
plt.xlabel("Flights Arrived")
plt.ylabel("Flights Delayed")
plt.grid()
plt.show()

#outliers
Q1= df[delay_cols].quantile(0.25)
Q3 = df[delay_cols].quantile(0.75)
IQR = Q3-Q1
lower =  Q1 - 1.5*IQR
upper =  Q3 + 1.5*IQR
outliers = ((df[delay_cols]<lower)|(df[delay_cols]>upper)).sum()
print(f'Outliers detected: {outliers}')
sns.boxplot(data=df[delay_cols],palette='pastel')
plt.title("Outlier Detection in Flight Delay Causes")
plt.xlabel("Delay Cause")
plt.ylabel("Delay Duration (minutes)")
plt.yscale("log")
plt.show()

# Z-Testing
year1 = df[df['year']==2024]['arr_delay']
year2 = df[df['year']==2023]['arr_delay']
z_test,p_val = ztest(year1,year2)
print(f"Z-Statistics: {z_test: .2f}")
print(f"P_value: {p_val: .2f}")
alpha=0.05
if(p_val<alpha):
    print("There is a Significant Difference in Arrival Delay Time b/w 2024 and 2023.")
else:
    print("There is not Significant Difference in Arrival Delay Time b/w 2024 and 2023.")



















