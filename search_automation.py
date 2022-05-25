from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def create_browser():
    """Creates a browser with a webdriver.
    Returns:
        object of class 'selenium.webdriver.chrome.webdriver.WebDriver': The used browser.
    """
    s = Service("/Users/leadang/Documents/Selenium/chromedriver")
    browser = webdriver.Chrome(service=s)
    return browser


def search_for_phrases(phrases, browser):
    """Searches for the first result of a phrase.
    Args:
        phrases (list of strings): The search phrases.
        browser (object of class 'selenium.webdriver.chrome.webdriver.WebDriver'): The used browser.
    Returns:
        dictionary: The phrase with the title and link of the first result.
    """
    # Open Google and handle Google consent popup
    browser.get("http://www.google.com")
    try:
        accept_button = browser.find_element(By.XPATH, "//*[@id=\"L2AGLb\"]/div")
        accept_button.click()
    except Exception:
        pass

    results = {}

    for phrase in phrases:
        # Searching for phrase in Google
        element = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.NAME, "q")))
        element.send_keys(phrase)
        element.send_keys(Keys.ENTER)

        # Clicking on the first Google search result
        result = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div > a > h3")))
        result.click()

        # Extracting title and URL of the first search result
        # Sleeping for a second so that page can load (function browser.implicitly_wait(10) did not always work)
        time.sleep(1)
        results[phrase] = [browser.title, browser.current_url]

        # Returning to search page and clearing searchbar
        browser.execute_script("window.history.go(-1)")
        search = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.NAME, "q")))
        search.clear()

    return results


def print_results(results):
    """Prints results on Standard output.
    Args:
        results (dictionary): Search phrases with titles and links.
    """
    print("\n" + "{:<30} {:<80} {:<80}".format('SEARCH PHRASE', 'TITLE of first result', 'URL of first result'))
    print("_____________________________" +
          "________________________________________________________________________________" +
          "________________________________________________________________________________")
    for phrase, result in results.items():
        title, url = result
        print("{:<30} {:<80} {:<80}".format(phrase, title, url))


def print_specific_result(results, *phrases):
    """Prints specific results on Standard output.
    Args:
        results (dictionary): Search phrases with titles and links.
    """
    print("\n" + "{:<30} {:<80} {:<80}".format('SEARCH PHRASE', 'TITLE of first result', 'URL of first result'))
    print("_____________________________" +
          "________________________________________________________________________________" +
          "________________________________________________________________________________")
    for phrase in phrases:
        if results.get(phrase) is not None:
            title, url = results.get(phrase)
            print("{:<30} {:<80} {:<80}".format(phrase, title, url))
        else:
            print("{:<30} {:<80} {:<80}".format(phrase, "Is not part of former search phrases!",
                                                "Is not part of former search phrases!"))


def main():
    # Example for an input
    phrases = ['Amazon Ratenzahlung',
               'H&M Ratenzahlung',
               'Mediamarkt Ratenzahlung',
               'Zara Ratenzahlung',
               'Buy now pay later',
               'Monet',
               'C&A Ratenzahlung']

    # Executing search
    browser = create_browser()
    results = search_for_phrases(phrases, browser)

    # Closing browser page
    browser.quit()

    # Results on Standard output
    print_results(results)

    # Specific results on Standard output
    print_specific_result(results, 'Amazon Ratenzahlung', 'Amazon', 'Monet')


if __name__ == '__main__': main()
