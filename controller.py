import time
from selenium import webdriver
from exceptions import OptionalException
from helper import DOM_IDENTIFIER_TYPE, DOM_ACTION
from selenium.webdriver.firefox.options import Options

class SelenimController:
    """
    UpworkController class
    """
    schemas = {
		DOM_IDENTIFIER_TYPE.ID: {
            'method': 'find_element_by_id(dom_identifier)'
        },
		DOM_IDENTIFIER_TYPE.CLASS: {
            'method': 'find_elements_by_class_name(dom_identifier)'
        },
        DOM_IDENTIFIER_TYPE.XPATH: {
            'method': 'find_element_by_xpath(dom_identifier)'
        },
        DOM_IDENTIFIER_TYPE.TEXT: {
            'method': 'find_element_by_link_text(dom_identifier)'
        },
        DOM_IDENTIFIER_TYPE.OBSCURE_TEXT: {
            'method': 'find_element(By.CSS_SELECTOR,dom_identifier)'
        }
	}

    def __init__(self, headless=False):
        firefox_options = Options()
        firefox_options.headless = True if headless == True else False
        print('firefox_options.headless: ' + str(firefox_options.headless))
        self.browser = webdriver.Firefox(options=firefox_options)

    def change_url(self, url):
        if url != self.browser.current_url:
            self.browser.get(url)

    def execute_action(self,
            schema=None,
            dom_identifier=None,
            action=None,
            value=None,
            optional=None,
            getAttributeValue=None,
            wait=True
    ):
        if schema not in self.schemas:
            raise Exception('Wrongly defined schema')

        if action == None or schema == None or dom_identifier == None:
            raise Exception('Empty elements have been delivered')

        if wait:
            time.sleep(5)

        try:
            element = eval('self.browser.' + str(self.schemas[schema]['method']))
        except Exception as e:
            # Check if the deliver DOM element is an optional one
            if optional:
                raise OptionalException()
            else:
                raise Exception(e)
        else:
            if action == DOM_ACTION.CLICK:
                element.click()
            elif action == DOM_ACTION.FILL:
                '''
                    We have to execute value at this point
                    f.e. because of the Google Auth's expiration time
                '''
                element.send_keys(value())
            elif action == DOM_ACTION.READ:
                return element.get_attribute(getAttributeValue)