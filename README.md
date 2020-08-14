# web-scraping-challenge

## Part 1
#### Summary
**Initial scraping** of NASA Mars News site for latest article title and summary, JPL Mars Space Images site for featured image url, Mars Weather twitter account for latest weather tweet, Mars Facts webpage for the table containg facts about the planet, and USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres using **Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter**.
### How to Run
Run the file _"mission_to_mars.ipynb"_ in **Mission_to_Mars** folder to view initial scrape
## Part 2
#### Summary
**Creating a _"new "_ HTML page** that displays all of the information that was scraped from the URLs above by using **MongoDB with Flask templating**.
### How to Run
Run the file _"app.py"_ in **Mission_to_Mars** folder to view HTML page with scraped data
* Note: The only purpose of  _"scrape_mars.py"_ is to hold the `scrape()` function
