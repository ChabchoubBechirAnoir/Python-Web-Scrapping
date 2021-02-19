from selenium import webdriver
import time
def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):

    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        
        for img in thumbnail_results[results_start:number_results]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls    
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                return image_urls
        else:
            return
        results_start = len(thumbnail_results)

    return image_urls

import pandas as pd
if __name__ == '__main__':
    driver = webdriver.Chrome()
    
    df= pd.read_csv("perfectproducts.csv")
    df = df.head(1000)
    data = df['product_name']
    result = []
    i = 0
    for name in data :
        link = fetch_image_urls(name,1,driver)
        if (link == None or len(link) == 0):
            result.append("")
            continue
        link = next(iter(link))
        result.append(link)
        i = i + 1 
        if(i % 100 == 0):
            print(i/len(data))
    df['link']= result 
    df.to_csv("goodproducts.csv")        


    print(df.head())