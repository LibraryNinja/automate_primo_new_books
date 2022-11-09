#Code that:
#- Removes anything already in the specified Collection in Alma
#- Checks specified Alma Analytics reports (configured to have rolling date filters) to get the current MMS IDs for the report
#- Adds the MMS IDs from those items to the (now-empty) Collection

import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

#Define empty list for later
delmmsid = []

#Set up default things for base URL and course API key
#If this is not your base URL, change it to the one for your region
alma_base = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1'

#Enter your Bib Read/Write API key (enclosed in single quotes) here:
bibapi = 'YOUR-BIB-API-KEY-HERE'
headers = {"Accept": "application/json"}

#ID for new books collection
#Enter Collection ID for the Collection you're using (enclosed in single quotes) here:
newpid =  'COLLECTION-ID-GOES-HERE'

#Gets count of how many items are in the collection currently (max 100 per request)
#This is to know how many to remove for step 1
getcount = requests.get(alma_base + '/bibs/collections/' + newpid + '/bibs?apikey=' + bibapi + '&limit=1', headers=headers).json()
countdump = json.dumps(getcount)
countload=json.loads(countdump)
count = countload["total_record_count"]
print(count)

#Grabs data for the collection and adds the MMS IDs for anything already there to the "Delete" list
for offset in range (0, count, 100):
    data = requests.get(alma_base + '/bibs/collections/' + newpid + '/bibs?apikey=' + bibapi + '&limit=100&offset=' + str(offset), headers=headers).json()
    dumpToPython = json.dumps(data)
    #dumpToPython
    dict_json=json.loads(dumpToPython)
    for _bib in dict_json["bib"]: 
        delmmsid.append(_bib["mms_id"])

#Remove anything that was already in the collection from the colection
for i in range(len(delmmsid)):
    tempid = (delmmsid[i]) 
    #Delete each MMS ID that was already there from collection
    x = requests.delete(alma_base+ '/bibs/collections/' +newpid + '/bibs/' + tempid + '?apikey=' + bibapi)
print('Old titles removed')

#Grab reports from Analytics API (to retrieve the MMS IDs that currently meet the report filters)
#Enter your Analytics API key (enclosed in single quotes) here:
analyticsapi = 'YOUR-ANALYTICS-API-KEY-HERE'
headersxml = {"Accept": "application/xml"}

#Path to Newly-Received Physical Items report
#You will have to change this path to the right one for your Analytics data. Instructions are (kind of) here: https://developers.exlibrisgroup.com/blog/working-with-analytics-rest-apis/
#(Just know that it does want actual spaces and not URL-encoded spaces like shown in the example)

reportpath = "/shared/.../Newly-Received Physical Items"

#Makes request to pull from the first report
#Default limit is 25, number must be a multiple of 25
r = requests.get(alma_base+'/analytics/reports?path=' + reportpath + '&limit=150&col_names=false&apikey=' + analyticsapi, headers=headersxml)
r.raise_for_status
xml = r.content

#Parse returned XML data with Beautiful Soup 
soup = BeautifulSoup(r.content, "xml")
print('New print books grabbed')

#Find the MMS IDs in the report output and append them to an empty list
#For my report I know that column is called 'Column1', but if you're getting weird information you may have to do some additional testing to see which column is the column with your MMS IDs
rawmms = soup.find_all('Column1')
data = []
for i in range(0,len(rawmms)):
    rows = [rawmms[i].get_text()]
    data.append(rows)

#Now again for the Ebooks, same deal as above with the path to the report
#Path to Newly-Received Ebooks report
ebookreportpath = "/shared/.../Newly-Received Ebooks"

#Now go through ebook report
rebook = requests.get(alma_base+'/analytics/reports?path=' + ebookreportpath + '&limit=150&col_names=false&apikey=' + analyticsapi, headers=headersxml)
rebook.raise_for_status
xmlmore = rebook.content
moresoup = BeautifulSoup(rebook.content, "xml")
print('New ebooks grabbed')

#Find the MMS IDs in the ebook report output (which in my report I know is 'Column1')
rawemms = moresoup.find_all('Column1')
for i in range(0,len(rawemms)):
    rows = [rawemms[i].get_text()]
    data.append(rows)


#Make a dataframe of just the MMS IDs collected from the report calls to feed into the POST request
df = pd.DataFrame(data,columns = ['MMS Id'])
df.head()
MMSIDs = df['MMS Id']

#Adds items to collection based on MMSIDs in previous step
#Feel free to adjust the Request body as needed
for i, mms in enumerate(MMSIDs, 0):
    mms = MMSIDs[i]    
    requestbody = {
        "link": "",
        "mms_id": mms,
        "record_format": "marc21",
        "suppress_from_publishing": "false",
        "suppress_from_external_search": "false",
        "suppress_from_metadoor": "false",
        "sync_with_oclc": "BIBS",
        "sync_with_libraries_australia": "NONE",
        "cataloging_level": {
         "value": "00"
         },
        "brief_level": {
            "value": "01"
        }
    }
    
    #The request to post each of the MMS IDs gathered from the reports to the initially-specified collection in Alma
    r = requests.post(url=alma_base+'/bibs/collections/'+newpid+'/bibs?apikey='+bibapi, headers=headers, json=requestbody).json()
print (str(len(MMSIDs)) + ' items added to collection')

#Done~!

