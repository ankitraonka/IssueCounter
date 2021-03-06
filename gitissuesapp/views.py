from django.shortcuts import render
from django.shortcuts import render
import requests	 #return reponse object created through url
import json	 #For loading json data
import datetime  #Used for dealing with date

#-----------Global Variable------------------#

base_url = ""
date_before_1=""
date_before_7=""

#issues including all issues including pull_requests
total_issues=0 
total_issues_1=0 #in last 24 hrs
total_issues_7=0 #in betweern last 24 hrs and last 7 days
total_issues_before_7=0 #all issues excluding last 7 days

#pull requests
total_pulls=0
total_pulls_1=0 #in last 24 hrs
total_pulls_7=0 #in betweern last 24 hrs and last 7 days
total_pulls_before_7=0 #all issues excluding last 7 days


#-----------------------------------------------#



def convertToStr(x):
    return str(x)

###############################################################################################################################
#   following code gives total count of issue including pull_requests				               		      #
#   "since" filter is used to get all the issues after a particular time                                                      #
#   but since only 100 issues can be shown in a single page, we have to count total by going to every single page             #
#   we enquire every page untill a page's count is less then 100                                                              #
###############################################################################################################################
def getTotalIssues():
    global total_issues_1
    global total_issues_7
    global total_issues_before_7
    global total_pulls_1
    global total_pulls_7

    count=100  #initialised with 100 so that it runs atleast once
    page=0
    complete=False
    while count==100:
        page+=1
        query_url=base_url+"/issues?&page="+convertToStr(page)+"&per_page=100"
        response=requests.get(query_url)
        content=json.loads(response.content or response.text)      
	count=len(content)
	while complete==False:
            for issue in content:
                time=issue["created_at"]
                if time>date_before_1:
                    total_issues_1+=1
		    if issue.has_key('pull_request'):
			total_pulls_1+=1
                elif time>date_before_7:
                    total_issues_7+=1
		    if issue.has_key('pull_request'):
			total_pulls_7+=1
                else:
		#once true it means we have checked every pull created in last 7 days and hence we dont need to
		#check each pull now and juz need to count pulls in each rendered page
                    complete=True  
                    break
    print total_issues_1
    #we have total issues and we have total no. of issues in last 7 days from this we can get total issues created excluding last 7 days 
    total_issues_before_7 = total_issues - total_issues_1 - total_issues_7

    return     


###############################################################################################################################
#   following code gives total pull_requests				               		      			      #
#   while using pulls filter, "since" filter is not available and therefore we have to check every pull request               #
#   via it's "created_at" to see if it lies within the given time period and we update the global variables manually          #
###############################################################################################################################
def getPullCount():
    global total_pulls
    global total_pulls_before_7
    
    page=0
    count=100
    complete=False   #denotes that we have chked all pull created in the past 7 days
    while count==100:
        page+=1
        query_url=base_url+"/pulls?page="+convertToStr(page)+"&per_page=100"
        response=requests.get(query_url)
        content=json.loads(response.content or response.text)
        count=len(content)
        total_pulls+=count
        
    total_pulls_before_7 = total_pulls - total_pulls_7 - total_pulls_1
    
    return
        
def main(request):
	#print "got_in"
	if request.POST:
	#	print "in_post"	    
		input_url=str(request.POST.get('url'))
		arr=map(str,input_url.split("/"))
		if arr[1]=="":
			user=arr[3]
			repo=arr[4]
		else:
			user=arr[1]
			repo=arr[2]
		global base_url		
		base_url="https://api.github.com/repos/"+user+"/"+repo   
		
		response=requests.get(base_url)
    		repo_detail=json.loads(response.content or response.text)

		if repo_detail.has_key("message"):
			issues={}
			issues['message']=repo_detail['message']
			issues["user"]="-"
			issues["repo"]="-"
			issues["total"]="-"
			issues["within1"]="-"
			issues["within7"]="-"
			issues["before7"]="-"
			return render(request,"index.html",issues)

		global total_issues		
		total_issues=repo_detail["open_issues"]  #gives total issues open_issues+pull_request

		global date_before_1
		global date_before_7

		date_before_1=(datetime.datetime.now()-datetime.timedelta(hours=24)).isoformat()
		date_before_7=(datetime.datetime.now()-datetime.timedelta(hours=24*7)).isoformat()


		getTotalIssues()
		getPullCount()

		total_open = total_issues - total_pulls
		total_open_1 = total_issues_1 - total_pulls_1
		total_open_7 = total_issues_7 - total_pulls_7
		total_open_before_7 = total_issues_before_7 - total_pulls_before_7

		issues={}
		issues['message']="Successful"
		issues["user"]=user
		issues["repo"]=repo
		issues["total"]=total_open
		issues["within1"]=total_open_1
		issues["within7"]=total_open_7
		issues["before7"]=total_open_before_7
		#print "Total open :",total_open
		#print "Total open in 24 hrs:",total_open_1
		#print "Total open in  1-6:",total_open_7
		#print "Total open in 7-infi:",total_open_before_7
		return render(request,"index.html",issues)
	else:
		print "in_else"
		issues={}
		issues['message']="None"
		issues["user"]="-"
		issues["repo"]="-"
		issues["total"]="-"
		issues["within1"]="-"
		issues["within7"]="-"
		issues["before7"]="-"
		return render(request,"index.html",issues)

	#print "Total open :",total_open
	#print "Total open in 24 hrs:",total_open_1
	#print "Total open in  1-6:",total_open_7
	#print "Total open in 7-infi:",total_open_before_7
