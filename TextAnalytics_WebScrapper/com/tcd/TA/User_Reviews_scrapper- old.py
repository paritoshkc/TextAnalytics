from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

driver = webdriver.Chrome('E:\MySoftwares\chromedriver')
driver.get("https://www.rottentomatoes.com/m/bloodshot_2020/reviews?type=user")
driver.implicitly_wait(5)

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
def get_user_reviews(url):

    ur_review=[]

    print(driver)

    soup = BeautifulSoup(driver.page_source, "html.parser")
 # audience reviews
    audience_reviews=soup.findAll('p', attrs={'class': 'audience-reviews__review--mobile js-review-text clamp clamp-4 js-clamp'})
    if len(audience_reviews)!=0 :
        for reviews in audience_reviews:
      # print(reviews.text)
         ur_review.append(reviews.text)
    return ur_review

button_click=driver.find_elements_by_xpath('//*[@id="content"]/div/div/nav[3]/button[2]')[0]
com_data=[]
while(check_exists_by_xpath('//*[@id="content"]/div/div/nav[3]/button[2]')):
    com_data.append(get_user_reviews(driver))
    try:
       button_click.click()
       driver.implicitly_wait(4)
    except ElementNotInteractableException:
        print(len(com_data))
        print(com_data)
        break
user_reviews=[]
for lists in com_data:
    for elements in lists:
        if elements not in user_reviews:
            user_reviews.append(elements)
print(len(user_reviews))
#content > div > div > nav:nth-child(4) > button.js-prev-next-paging-next.btn.prev-next-paging__button.prev-next-paging__button-right


