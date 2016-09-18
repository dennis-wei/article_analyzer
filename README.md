# Article Analyzer

This application regularly scrapes various sources for political news articles and vectorizes them based on a bag-of-words model that accounts for both standard English and recent topics. Then, the user can submit a link to an article, and the app will search through its database for similar articles and relay them to the user.

### Running the Application

`pip install requirements.txt`

Setup settings.py to a Postgresql database. Schema can be found in models.models

`python app.py`


### Current State

At the moment, the application only supports the New York Times, and it will only successfully scrape if done locally with Cookies corresponding to a NYT account online.

### Future

Newspaper API usage to more easily collect article data without having to worry too much about navigating paywalls/bot blocks.

Entity analysis API to compare bias between articles and sources
