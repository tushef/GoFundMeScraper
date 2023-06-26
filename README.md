# GoFundMeScraper
Collecting data on Go Fund Me Fundraisers. THe data can be used for Sentiment Analysis, Marketing Analysis and potentially identifying current problems in modern Medicine which cause unaffordable treatments

o Using selenium for automated bot tasks, BeautifulSoup 4 for scraping and pandas for data manipulation

o Using the time library for optimization of automated operations, because improper web loadings could cause errors during seleniums and BS4 operations

o It scrapes first hand (general) data for the first 500 Fundraisers. It uses selenium to switch pages in order to load more entries.

o It scrapes second hand (specific/missing) data for Fundraisers such as nr. of donations, description text, nr. of comments, nr. of updates etc.

o Using SQLite to store the data and later conduct tests/research upon it
