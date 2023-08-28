import os
from time import sleep
from selenium import webdriver
from dotenv import load_dotenv
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

load_dotenv()


class InstagramFollowerBot:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def instagram_login(self):
        self.driver.find_element(by=By.XPATH, value="//button[text()='Allow all cookies']").click()
        sleep(2)
        self.driver.find_element(
            by=By.XPATH,
            value="//*[@id='loginForm']/div/div[1]/div/label/input"
        ).send_keys(os.environ["phone_number"])
        self.driver.find_element(
            by=By.XPATH,
            value="//*[@id='loginForm']/div/div[2]/div/label/input"
        ).send_keys(os.environ["pass"])
        self.driver.find_element(by=By.XPATH, value="//div[text()='Log in']").click()
        sleep(5)
        self.driver.find_element(by=By.XPATH, value="//button[text()='Save Info']").click()
        sleep(2)
        self.driver.find_element(by=By.XPATH, value="//button[text()='Not Now']").click()

    def find_followers(self):
        self.driver.find_element(
            by=By.XPATH,
            value="/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a"
        ).click()
        sleep(2)
        followers_elements_1 = self.get_followers_elements()
        self.scroll_followers()
        followers_elements_2 = self.get_followers_elements()
        while len(followers_elements_1) != len(followers_elements_2):
            followers_elements_1 = followers_elements_2
            self.scroll_followers()
            followers_elements_2 = self.get_followers_elements()

        self.follow_accounts(followers_elements_1)

    def get_followers_elements(self):
        return self.driver.find_elements(
            by=By.XPATH,
            value='/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div/div'
        )

    def scroll_followers(self):
        scrollable_div = self.driver.find_element(
            by=By.XPATH,
            value='/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]'
        )

        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        sleep(3)

    def follow_on_instagram(self):
        self.driver.get(f"https://instagram.com/")
        sleep(2)
        self.instagram_login()
        sleep(5)
        self.driver.get(f"https://instagram.com/{os.environ['instagram_account']}")
        sleep(5)
        self.find_followers()

    @staticmethod
    def follow_accounts(followers):
        for element in followers:
            try:
                follow_button = element.find_element(by=By.CSS_SELECTOR, value="button._acan._acap._acas._aj1-")
                follow_button.click()
            except NoSuchElementException as e:
                print(f"Can't follow {element.text.split()[0]}")
            else:
                print(f"Can follow {element.text.split()[0]}")


ic = InstagramFollowerBot()
ic.follow_on_instagram()

sleep(20)
