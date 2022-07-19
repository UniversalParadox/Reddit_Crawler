


import json
import pandas as pd
import requests
import pygsheets
from IPython.display import display

#authorization for google sheets api
gc = pygsheets.authorize(service_file=r"<INSERT-SERVICE-ACCOUNT-JSON-LOCATION")
  
subreddit = 'buildapcsales' #choose a subreddit
limit = 100 #Reddit limits queries to their api
timeframe = 'week' #hour, day, week, month, year, all
listing = 'new' # controversial, best, hot, new, random, rising, top
  
def get_reddit(subreddit,listing,limit,timeframe):
    #This gathers the basic JSON file from reddit with the parameters that were set above.
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
    Create a DataFrame with the post title, URL ink, and Flair.
    The parameters can be easily be changed to gather different data types.
    '''
    myDict = {}
    for post in r['data']['children']:
        
        myDict[post['data']['title']] = {'Post Title':post['data']['title'],'Link':post['data']['url'],'Flair':post['data']['link_flair_text']}

        
    date = {} #Dates are hard,
    for post in r['data']['children']:

        date[post['data']['title']] = {'Created Date':post['data']['created_utc']}

    
    
    df = pd.DataFrame.from_dict(myDict, orient='index') #Creates a dataframe for the first set of data
    df2 = pd.DataFrame.from_dict(date, orient='index') #Creates a dataframe for the second set of data

    df2['Created Date'] = pd.to_datetime(df2['Created Date'], unit = 's') #convert from EPOCH time to UTC

    df = pd.concat([df, df2], ignore_index=False, axis=1) #Combines both dataframes together, based on column names.
    
    return df
    
    
 

if __name__ == '__main__':
    r = get_reddit(subreddit,listing,limit,timeframe)
    df = get_results(r)
    sh = gc.open('<INSERT-NAME-OF-GOOGLE-SHEET') #Please ensure that you have the service account added as an editor in order for it to write.
    wks = sh[0] #Selects the first sheet
    wks.set_dataframe(df,(1,1)) #Imports the dataframe to the selected google sheet
    input("\nPlease press the Enter key to close this program.")
    