# GDPR-OSS-Impact
Scripts to collect the GDPR data on Github &amp; Data files and data analysis to understand the impact of the General Data Protection Regulation on Open-Source Software Development

## Description of the folder contents with paper sections:

**survey** (*Data Source 1: Developer Survey* (3.2.2) in Methodology section)
1. This directory contains a copy of the survey (`survey.pdf`) distributed to OSS developers to further discover their perceptions of GDPR implementation.

**data_collection_scripts** (*Data Source 2: GDPR PRs on GitHub* (3.3.1) in the Methodology section)
1. The ``gdpr_github.py`` file is used to collect  body, commit message, review, and comment of the GDPR and non GDPR pull requests based on the PR's urls
2. The ``github_search_json_to_csv.py`` file is used to collect GDPR and non-GDPR related Github pull requests' information: including url, title, merged, closed, etc.
3. The ``sentiment_analysis.py`` file is used to preprocess the raw data and run the sentiment analysis on the cleaned data

**original_data_files** (*GDPR and non-GDPR PRs* (3.3.1) in Methodology section)
1. The ``all_gdpr_data.csv`` file contains all GDPR-related pull request infomation: including url, title, created_at, updated_at, commits, closed, open, etc.
2. The ``all_non_gdpr_data.csv`` file contains all non-GDPR-related pull request infomation: including url, title, created_at, updated_at, commits, closed, open, etc.

**sentiment_analysis** (*Measuring Developer Perception* in the Data Analysis sub-section (3.3.3) of the Methodology section)
1. The ``sentiment_combined.xlsx`` file contains the sentiment analysis results of title, body, comment, review, and commit messages for GDPR and non-GDPR PRs, along with t-test results for the three sentiment analysis models (Liu-Hu, VADER, and SentiArt). 
