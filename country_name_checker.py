import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter  # https://geopy.readthedocs.io/en/stable/#usage-with-pandas


df = pd.read_csv('covid19_tweets.csv')

# Getting locations of USA, India, Bangladesh
us_url = 'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States'
us_table = pd.read_html(us_url)
us_states = us_table[0].iloc[:, 0].tolist()
us_cities = us_table[0].iloc[:, 1].tolist() + us_table[0].iloc[:, 2].tolist() + us_table[0].iloc[:, 3].tolist()
us_Federal_district = us_table[1].iloc[:, 0].tolist()
us_Inhabited_territories = us_table[2].iloc[:, 0].tolist()
us_Uninhabited_territories = us_table[3].iloc[:, 0].tolist()
us_Disputed_territories = us_table[4].iloc[:, 0].tolist()
us = us_states + us_cities + us_Federal_district + us_Inhabited_territories + us_Uninhabited_territories + us_Disputed_territories

in_url = 'https://en.wikipedia.org/wiki/States_and_union_territories_of_India#States_and_Union_territories'
india_table = pd.read_html(in_url)
in_states = india_table[3].iloc[:, 0].tolist() + india_table[3].iloc[:, 4].tolist() + india_table[3].iloc[:, 5].tolist()
in_unions = india_table[4].iloc[:, 0].tolist()
ind = in_states + in_unions

bd_url = 'https://en.wikipedia.org/wiki/Districts_of_Bangladesh#List_of_districts'
bd_table = pd.read_html(bd_url)
bd = bd_table[1].iloc[:, 0].str[:-9].tolist()

usToStr = ' '.join([str(elem) for elem in us])
indToStr = ' '.join([str(elem) for elem in ind])
bdToStr = ' '.join([str(elem) for elem in bd])

# Country name checker functions

def checkl(T):
    TSplit_space = [x.lower().strip() for x in T.split()]
    TSplit_comma = [x.lower().strip() for x in T.split(',')]
    TSplit = list(set().union(TSplit_space, TSplit_comma))
    res_ind = [ele for ele in ind if(ele in T)]
    res_us = [ele for ele in us if(ele in T)]
    res_bd = [ele for ele in bd if(ele in T)]

    if 'india' in TSplit or 'hindustan' in TSplit or 'bharat' in TSplit or T.lower() in indToStr.lower() or bool(res_ind) == True :
        T = 'India'
    elif 'US' in T or 'USA' in T or 'United State' in T or 'usa' in TSplit or 'united state' in T.lower() or T.lower() in usToStr.lower() or bool(res_us) == True :
        T = 'USA'
    elif 'Bangladesh' in T or 'bangla' in T.lower() or T.lower() in usToStr.lower() or bool(res_bd) == True :
         T = 'Bangladesh'
    elif len(T.split(','))>1 :
        if T.split(',')[0] in indToStr or  T.split(',')[1] in indToStr :
             T = 'India'
        elif T.split(',')[0] in usToStr or  T.split(',')[1] in usToStr :
             T = 'USA'
        elif T.split(',')[0] in bdToStr or  T.split(',')[1] in bdToStr :
             T = 'Bangladesh'
        else:
             T = "Others"
    else:
        T = "Others"
    return T

def checkl1(T):
    TSplit = T.strip().lower().replace(",", " ").split()
    res_ind = [ele for ele in ind if(ele in T)]
    res_us = [ele for ele in us if(ele in T)]
    res_bd = [ele for ele in bd if(ele in T)]

    if 'india' in TSplit or 'hindustan' in TSplit or 'bharat' in TSplit or T.lower() in indToStr.lower() or len(res_ind) > 0 :
        T = 'India'
    elif 'US' in T or 'USA' in T or 'United State' in T or 'usa' in TSplit or 'united state' in T.lower() or T.lower() in usToStr.lower() or len(res_us) > 0 :
        T = 'USA'
    elif 'Bangladesh' in T or 'bangla' in T.lower() or T.lower() in usToStr.lower() or len(res_bd) > 0:
         T = 'Bangladesh'
    elif len(T.split(','))>1 :
        if T.split(',')[0] in indToStr or  T.split(',')[1] in indToStr :
             T = 'India'
        elif T.split(',')[0] in usToStr or  T.split(',')[1] in usToStr :
             T = 'USA'
        elif T.split(',')[0] in bdToStr or  T.split(',')[1] in bdToStr :
             T = 'Bangladesh'
        else:
             T = "Others"
    else:
        T = "Others"
    return T

def checkl2(T):
    geolocator = Nominatim(user_agent='geonames@googlegroups.com')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geocode(T)
    if location is None:
        country = 'Others'
    else:
         country = location.address.split(',')[-1].strip()
         if 'United States' in country :
            country = 'USA'
         elif 'India' in country :
            country = 'India'
         elif 'Bangladesh' in T or 'Bangladesh' in country :
            country = 'Bangladesh'
         else:
            country = 'Others'
    return country

# test 1:
print('Test #1\n')
P = ['USA', 'India', 'United States', 'Indiana', 'indiana', 'indianapolis','Bangladesh', 'New Delhi, India', 'Dhaka, Bangladesh',
   'Dhaka,bangladesh', 'New York City', 'New York, NY', 'College Station, Texas', 'Pewee Valley, KY', 'Jammu and Kashmir', 'Delhi,india',
    'india, usa', 'usa,india', 'Akhand Bharat', 'Hindustan 🇮🇳', 'fort wayne, indiana', 'milford, indiana', 'indianapolis in']
for x in P:
    if checkl1(x) != checkl2(x):
        print(x,'=>',  checkl(x),':', checkl1(x),':', checkl2(x))

# test 2
print('Test #3\n')
known_values = [
    ('astroworld', 'Others'),
    ('New York, NY', 'USA'),
    ('indianapolis in', 'USA'),
    ('Pewee Valley, KY', 'USA'),
    ('Stuck in the Middle ', 'Others'),
    ('Jammu and Kashmir', 'India'),
    ('Новоро́ссия', 'Others'),
    ('Gainesville, FL', 'USA'),
    ('dhaka,Bangladesh', 'Others'),
    ('Hotel living - various cities!  Who needs a home when hotel living is so fabulous!', 'Others'),
    ('Africa', 'Others'),
    ('new delhi', 'India'),
    ('Nagaland, India', 'India'),
    ('Brussels', 'Others'),
    ('Florida, USA', 'USA'),
    ('Northwest Indiana', 'USA'),
    ('Graz', 'Others'),
    ('Mumbai, India', 'India'),
 ]
for uloc, loc in known_values:
        if checkl1(uloc) != checkl2(uloc):
            print(uloc,'=>', loc ,':', checkl(uloc),':', checkl1(uloc),':', checkl2(uloc))

# test 3
print('Test on the dataframe\n')
for uloc in df['user_location'].dropna().iloc[0:200]:
    if checkl1(uloc) != checkl2(uloc):
        print(uloc,'=>',  checkl(uloc),':', checkl1(uloc),':', checkl2(uloc))
