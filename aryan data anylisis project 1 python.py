import pandas as pd
df = pd.read_csv("customer_shopping_behavior.csv")

# print(df.head(8)) 
# print (df.info())
# print(df.describe(include='all'))
# print (df.isnull().sum())


df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))


## Renaming columns according to snake casing for better readability and documentation
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ', "_")
df=df.rename(columns={'purchase_amount_(usd)': "purchase_amount"})


agecat=['young-adult','adult','middle-aged','senior-citizen']
df['age_group'] = pd.qcut(df['age'],q=4,labels=agecat)
# print(df[['age','age_group']])

# create new column purchase_frequency_days
frequency_mapping={'Fortnightly': 14, 'Weekly': 7, 'Monthly': 30, 'Quarterly': 90, 'Bi-Weekly': 14, 'Annually': 365, 'Every 3 Months': 90}
df['purchase_freq_days']= df['frequency_of_purchases'].map(frequency_mapping)


#dropping columns with same data
(df['discount_applied']==df['promo_code_used']).all()
df=df.drop("promo_code_used", axis=1)
# print(df.columns)

#connecting python scipt to mysql

import sqlalchemy

from sqlalchemy import create_engine

# MySQL connection
username = "root"
password = "xezen133"
host = "localhost"
port = "3306"
database = "dataanylisis_project_1"

engine = create_engine(f"mysql+pymysql://{'root'}:{'xezen133'}@{'localhost'}:{'3306'}/{'dataanylisis_project_1'}")

# Write DataFrame to MySQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

# Read back sample
print(pd.read_sql("SELECT * FROM customer LIMIT 5;", engine))
#print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")