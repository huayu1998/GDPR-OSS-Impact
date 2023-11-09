# GDPR-OSS-Impact
Scripts to collect the GDPR data on Github &amp; Data files and data analysis to understand the impact of the General Data Protection Regulation on Open-Source Software Development

## Description of the folder contents with paper sections:

**data_collection_scripts** (*Data Collection* (3.1.1) &amp; *Data Processing* (3.1.2) in the Methodology section)
1. The ``gdpr_github.py`` file is used to collect  body, commit message, review, and comment of the GDPR and non GDPR pull requests based on the PR's urls
2. The ``github_search_json_to_csv.py`` file is used to collect GDPR and non-GDPR related Github pull requests' information: including url, title, merged, closed, etc.
3. The ``keywords_analysis.py`` file is used to run the keywords extraction and word cloud on the preprocessed data after sentiment analysis
4. The ``sentiment_analysis.py`` file is used to preprocess the raw data and run the sentiment analysis on the cleaned data

**keywords_analysis** (*Measuring Developer Perception* in the Data Analysis sub-section (3.1.3) of the Methodology section)
1. It contains the keywords extraction &amp; word cloud results of title, body, comment, review, and commit message for both GDPR and non-GDPR PRs.  

**original_data_files** (*Data Collection* (3.1.1) in Methodology section)
1. The ``new_gdpr_data.csv`` file contains GDPR-related pull request infomation: including url, title, created_at, updated_at, commits, closed, open, etc.
2. ``new_non_gdpr_data.csv`` contains non-GDPR-related pull request infomation: including url, title, created_at, updated_at, commits, closed, open, etc.

**sentiment_analysis** (*Measuring Developer Perception* in the Data Analysis sub-section (3.1.3) of the Methodology section)
1. This directory contains the sentiment analysis results of title, body, comment, review, and commit message for both GDPR and non-GDPR PRs. 

**survey** (*Survey Design* (3.2.2) in Methodology section)
1. This directory contains a copy of the survey (``survey.pdf'') distributed to OSS developers to further discover their perceptions of GDPR implementation.
