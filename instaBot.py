from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import wget


class InstagramBot1:
    def __init__(self):
        self.followers = []
        self.following = []
        self.driver = webdriver.Chrome("C:\\Users\\Anand\\chromedriver.exe")

    def login(self, user, pw):
        driver = self.driver
        driver.get('https://www.instagram.com/')
        try:
            username = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input[name='username']"))
            )
            username.clear()
            username.send_keys(user)
            password = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input[name='password']"))
            )
            password.clear()
            password.send_keys(pw)

            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[type='submit']"))
            )
            submit_button.click()

            save_info = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'Save Info')]"))
            )
            save_info.click()

            turn_on = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'Turn On')]"))
            )
            turn_on.click()
        finally:
            print('Login error')

    def go_to_user_profile(self):
        driver = self.driver
        user_profile = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/span"))
        )
        user_profile.click()
        go_to_user_profile = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]"))
        )
        go_to_user_profile.click()

    def get_followers(self):
        driver = self.driver
        wait = WebDriverWait(driver, 120)
        follower_but = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//header/section/ul/li[2]/a")))
        follower_but.click()
        popup_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[5]/div/div/div[2]")))

        num_of_followers = int(
            driver.find_element_by_xpath("//li[2]/a/span").text)
        driver.implicitly_wait(10)
        print('Scrapping the followers list....')
        for _ in range(5):
            driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollHeight', popup_box)
            time.sleep(2)
            followers_elems = driver.find_elements_by_class_name('FPmhX')[-60:]
        self.followers = [e.text for e in followers_elems]
        print(self.followers)
        close_but = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[2]")
        ))
        close_but.click()

    def get_following(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        following_but = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//header/section/ul/li[3]/a")))
        following_but.click()
        popup_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[5]/div/div/div[2]")))
        driver.implicitly_wait(10)
        print('Scrapping the following list....')
        for _ in range(5):
            driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollHeight', popup_box)
            time.sleep(2)
            following_elems = driver.find_elements_by_class_name('FPmhX')[-35:]
            following_bio = driver.find_elements_by_class_name('wFPL8')[-35:]
        self.following = [e.text for e in following_elems]
        following_bio = [r.text for r in following_bio]
        following_dict = dict(zip(self.following, following_bio))
        print("------- These are the accounts and bios of the accounts you follow -------")
        print(following_dict)
        print()
        close_but = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[2]")
        ))
        close_but.click()

    def get_results(self):
        driver = self.driver
        results = list(set(self.followers)-set(self.following))
        print(results)
        print()
        print("---------- Followers not following you back -------------")
        for i in range(len(results)):
            print(str(i+1) + ". " + results[i])
        print()

    def back_to_home_page(self):
        driver = self.driver
        home_but = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[1]/div"))
        )
        home_but.click()
        turn_on = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Turn On')]"))
        )
        turn_on.click()

    def search_hashtag(self, hashtag):
        driver = self.driver
        driver.get('https://www.instagram.com/explore/tags/' + hashtag)

    def like_photos(self, amount):
        driver = self.driver
        driver.find_element_by_class_name('v1Nh3').click()
        i = 1
        while i <= amount:
            time.sleep(2)
            driver.find_element_by_class_name('fr66n').click()
            time.sleep(2)
            driver.find_element_by_class_name(
                'coreSpriteReftPaginationArrow').click()
            i += 1
        close_button = driver.find_element_by_class_name('wpO6b')
        close_button.click()
        wait = WebDriverWait(driver, 10)
        home_but = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[1]/div/a")))
        home_but.click()


ig = InstagramBot1()
ig.login('jiminsisisiii', 'jiminpark')
ig.go_to_user_profile()
ig.get_followers()
ig.get_following()
ig.get_results()
ig.back_to_home_page()
ig.search_hashtag('travel')
ig.like_photos(5)
