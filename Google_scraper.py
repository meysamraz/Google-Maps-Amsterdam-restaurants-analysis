from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pandas as pd
import time



def get_restaurants(chromedriver_path,city_restaurant):
    """Scraping Google Maps restaurants thier reviews using Selenium. By running it will search 
       on google and open resturants and start scraping restaurants (title, rating, reviews, expense,category, description, services, address)


    Args:
        chromedriver_path: path of your chromedriver (make sure you have latest version)
        city_restaurant: name of the city + restaurants

    Returns:
        restaurants_details dataframe
    """
    

    # Setup Chrome drives
    options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--lang=en")
    driver = webdriver.Chrome(executable_path=chromedriver_path,options=options)
    details_list = []


    # Navigate to Google
    driver.get('https://www.google.com')

    # Search city + restaurant 
    search_box = driver.find_element_by_name('q')
    search_box.send_keys(city_restaurant)
    search_box.send_keys(Keys.RETURN)
    restaurants_list = []
    time.sleep(1)

    # Click on more (Navigate to Google maps)
    driver.find_element_by_css_selector('span.Z4Cazf.OSrXXb').click()
    driver.maximize_window()
    time.sleep(1)
    while True:
        time.sleep(5)
        for a in driver.find_elements_by_css_selector('a.vwVdIc.wzN8Ac.rllt__link.a-no-hover-decoration'):
            a.click()
            time.sleep(2)
            try:
                title = driver.find_element_by_xpath('/html/body/div[6]/div/div[9]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/div/h2/span').text
            except:
                title = 'No title'
            try:
                rating = driver.find_element_by_xpath('/html/body/div[6]/div/div[9]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div/div/span/span[1]').text
            except:
                rating = "0,0"
            try: 
                reviews = driver.find_element_by_xpath('/html/body/div[6]/div/div[9]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div/div/span/span[3]').text
            except:
                reviews = "(0)"
            try:
                expense = driver.find_element_by_xpath('/html/body/div[6]/div/div[9]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[2]/div[2]/div/span[1]/span').text
            except:
                expense = "Unclear"    
            try:
                category = ""
                for elem in driver.find_elements_by_xpath('/html/body/div[6]/div/div[9]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[2]/div[2]/div/span'):
                    category = elem.text
            except:
                    category = "Unclear"
            try:
                description = driver.find_element_by_xpath('/html/body/div[6]/div/div[9]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[5]/g-flippy-carousel/div/div/ol/li[1]/span/div/div/div/div[1]/div/div/c-wiz/div/div/div/span').text
            except:
                description = "No description"
            try:
                services = driver.find_element_by_xpath('/html/body/div[6]/div/div[9]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[5]/g-flippy-carousel/div/div/ol/li[1]/span/div/div/div/div[1]/c-wiz/div').text
            except :
                    try:
                        services = driver.find_element_by_xpath('/html/body/div[6]/div/div[9]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[5]/g-flippy-carousel/div/div/ol/li[1]/span/div/div/div/div[2]/c-wiz/div').text
                    except :
                            services = "Unclear"
            try:
                services = driver.find_element_by_xpath('/html/body/div[6]/div/div[9]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[5]/g-flippy-carousel/div/div/ol/li[1]/span/div/div/div/div[1]/c-wiz/div').text
                
            except:
                try:
                    services = driver.find_element_by_xpath('/html/body/div[6]/div/div[9]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[5]/g-flippy-carousel/div/div/ol/li[1]/span/div/div/div/div[2]/c-wiz/div').text
                except :
                    services = "Unclear"
            try:
                address =  driver.find_element_by_css_selector('span.LrzXr').text
            except:
                address = None
                
            time.sleep(1)
            restaurants_dict = {"title":title,"rating":rating,"reviews":reviews,"expense":expense,"category":category,"description":description,"services":services,"address":address}
            details_list.append(restaurants_dict)
            df = pd.DataFrame(details_list)
            print(df)
        # find next if there was no next button done scraping
        try:
        
            driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]').click()
            time.sleep(2)
        except:
            break
        
    return df


df_restaurants = get_restaurants('chromedriver.exe',"amsterdam restaurants")
df_restaurants.to_csv('Amsterdam_restaurants.csv',index=False)