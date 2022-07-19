import json
from turtle import left 
import pandas as pd
import requests



  
subreddit = 'buildapcsales'
limit = 100
timeframe = 'week' #hour, day, week, month, year, all
listing = 'new' # controversial, best, hot, new, random, rising, top
  
def get_reddit(subreddit,listing,limit,timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()
 
def get_post_titles(r):
    '''
    Get a List of post titles
    '''
    posts = []
    for post in r['data']['children']:
        x = post['data']['title']
        
        posts.append(x)
    return posts
    



def get_results(r):
    '''
    Create a DataFrame Showing Title, URL, Score and Number of Comments.
    '''
    myDict = {}
    for post in r['data']['children']:
        
        myDict[post['data']['title']] = {'Link':post['data']['url'],'Flair':post['data']['link_flair_text']}

        
    date = {}
    for post in r['data']['children']:

        date[post['data']['title']] = {'Created Date':post['data']['created_utc']}

    
    
    df = pd.DataFrame.from_dict(myDict, orient='index')
    df2 = pd.DataFrame.from_dict(date, orient='index')

    df2['Created Date'] = pd.to_datetime(df2['Created Date'], unit = 's')

    df = pd.concat([df, df2], ignore_index=False, axis=1)

    return df
    
    
 


if __name__ == '__main__':
    r = get_reddit(subreddit,listing,limit,timeframe)
    df = get_results(r)
   