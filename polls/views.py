from django.http import HttpResponse
from django.shortcuts import render
from searchtweets import  *
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os
import json
from rest_framework.response import Response

def index(request):
    bearer_token = os.environ['bearer_token']
    v2_search_args = {'bearer_token': bearer_token,
    'endpoint': 'https://api.twitter.com/2/tweets/count/recent',
    'extra_headers_dict': None}

    output = {"mentions":[],
            "hashtags":[]}
    for hstag in ["#NFTs","#gaypride","#hololive","@happygrape123","#solana"]:
    #  hstag = input("Search for hashtag:")
        query = gen_request_parameters(hstag.strip(), results_per_call=1000, granularity = "day")
        tweets = collect_results(query,max_tweets=1000,result_stream_args=v2_search_args)
        if(hstag[0]=='#'):
            tempdict = {"hashtag":hstag[1::].strip(), "count":tweets[0]['meta']['total_tweet_count']}
            output["hashtags"].append(tempdict)
        if(hstag[0]=='@'):
            tempdict = {"account":hstag[1::].strip(), "count":tweets[0]['meta']['total_tweet_count']}
            output["mentions"].append(tempdict)


    output_discord = {"servers":[]}
    for server in ["TYsjGVDU",
    "thebalanceffxiv",
    "pewdiepie",
    "lsxyz9"]:
        url = 'https://discord.com/invite/' + server.strip()
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for i in soup.findAll("meta"):
            try:
                if(i["name"]=="twitter:description"):
                    description = i
            except:
                pass
        num = ""
        memberstring = " members"
        same = 0
        members = 0
        index = 0
        #print(description)
        for i in description["content"]:
            if(i.isnumeric()):
                num+=i
            elif(i!=',' and num!=''):
                if(num.isnumeric()):
                    members = num
                num = ""
        title = soup.findAll("title")
        for i in title[0]:
            name = str(i)
        tempdict = {"servername": name, "members": members}
        output_discord["servers"].append(tempdict)

    results = {
        "output":output,
        "output_discord":output_discord
    }
    # Render the HTML template index.html with the data in the context variable
    print(results)
    return HttpResponse(json.dumps(results))
