import configparser
import io
import time

import boto3
import requests
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from logs import get_logger

logger = get_logger(__name__)
config = configparser.ConfigParser()
config.read_file(open("config.cfg"))

AWS_KEY = config.get("AWS", "AWS_KEY")
AWS_SECRET = config.get("AWS", "AWS_SECRET")

URL_PRICES = config.get("STAGING", "URL_PRICES")
DRIVER_PATH = config.get("STAGING", "DRIVER_PATH")
BUCKET = config.get("STAGING", "BUCKET")
PREFIX_PRICES = config.get("STAGING", "PREFIX_PRICES")


def get_url(element: WebElement) -> str:
    """Get url from element"""

    tries = 0
    while True:
        try:
            url = element.get_attribute("href")
            logger.info(f"Parsed url: {url}")
            break
        except StaleElementReferenceException as e:
            time.sleep(1)
            tries += 1

        if tries > 5:
            break
    else:
        logger.error("url not found")

    return url


def save_file(url: str) -> None:
    """Store downloaded file in S3 bucket."""

    name = url.split("/")[-1]
    resp = requests.get(url)

    buf = io.BytesIO()
    buf.write(resp.content)
    buf.seek(0)

    s3 = boto3.resource(
        "s3",
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_SECRET,
    )

    boto_test_bucket = s3.Bucket(BUCKET)
    boto_test_bucket.upload_fileobj(buf, f"{PREFIX_PRICES}/{name}")


def main():
    """Run extraction of files from the web"""
    ## Setup chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    # Set path to chromedriver as per your configuration
    webdriver_service = Service(DRIVER_PATH)

    # Choose Chrome Browser
    browser = webdriver.Chrome(
        service=webdriver_service, options=chrome_options
    )
    browser_files = webdriver.Chrome(
        service=webdriver_service, options=chrome_options
    )

    # Get page
    browser.get(URL_PRICES)

    try:
        list_elements = browser.find_elements(
            By.XPATH,
            "/html/body/div[1]/div[2]/div/div[1]/div/article/section/div/pre/a",
        )
        for elem in list_elements:
            url = get_url(elem)
            browser_files.get(url)
            list_files = browser_files.find_elements(
                By.XPATH,
                "/html/body/div[1]/div[2]/div/div[1]/div/article/section/p[2]/a",
            )
            if not list_files:
                list_files = browser_files.find_elements(
                    By.XPATH,
                    "/html/body/div[1]/div[2]/div/div[1]/div/article/section/div"
                    "[3]/table/tbody/tr/td[3]/a",
                )

            for file in list_files:
                url = get_url(file)
                save_file(url)
                time.sleep(1)
    except Exception as e:
        logger.error(e)
    finally:
        browser.quit()
        browser_files.quit()
