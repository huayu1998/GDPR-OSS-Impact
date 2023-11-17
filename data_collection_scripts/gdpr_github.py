# Packages imported
from github import Github
from github import Auth
import pandas as pd

"""
PullRequest.body to get the main body of a PR
PullRequest.title to get the body title of a PR
PullRequest.get_reviews().body in pullRequestReview object to get the PR reviews (note)
PullRequest.get_comments()/get_review_comments().body in pullRequestComment object to get the PR review comments
PullRequest.get_commits().commit.message in git.commit object to get commit message
"""

### Helper functions
def getFullNamePullNum(url):
    items = url.split('/')
    fullName = items[4]+'/'+items[5]
    pullNum = int(items[7])
    return fullName,pullNum

def getData(urls,df,nameOfcsv):
    firstIndex = 0
    startIndex = 0
    endIndex = 998
    lastIndex = 998 # ends of last index of urls list
    count = 0
    prBot = []
    prBody = []
    prCommitMessage = []
    prReviews = []
    prComments = []
    # Pre-add the empty value
    for temp in range(firstIndex, startIndex):
        print(temp)
        prBot.append(None)
        prBody.append(None)
        prCommitMessage.append(None)
        prReviews.append(None)
        prComments.append(None)

    for index in range(startIndex, endIndex):
        pr_url = urls[index]
        print(index,pr_url)
        fullName, pullNum = getFullNamePullNum(pr_url)
        try:
            # Access the repo and pr
            repo = gh.get_repo(fullName)
            pr = repo.get_pull(pullNum)

            response = urlopen(pr_url)
            pr_data = json.loads(response.read())
            # Get bot part
            aBot = 'bot' in pr.user.login or pr_data['user']['type'].lower() == 'bot'
            if aBot:
                prBot.append(1)
            else:
                prBot.append(0)
            
            # Get body part
            prBody.append(pr.body)

            # Get commit message part
            commitList = pr.get_commits()
            resultCommit = ''
            for item in commitList:
                resultCommit = resultCommit + item.commit.message +'\n\n'
            prCommitMessage.append(resultCommit)

            # Get review part
            reviewsList = pr.get_reviews()
            resultReview = ''
            for item in reviewsList:
                if item.body:
                    resultReview = resultReview + item.body +'\n\n'
            prReviews.append(resultReview)

            # Get comments part
            commentList = pr.get_comments()
            resultComment = ''
            for item in commentList:
                resultComment = resultComment + item.body +'\n\n'
            prComments.append(resultComment)

        except Exception:
            prBot.append(None)
            prBody.append(None)
            prCommitMessage.append(None)
            prReviews.append(None)
            prComments.append(None)

        # Update the count
        count += 1
    
    # Post-add the empty value
    for temp in range(endIndex, lastIndex):
        print(temp)
        prBot.append(None)
        prBody.append(None)
        prCommitMessage.append(None)
        prReviews.append(None)
        prComments.append(None)

    # Ends loop & update the dataframe    
    df['bot'] = prBot # 12228 out of 12227
    df['body'] = prBody
    df['commits'] = prCommitMessage
    df['reviews'] = prReviews # 12226 out of 12227
    df['comments'] = prComments
    print("Success ends & Count",count)
    df.to_csv(nameOfcsv, index=False)

# Variables and PyGithub object using Auth Access Token set up
accessToken = '[redacted]'
auth = Auth.Token(accessToken)
gh = Github(auth=auth)
nameOfInputFile = 'update_new_gdpr_data.csv'
nameOfOutputFile = 'all_gdpr_data.csv'

# Read new_gdpr_data.csv file and get github API url links
df = pd.read_csv(nameOfInputFile)
df = df.dropna(subset=['url'])
df = df.reset_index(drop=False)
urls = df["url"]

# Get all data from the pull requests
getData(urls,df,nameOfOutputFile)

print('Rate limit/hour:',gh.get_rate_limit().core.limit) # Rate limit per hour
print('Rate used:',gh.get_rate_limit().core.limit - gh.rate_limiting[0]) # Rate used
print('Rate remaining:',gh.get_rate_limit().core.remaining) # Rate remaining
print('Rate reset time:',gh.get_rate_limit().core.reset) # Rate reset time
# Unix timestamp indicating when rate limiting will reset
print('Rate reset time in Unix timestamp:',gh.rate_limiting_resettime)

"""
Add all the data parts into one
"""
df = pd.read_csv(nameOfOutputFile)
bot = df['bot']
body = df['body']
commits = df['commits']
reviews = df['reviews']
comments = df['comments']

body_not_bot = []
commits_not_bot = []
reviews_not_bot = []
comments_not_bot = []

for index in range(bot.size):
    if bot[index] == 0:
        body_not_bot.append(body[index])
        commits_not_bot.append(commits[index])
        reviews_not_bot.append(reviews[index])
        comments_not_bot.append(comments[index])
    else:
        body_not_bot.append(None)
        commits_not_bot.append(None)
        reviews_not_bot.append(None)
        comments_not_bot.append(None)

df['body_not_bot'] = body_not_bot
df['commits_not_bot'] = commits_not_bot
df['reviews_not_bot'] = reviews_not_bot
df['comments_not_bot'] = comments_not_bot
print(len(body_not_bot),len(commits_not_bot),len(reviews_not_bot),len(comments_not_bot))

df.to_csv('non_bot_gdpr_data.csv', index=False)