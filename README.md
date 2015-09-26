IssueCounter (Implemented in Python using Django)

application live at: http://git-issue-counter.herokuapp.com/

Problem Statement

Create a repository on GitHub and write a program in any programming language that will do the following: 

Input : User can input a link to any public GitHub repository

Scope of improverment:

Given more time 
The time complexity of this app can be improved by studying about various filters available in the github api

Solution Approach:

We can get total issue count ie open issues+pull requests from
www.api.github.com/repos/"username"/"repository_name"

now we have to get total number of issues opened in last 24 hrs and between 24hrs and last 7 days
we get details of each issue through
www.api.github.com/repos/"username"/"repository_name"/issues

but this gives only 30 issues per page by default
therefore we traverse each page till we get issue that are out of our required time range
if any issue is a pull request then we update the concerned variable 
we use:
www.api.github.com/repos/"username"/"repository_name"/issues?page="page_no"&per_page=100

form above we get total issues
total issues in previous 24 hrs
total pulls in previous 24 hrs
total issues in between 24 hrs & last 7 days
total pulls in between 24 hrs & last 7 days


for getting total pull request 
we use
www.api.github.com/repos/"username"/"repository_name"/pull?page="page_no"&per_page=100

we traverse each page and count the total number of pull request in it
if count is less than 100 then we are on the last page

from above we get total pull request

from this we can answer all queries

ex:
total open issues= total issue-total pull requests



