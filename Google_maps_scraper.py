from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pandas as pd
import time

def get_restaurants(chromedriver_path,city_restaurant_url,getting_comments=True):
    """Scraping Google Maps restaurants thier reviews using Selenium. By running it will scrape 
       restaurants (title, stars, reviews, type, address, currency, url) thier comments and rating

    Args:
        chromedriver_path: path of your chromedriver (make sure you have latest version)
        city_restaurant_url: url of desire city restaurants on Google Maps
        getting_comments: by making this Ture or False you will determine whether comments be scraped or not

    Returns:
        restaurants_details dataframe and restaurants_comments dataframe
    """
    urls=[]
    details_list = []
    comments_list = []
    
    df_comments = pd.read_csv('comments.csv')
    df_details = pd.read_csv('detail.csv')
    
    # Setup Chrome drives
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=chromedriver_path,options=options)

    # Start Scraping
    driver.get(city_restaurant_url)

    time.sleep(3)
    print('Start scraping')

    # Scrolling down (handling infinite scrolling)
    scrollView = driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')
    while True:
        scrollView.send_keys(Keys.PAGE_DOWN)
        scrollView.send_keys(Keys.PAGE_DOWN)
        scrollView.send_keys(Keys.PAGE_DOWN)    
        time.sleep(1)
        scrollView.send_keys(Keys.PAGE_UP)
        time.sleep(1)
        try:
            # Get url of restaurants
            if driver.find_element_by_class_name("HlvSq"):
                for a in driver.find_elements_by_xpath('/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div/div/a'):
                    url = a.get_attribute('href')
                    url_dict = {"url":url}
                    urls.append(url_dict)
                df_urls = pd.DataFrame(urls)
                print("Available Restaurants: ",len(df_urls))
                break
        except:
            pass

    print('Start getting page details')
    
    # Start scraping Restaurants details
    for url in df_urls['url'].to_list():
        driver.get(url)
        try:
            stars = driver.find_element_by_xpath('/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[1]/span/span[1]').text
        except:
            stars = 0.0   
        try:
            reviews = driver.find_element_by_xpath('/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span').text
        except:
            reviews = "0 Reviews"  
            
        title = driver.find_element_by_xpath('/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[2]').text
        restaurant_type = driver.find_element_by_xpath('/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/span[1]/span[1]/button').text
        address = driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div[3]/button/div[1]/div[2]/div[1]').text
        try:    
            currency = driver.find_element_by_xpath('/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span/span[2]/span[1]/span').text
        except:
            currency = "Unclear"
            
        detail_dict = {"title":title,"stars":stars,"reviews":reviews,"type":restaurant_type,"address":address,"expense":currency,"url":url}
        details_list.append(detail_dict)
        df_detail = pd.DataFrame(details_list)
        df_details_final = df_details.append(df_detail)   
        print(df_details_final.shape)
        time.sleep(3)
        if getting_comments == True:
            time.sleep(2)
            
            # Finding More reviews (all reviews) button
            element = driver.find_element_by_xpath('/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]')
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            
            # Click on More reviews button
            driver.find_element_by_xpath('//button[contains(@aria-label, "More reviews")]').click()
            
            time.sleep(3)
            
            # Scrolling down (handling infinite scrolling for comments) for 120 second
            scrollView2 = driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
            time.sleep(3)
            timeout = time.time() + 110
            
            while True:
                if time.time() > timeout:
                    break
                    time.sleep(3)
                else:
                    scrollView2.send_keys(Keys.PAGE_DOWN)
                    scrollView2.send_keys(Keys.PAGE_DOWN)
                    scrollView2.send_keys(Keys.PAGE_DOWN)    
                    time.sleep(1)
                    scrollView2.send_keys(Keys.PAGE_UP)
                

            # Find comments and thier rates
            comments = driver.find_elements_by_class_name('wiI7pd')
            stars = driver.find_elements_by_class_name('kvMYJc')

            for comment,star in zip(comments, stars):
                comments_dict = {"title":title,"comment":comment.text,"stars":star.get_attribute("aria-label")}
                comments_list.append(comments_dict)
                df2 = pd.DataFrame(comments_list)
                df_comments_final = df_comments.append(df2)
            print(df_comments_final.shape)

    # If getting_comments were ture return both dataframes if not just returen df details
    if getting_comments == True:
        return df_details_final,df_comments_final
    else:
        return df_details_final
    driver.quit()



df_details_final = get_restaurants('chromedriver.exe',"https://www.google.com/maps/search/Restaurants/@52.3730777,4.74684,10z/data=!4m2!2m1!6e5",getting_comments=False)

df_details_final.to_csv('Amsterdam_restaurants.csv',index=False)


# df_details_final,df_comments_final = get_restaurants('chromedriver.exe',"https://www.google.com/maps/search/Restaurants/@52.3730777,4.74684,10z/data=!4m2!2m1!6e5",getting_comments=True)

# df_details_final.to_csv('Amsterdam_restaurants.csv',index=False)
# df_details_final.to_csv('Amsterdam_restaurants_comments.csv',index=False)
