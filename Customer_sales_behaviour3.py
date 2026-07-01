import pandas as pd
from sqlalchemy import create_engine
df = pd.read_csv('end to end project\customer_shopping_behavior.csv')
print("Data loaded successfully!")
print(df.head())
print(df.info())
print(df.describe(include='all'))

# for handling missing values

print("Missing values in each column:")
print(df.isnull().sum())  
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
print("Data after filling missing values:")
print(df.isnull().sum())  

# for rename columns or for lower case and replace space with underscore

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
df = df.rename(columns={'promo_code_used':'promo_code',})
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
df=df.rename(columns={'frequency_of_purchases':'purchase_frequency'})
print(df.columns)

# for age group categorization using pd.cut()

df['age_group'] = pd.cut(
    df['age'],[18, 25, 40, 60, 100],
    labels=['young_adults', 'adults', 'middle-aged', 'seniors']
    )
print(df[['age', 'age_group']].head(10))



frequency_mapping = {
    'Fortnightly': 14,
    'Weekly':7,
    'Monthly':30,
    'Quarterly':90,
    'Bi-weekly':14,
    'Annually':365,
    'Every 3 months':90,
}
df['purchase_frequency_days'] = df['purchase_frequency'].map(frequency_mapping)
print(df[['purchase_frequency_days','purchase_frequency']].head(10))

print(df[[ 'discount_applied', 'promo_code']].head(10))
df['discount_applied'] == df['promo_code'].all()
df = df.drop('promo_code', axis=1)
print(df.columns)

df.to_excel("data.xlsx", index=False)

username = "postgres"
password = "Usman0987"
host = "localhost"
port = "5432"   
database = "Customer_sales"
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')

table_name = "customer_sales_data"
df.to_sql(table_name, engine, if_exists='replace', index=False) 
print(f"Data inserted into PostgreSQL table '{table_name}' successfully!")
