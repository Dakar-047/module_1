#!/usr/bin/env python
# coding: utf-8

# In[247]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter


# In[381]:


data = pd.read_csv('movie_bd_v5.xls',sep = '\t', encoding='koi8-r', delimiter = ',')
data.sample(5)


# In[382]:


data.describe()


# # Предобработка

# In[383]:


answers = {} # создадим словарь для ответов

# тут другие ваши предобработки колонок например:

#add a column to the dataset with information about the total profit or loss of the movie
data ['profit'] = data['revenue'] - data['budget']

#the time given in the dataset is in string format.
#So we need to change this in datetime format by adding a new column
data['release_date_1'] = pd.to_datetime(data['release_date'])


# # 1. У какого фильма из списка самый большой бюджет?

# Использовать варианты ответов в коде решения запрещено.    
# Вы думаете и в жизни у вас будут варианты ответов?)

# In[384]:


# в словарь вставляем номер вопроса и ваш ответ на него
# Пример: 
answers['1'] = '2. Spider-Man 3 (tt0413300)'
# запишите свой вариант ответа
answers['1'] = 'Pirates of the Caribbean: On Stranger Tides (tt1298650) +'
# если ответили верно, можете добавить комментарий со значком "+"


# In[252]:


# тут пишем ваш код для решения данного вопроса:
data.loc[data['budget'] == data['budget'].max(),'original_title'].values[0]


# ВАРИАНТ 2

# In[201]:


# можно добавлять разные варианты решения
data[(data.budget == data.budget.max())].original_title.describe()


# # 2. Какой из фильмов самый длительный (в минутах)?

# In[385]:


# думаю логику работы с этим словарем вы уже поняли, 
# по этому не буду больше его дублировать
answers['2'] = 'Gods and Generals (tt0279111) +'


# In[254]:


data.loc[(data.runtime == data.runtime.max()),'original_title'].values[0]


# # 3. Какой из фильмов самый короткий (в минутах)?
# 
# 
# 
# 

# In[386]:


answers['3'] = 'Winnie the Pooh (tt1449283) +'

data.loc[(data.runtime == data.runtime.min()),'original_title'].values[0]


# # 4. Какова средняя длительность фильмов?
# 

# In[387]:


answers['4'] = '110 +'

round (data.runtime.mean())


# # 5. Каково медианное значение длительности фильмов? 

# In[388]:


answers['5'] = '107 +'

round (data.runtime.median())


# # 6. Какой самый прибыльный фильм?
# #### Внимание! Здесь и далее под «прибылью» или «убытками» понимается разность между сборами и бюджетом фильма. 
# ####(прибыль = сборы - бюджет) в нашем датасете это будет (profit = revenue - budget) 

# In[389]:


answers['6'] = 'Avatar (tt0499549) +'

# лучше код получения столбца profit вынести в Предобработку что в начале
grouped_data = data.groupby(['original_title'])['profit'].sum().sort_values(ascending=False)
print(grouped_data.head(1))


# # 7. Какой фильм самый убыточный? 

# In[390]:


answers['7'] = 'The Lone Ranger (tt1210819) +'

grouped_data = data.groupby(['original_title'])['profit'].sum().sort_values(ascending=True)
print(grouped_data.head(1))


# # 8. У скольких фильмов из датасета объем сборов оказался выше бюджета?

# In[391]:


answers['8'] = '1478 +'

len (data[data.profit > 0])


# # 9. Какой фильм оказался самым кассовым в 2008 году?

# In[392]:


answers['9'] = 'The Dark Knight (tt0468569) +'

df1 = data.loc[data['release_year'].isin(['2008'])].pivot_table(values=['revenue'],
index=['release_year'],
columns=['original_title'],
aggfunc='max')
df1.max().sort_values(ascending=False)


# # 10. Самый убыточный фильм за период с 2012 по 2014 г. (включительно)?
# 

# In[393]:


answers['10'] = 'The Lone Ranger (tt1210819) +'

df = data.loc[data['release_year'].isin(['2012','2013','2014'])].pivot_table(values=['profit'],
index=['release_year'],
columns=['original_title'],
aggfunc='sum')
df.min().sort_values(ascending=True)


# # 11. Какого жанра фильмов больше всего?

# In[394]:


answers['11'] = 'Drama +'

# эту задачу тоже можно решать разными подходами, попробуй реализовать разные варианты
# если будешь добавлять функцию - выноси ее в предобработку что в начале

sample1 = data.genres.str.split('|', expand = True)
sample2 = sample1.stack()
s = sample2.tolist()

data_genres = pd.Series(s)
data_genres.value_counts()


# ВАРИАНТ 2

# In[265]:


display(data['genres'].str.split('|').explode().value_counts())


# # 12. Фильмы какого жанра чаще всего становятся прибыльными? 

# In[395]:


answers['12'] = 'Drama +'

genres_profit = data[data.profit > 0]
sample1 = genres_profit.genres.str.split('|', expand = True)
sample2 = sample1.stack()
s = sample2.tolist()

data_genres = pd.Series(s)
data_genres.value_counts()


# # 13. У какого режиссера самые большие суммарные кассовые сбооры?

# In[396]:


answers['13'] = 'Peter Jackson +'

data ['directors'] = data.director.apply(lambda s: s.split('|'))
data_1 = data.explode('directors')

data_1.groupby(by = 'directors').revenue.sum().sort_values(ascending = False)


# # 14. Какой режисер снял больше всего фильмов в стиле Action?

# In[397]:


answers['14'] = 'Robert Rodriguez +'

genres1 = data[data.genres.str.contains('Action', na=False)]
director1 = genres1['director'].str.split('|',expand=True).stack().value_counts()
director1.head(1)


# # 15. Фильмы с каким актером принесли самые высокие кассовые сборы в 2012 году? 

# In[398]:


answers['15'] = 'Chris Hemsworth +'

c1 = data[data.release_year == 2012][['cast', 'revenue']]
c1.cast = c1.cast.apply(lambda s: s.split('|'))
c2 = c1.explode('cast')

c2.groupby(by = 'cast').revenue.sum().sort_values(ascending = False)


# # 16. Какой актер снялся в большем количестве высокобюджетных фильмов?

# In[399]:


answers['16'] = 'Matt Damon +'

b1 = data[(data.budget > data.budget.mean())][['cast', 'budget']]
b1.cast = b1.cast.apply(lambda s: s.split('|'))
b2 = b1.explode('cast')

b2.groupby(by = 'cast').budget.count().sort_values(ascending = False)


# # 17. В фильмах какого жанра больше всего снимался Nicolas Cage? 

# In[400]:


answers['17'] = 'Action +'

n1 = data[data.cast.str.contains('Nicolas Cage', na=False)]
n1.genres = n1.genres.apply(lambda s: s.split('|'))
n2 = n1.explode('genres')

n2.groupby(by = 'genres').genres.count().sort_values(ascending = False)


# # 18. Самый убыточный фильм от Paramount Pictures

# In[401]:


answers['18'] = 'K-19: The Widowmaker (tt0267626) +'

p1 = data[data.production_companies.str.contains('Paramount Pictures', na=False)]
p1.production_companies = p1.production_companies.apply(lambda s: s.split('|'))
p2 = p1.explode('production_companies')


pivot = p2.pivot_table(columns='production_companies', index = 'original_title', \
        values = 'profit', aggfunc='sum', fill_value=0)
pivot['Paramount Pictures'].sort_values (ascending=True)


# # 19. Какой год стал самым успешным по суммарным кассовым сборам?

# In[402]:


answers['19'] = '2015 +'

grouped_df = data.groupby(['release_year'])['revenue'].sum().sort_values(ascending=False)
display(grouped_df)


# # 20. Какой самый прибыльный год для студии Warner Bros?

# In[403]:


answers['20'] = '2014 +'

data.production_companies = data.production_companies.apply(lambda s: s.split('|'))
w1 = data.explode('production_companies')
w2 = w1[w1.production_companies.str.contains('Warner Bros', na=False)]

grouped_df = w2.groupby(['release_year'])['profit'].sum().sort_values(ascending=False)
display(grouped_df)


# # 21. В каком месяце за все годы суммарно вышло больше всего фильмов?

# In[404]:


answers['21'] = 'Сентябрь +'

data['release_date_1'] = pd.to_datetime(data['release_date'])
data['month'] = data['release_date_1'].map(lambda x:  x.month)


month_df= data.pivot_table(columns = 'month', index = 'original_title', \
          values = 'revenue', aggfunc = 'count', fill_value=0)
month_df.sum().sort_values(ascending=False)


# # 22. Сколько суммарно вышло фильмов летом? (за июнь, июль, август)

# In[405]:


answers['22'] = '450 +'

data['release_date_1'] = pd.to_datetime(data['release_date'])
data['month'] = data['release_date_1'].map(lambda x: x.month)

count = 0

for i in data ['month']:
    if 6 <= i <= 8:
        count+=1
print (count)


# # 23. Для какого режиссера зима – самое продуктивное время года? 

# In[406]:


answers['23'] = 'Peter Jackson +'

data['release_date_1'] = pd.to_datetime(data['release_date'])
data['month'] = data['release_date_1'].map(lambda x: x.month)
data.director = data.director.apply(lambda s: s.split('|'))
data_1 = data.explode('director')


pivot = data_1.loc[data_1['month'].isin(['12', '1', '2'])].pivot_table(columns = 'director', \
        index = 'original_title', values = 'revenue', aggfunc = 'count', fill_value=0)
pivot.sum().sort_values(ascending=False)


# # 24. Какая студия дает самые длинные названия своим фильмам по количеству символов?

# In[407]:


answers['24'] = 'Four By Two Productions +'

data = pd.read_csv('movie_bd_v5.xls',sep = '\t', encoding='koi8-r', delimiter = ',')

data['title_lenght'] = data['original_title'].map(lambda x: len(x))
data.production_companies = data.production_companies.apply(lambda s: s.split('|'))
data_2 = data.explode('production_companies')

grouped_df = data_2.groupby(['production_companies'])['title_lenght']\
             .max().sort_values(ascending=False)
display(grouped_df)


# # 25. Описание фильмов какой студии в среднем самые длинные по количеству слов?

# In[408]:


answers['25'] = 'Midnight Picture Show +'

data = pd.read_csv('movie_bd_v5.xls',sep = '\t', encoding='koi8-r', delimiter = ',')


data['overview_lenght'] = data['overview'].map(lambda x: len(x))
data.production_companies = data.production_companies.apply(lambda s: s.split('|'))
data_3 = data.explode('production_companies')


pivot = data_3.pivot_table(columns = 'production_companies',\
        values = 'overview_lenght', aggfunc = 'mean', fill_value=0)
pivot.max().sort_values(ascending=False)


# # 26. Какие фильмы входят в 1 процент лучших по рейтингу? 
# по vote_average

# In[409]:


answers['26'] = 'Inside Out, The Dark Knight, 12 Years a Slave +'
answers['27'] = 'Daniel Radcliffe & Rupert Grint +'

grouped_df = data.groupby(['original_title'])['vote_average'].max()\
             .sort_values(ascending=False)
print(grouped_df.head(round(len(grouped_df)*0.01)))


# # 27. Какие актеры чаще всего снимаются в одном фильме вместе?
# 

# ВАРИАНТ 2

# # Submission

# In[410]:


# в конце можно посмотреть свои ответы к каждому вопросу
answers


# In[411]:


# и убедиться что ни чего не пропустил)
len(answers)


# In[ ]:





# In[ ]:




