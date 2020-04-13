from operator import index

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import requests
import urllib.request
import time
import pandas as pd
import re

from openpyxl import load_workbook


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def get_ctric_reviews(url):
    response = requests.get(url)

    crtc_review = []
    print(url)
    soup = BeautifulSoup(response.text, "html.parser")
    page_no = soup.findAll('span', attrs={'class': 'pageInfo'})
    tes = 0
    if len(page_no) != 0:
        tes = 0
        num = int(page_no[0].text[-2:])
        while (num != 0):
            # print(num)
            print(len(crtc_review))
            response = requests.get(url + url_back_critics_page + str(num))
            if response.status_code == 200:
                c_reviews = soup.findAll('div', attrs={'class': 'the_review'})
                num -= 1

                if len(c_reviews) != 0:
                    for reviews in c_reviews:
                        tes += 1
                        crtc_review.append(
                            reviews.text.replace('                                   ', '').replace('\n', '').replace(
                                '\n', '').replace('                                ', ''))
    # print('total reviews for '+url+str(len(crtc_review)))#
    return crtc_review


def get_user_reviews(url):
    ur_review = []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    # audience reviews
    audience_reviews = soup.findAll('p', attrs={
        'class': 'audience-reviews__review--mobile js-review-text clamp clamp-4 js-clamp'})
    if len(audience_reviews) != 0:
        for reviews in audience_reviews:
            # print(reviews.text)
            ur_review.append(reviews.text)
    return ur_review

def write_to_file(filename,movie_title,dataframe):
    writer = pd.ExcelWriter(filename, engine='openpyxl')
    writer.book = load_workbook(filename)
    writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
    reader = pd.read_excel(r''+filename+'')
    dataframe.to_excel(writer, movie_title, index=False, header=False, startrow=len(reader) + 1,)
    writer.close()

urls=['https://www.rottentomatoes.com/m/spotlight_2015/reviews','https://www.rottentomatoes.com/m/gravity_2013/reviews','https://www.rottentomatoes.com/m/moonlight_2016/reviews']


print(len(urls))


url_back_critics_page = '?type=&sort=&page='
url_aud_review_page='?type=user'
title = ''
print('started')
for url in urls:
    print(url)
    driver = webdriver.Chrome('E:\MySoftwares\chromedriver')
    driver.get(url+url_aud_review_page)
    driver.implicitly_wait(5)



    soup = BeautifulSoup(driver.page_source, "html.parser")
    titles = soup.find_all('a', attrs={'class': 'unstyled articleLink', 'target': '_top'})
    for t in titles:
        title = t.text
    title=title.strip()
    print("title"+title)


    # cdf = pd.DataFrame()

    # clist=get_ctric_reviews(url)
    # cdf['critiquereview']=clist

    # write_to_file('Creview.xlsx',title,cdf)

    button_click = driver.find_elements_by_xpath('//*[@id="content"]/div/div/nav[3]/button[2]')[0]
    com_data = []

    while (check_exists_by_xpath('//*[@id="content"]/div/div/nav[3]/button[2]')):
        com_data.append(get_user_reviews(driver))
        try:
            button_click.click()
            driver.implicitly_wait(4)
        except ElementNotInteractableException:
            print(len(com_data))
            print(com_data)
            break
    user_reviews = []
    for lists in com_data:
        for elements in lists:
            if elements not in user_reviews:
                user_reviews.append(elements)
    print(len(user_reviews))


    df = pd.DataFrame()
    df['UserReviews'] = user_reviews

    print(df)
    # MyFile = open(title+'.txt', 'w',encoding="utf-8")
    import io

    with io.open(title, "wt", encoding="utf-8") as f:
        f.write('\n'.join(str(line) for line in user_reviews))
    # for element in user_reviews:
    #     MyFile.write(element)
    #     MyFile.write('\n')
    # MyFile.close()


    # write_to_file('review.xlsx',title,df)
    driver.close()

