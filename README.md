# Google Maps Amsterdam restaurants analysis
In this project, I scraped details of Amsterdam restaurants from Google Maps using Selenium and analyzed the data. 

Who is this analysis for ?
- Tourists, those who travel to Amsterdam and those who live in Amsterdam can use this analysis to find the best restaurants.
- Those who are looking to start a business in the restaurant industry and provide services in Amsterdam

I used Google Maps to get data about restaurants in Amsterdam. Unfortunately, it is not possible for those who live in Iran to access Google APIs :( But this is not the end of the work, I was able to create two robots using Selenium and scrape the Google maps data. The first bot [Google_maps_scraper.py](https://github.com/meysamraz/Google-Maps-Amsterdam-restaurants-analysis/blob/master/Google_maps_scraper.py) is from the Google Map site for scraping. It uses and is able to scrape restaurant reviews and the second bot [Google_scraper.py](https://github.com/meysamraz/Google-Maps-Amsterdam-restaurants-analysis/blob/master/Google_scraper.py) uses Google to collect data. 

![alt Text](https://github.com/meysamraz/Google-Maps-Amsterdam-restaurants-analysis/blob/master/src/demo_scraper1.gif)![alt Text](https://github.com/meysamraz/Google-Maps-Amsterdam-restaurants-analysis/blob/master/src/demo_scraper2.gif)



# Project Overview :
- ### 1 - Scraping data from Google maps
    - title : name of restaurant
    - rating : google maps rating (star 0-5) of restaurant
    - reviews : number of reviews of the restaurant
    - expense : price range of the restaurant ($ - econony, $$ - regular, $$$  - expensive, $$$ - luxury)
    - category : what type of food does restaurant serve (Italian - french or etc.)
    - description : restaurant description in Google maps
    - services : What kind of services does the restaurant offer? (die-in,takeaway...)
    - address : The registered address of the restaurant in Google Map

- ### 2 - Cleaning the data
    - Convert ratings to number
    - Remove K and convert number of reveiws to int
    - Remove "Service options:" from services
- ### 3 - Analyzing Data
    - The Number of scrapped restaurants
    - Min - Meam - Max of Restaurats Rating
    - Rating vs Reviews
    - Rating Distribution
    - Removing outliers and perform analysis
    - Min - Meam - Max of Restaurats Number of Reviews
    - How many restaurants have takeaway?
    - How many restaurants have dine-in?
    - How many restaurants have both dine-in and takeaway?
    - Restaurant with most reviews
    - Restaurant with lowest rating
    - Restaurant with highest rating and No. reviews
    - What categories most restaurants are from?
    - Number of closed Restaurants
    - In what category are the restaurants in terms of price?
    - Restaurant with highest rate in each category
    - Reviews Word Cloud
- ### 4 - Get latitude and longitude based on the addresses
    - Which area of Amsterdam has the most restaurants?
    - Where are most luxury restaurants located ?
