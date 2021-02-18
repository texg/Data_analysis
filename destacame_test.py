#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import datetime


# In[2]:


my_path = '/Users/texiagonzalezcaceres/Desktop/test_destacame/data'


# In[3]:


print(os.listdir(my_path))


# In[4]:


df_accounts_profile = pd.read_csv('/Users/texiagonzalezcaceres/Desktop/test_destacame/data/accounts_profile.csv')
df_financial_profile = pd.read_csv('/Users/texiagonzalezcaceres/Desktop/test_destacame/data/financial_profile.csv')
df_quotation_activity = pd.read_csv('/Users/texiagonzalezcaceres/Desktop/test_destacame/data/quotation_activity.csv')
df_payment_offer = pd.read_csv('/Users/texiagonzalezcaceres/Desktop/test_destacame/data/payment_offer.csv')


# In[5]:


df_accounts_profile.fillna(0, inplace=True)
df_financial_profile.fillna(0, inplace=True)
df_quotation_activity.fillna(0, inplace=True)
df_payment_offer.fillna(0, inplace=True)


# In[6]:


df_accounts_profile.head(4)


# In[7]:


df_financial_profile.head(4)


# In[8]:


df_quotation_activity.head(4)


# In[9]:


df_payment_offer.head(4)


# # Quantity by gender
# 
# #### Recupera la cantidad de usuarios, agrupado por género

# In[31]:


quantity_gender = df_accounts_profile.gender.value_counts()
quantity_gender = quantity_gender.to_frame()
quantity_gender.rename(index={'m': 'male', 0: 'unknown', 'f': 'female'}, inplace=True)
quantity_gender


# # Quantity by country
# 
# #### Recupera la cantidad de usuarios, agrupado por país

# In[11]:


quantity_country = df_accounts_profile.country_id.value_counts()
quantity_country = quantity_country.to_frame()
quantity_country


# # Quantity by employment_status
# 
# #### Recupera la cantidad de usuarios, agrupado por employment_status

# In[12]:


quantity_employment = df_financial_profile.employment_status.value_counts()
quantity_employment = quantity_employment.to_frame()
quantity_employment.rename(index= {0: 'unknown'}, inplace=True)
quantity_employment


# # Quantity by salary
# 
# #### Recupera la cantidad de usuarios, agrupado por salary

# In[13]:


quantity_salary = df_financial_profile.salary.value_counts()
quantity_salary = quantity_salary.to_frame()
quantity_salary


# # Most traded product
# 
# #### Recupera la cantidad de productos mas transado

# In[14]:


quantity_most_traded = df_payment_offer['product'].value_counts().max()
product_most_traded = df_payment_offer['product'].mode()

print('The most traded product is: {} which has been selected {} times'.format(product_most_traded[0],quantity_most_traded))


# # Adding field "age" in profile data
# 
# #### Crear campo edad dentro de los datos del profile

# In[15]:


df_accounts_profile['birthday'] = pd.to_datetime(df_accounts_profile['birthday'], errors = 'coerce')


# In[16]:


today = datetime.date.today()

df_accounts_profile['age'] = df_accounts_profile['birthday'].apply(
    lambda x: today.year - x.year - 
    ((today.month, today.day) < (x.month, x.day)) 
)


# In[17]:


df_accounts_profile['age'].fillna(0, inplace=True)
df_accounts_profile['age'] = df_accounts_profile['age'].astype(int)


# In[18]:


df_accounts_profile.head(5)


# # Adding field "age_range" in profile data
# 
# #### Crear campo de rango de edades dentro de los datos del profile 
# #### (values = ('0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90'))

# In[19]:


df_accounts_profile['age_range'] = pd.cut(
    x=df_accounts_profile['age'] , 
    bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90], 
    labels=[
        '0-10', 
        '10-20', 
        '20-30', 
        '30-40', 
        '40-50', 
        '50-60', 
        '60-70', 
        '70-80', 
        '80-90',
    ], 
    right=False,
)


# In[20]:


df_accounts_profile.head(5)


# # Creating df_quotation_account
# 
# #### Unir tabla quotation y account

# In[21]:


df_quotation_account = pd.merge(
    df_accounts_profile, 
    df_quotation_activity, 
    left_on='id', 
    right_on='user_id',
)


# In[22]:


df_quotation_account.drop(
    columns='id', 
    inplace=True,
)


# In[23]:


df_quotation_account.head(5)


# # Creating df_qaf
# 
# #### Unir tabla quotation, account y financial

# In[24]:


df_qaf =  pd.merge(
    pd.merge(
        df_accounts_profile,
        df_quotation_activity,
        left_on='id',
        right_on='user_id'
    ), 
    df_financial_profile, on='user_id',
)


# In[25]:


df_qaf =  pd.merge(
    df_quotation_account, 
    df_financial_profile, 
    on='user_id',
)


# # Changing to datetime
# 
# #### Cambiar el tipo de dato de created y date_joined a datetime.

# In[26]:


df_qaf['date_joined'] = pd.to_datetime(
    df_qaf['date_joined'], 
    errors='coerce',
)

df_qaf['created'] = pd.to_datetime(
    df_qaf['created'], 
    errors='coerce',
)


# In[27]:


df_qaf.dtypes


# # Creating report
# 
# #### Generar un csv con la siguiente información:
# #### user_id, ege, age_range, genger, country_id, date_joined, last_login, salary, seniority, product, created

# In[28]:


array_report = [
                'user_id', 
                'age', 
                'age_range', 
                'gender', 
                'country_id', 
                'date_joined', 
                'last_login', 
                'salary', 
                'seniority', 
                'product', 
                'created'
]
df_report = df_qaf[array_report]


# In[29]:


df_report.head(5)


# In[30]:


df_report.to_csv('/Users/texiagonzalezcaceres/Desktop/test_destacame/df_report.csv')

