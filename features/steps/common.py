# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-raised
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=bare-except
# pylint: disable=unnecessary-dunder-call
# pylint: disable=no-member
from datetime import datetime
import json
import os
import glob
import random
import re
import string
import time
import xml.etree.ElementTree as ET
import fitz  # PyMuPDF
import requests
import pytesseract
from datetime import datetime
import allure
from PIL import Image
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from yaml import safe_load
from steps import logger



def attach_page(context, page_name):
    """This method attaches the specified page by switching to the corresponding browser window."""
    page_name = int(page_name.replace("Page", "")) - 1
    all_window_handles = context.driver.window_handles
    if page_name is not None:
        context.driver.switch_to.window(all_window_handles[page_name])
        return
    for handle in all_window_handles:
        context.driver.switch_to_window(handle)
        page_title = context.driver.title
        if page_name in page_title:
            break


def delete_files(folder_path):
    """this method delete the files"""
    for the_file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def rename_file(path, file_name):
    """this method rename the files"""
    try:
        new_file_name = os.path.join(path, file_name + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.png')
        os.rename(os.path.join(path, file_name + '.png'), new_file_name)
    except WindowsError:
        print('image not found to rename:' + new_file_name)


def get_xml_data(file_path, tag_name):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root.find(tag_name).text
    except Exception as e:
        raise Exception(e)


def get_data(context, variable):
    """
    Processes the input variable by replacing specific placeholders with ,dynamically generated data,
    such as random numbers, text, emails or copied text/number from a context object.
    Args:
        context: An object containing data sources like yamldata, WebCopiedList, etc.
        variable (str): The variable name or placeholder string to process.
    Returns:
        str: The processed string with dynamic placeholders replaced.
    """
    variable = str(get_yml_value(context.yaml_data, variable))


    variable = variable.replace('_empty_', '').replace('_space_', '')
    # Handle @randomnumber_X to generate random numbers of specified digits
    if "@randomnumber_" in variable:
        try:
            num_digits = int(variable.split("_")[1])
            random_number = ''.join(random.choice("0123456789") for _ in range(num_digits))
            variable = variable.replace(f"@randomnumber_{num_digits}", random_number)
        except (IndexError, ValueError):
            random_number = str(random.randint(0, 9999999999)).zfill(10)
            variable = variable.replace("@randomnumber_", random_number)
    # Handle @randomnumber for a general random number with up to 10 digits
    elif "@randomnumber" in variable:
        random_number = str(random.randint(0, 9999999999)).zfill(10)
        variable = variable.replace("@randomnumber", random_number)
    # Handle @randomtext to generate a random string of 7 lowercase letters
    if "@randomtext" in variable:
        random_text = ''.join(random.choice(string.ascii_lowercase) for _ in range(7))
        variable = variable.replace("@randomtext", random_text)
    # Handle @randomemail to generate a random email address
    if "@randomemail" in variable:
        random_text = ''.join(random.choice(string.ascii_lowercase) for _ in range(7))
        digits = ''.join(random.choice(string.digits) for _ in range(3))
        email_prefix = random_text + digits
        variable = variable.replace("@randomemail", email_prefix + "@gmail.com")
    # Special case: If variable ends with @gmail.com and contains @randomtext
    if variable.endswith("@gmail.com") and "@randomtext" in variable:
        random_text = ''.join(random.choice(string.ascii_lowercase) for _ in range(7))
        variable = variable.replace("@randomtext", random_text)
    if "@copiedtext" in variable.lower():
        match = re.search(r"@copiedtext_(\d+)", variable.lower())
        if match:
            index = int(match.group(1))
            variable = context.web_copied_list[index - 1]
        else:
            variable = context.label_text
    if "@copiednumber" in variable.lower():
        variable = context.label_number
        # Handle @currentdate with or without a specified format
    if "@currentdate" in variable.lower():
        if "@currentdate_" in variable:
            try:
                format_part = variable.split("@currentdate_")[1]
                date_format = (format_part.replace("dd", "%d")
                               .replace("mm", "%m")
                               .replace("yyyy", "%Y")
                               .replace("yy", "%y"))
                current_date = datetime.now().strftime(date_format)
                variable = variable.replace(f"@currentdate_{format_part}", current_date)
            except (IndexError, ValueError):
                current_date = datetime.now().strftime("%Y-%m-%d")
                variable = variable.replace("@currentdate_", current_date)
        else:
            current_date = datetime.now().strftime("%Y-%m-%d")
            variable = variable.replace("@currentdate", current_date)

    return variable


def get_yml_value(data, key):
    """
    Retrieves the value associated with a given key from a YAML-formatted string.
    Args:
        data (str): A YAML-formatted string.
        key (str): The key whose value needs to be retrieved.
    Returns:
        str: The value corresponding to the key, or the key itself if not found or an error.
    """
    try:
        data = safe_load(data)
        value = data.get(key)
        if value is None:
            return key
        else:
            return value
    except Exception as e:
        return key


def get_yml_object_repository_value(data, node, key, context):
    """
    Retrieves a value from a specified node and key in a YAML-formatted string.
    Args:
        data (str): A YAML-formatted string.
        node (str): The top-level key (node) under which to look for the sub-key.
        key (str): The key within the node whose value is to be retrieved.
    Returns:
        str: The value corresponding to the node and key, or the key itself if not found or on error.
    """
    try:
        data = safe_load(data)
        if node == "":
            value = data[key]
        else:
            value = data[node][key]
        if value is None:
            value = key
    except Exception as e:
        print(e)
        value = key
    context.xpath = value
    context.xpath_key = node + "." + key
    return value


def get_object_repository_value(data, key):
    """
    Retrieves the value associated with a given key from an object repository stored in a YAML-formatted string.
    Args:
        data (str): A YAML-formatted string representing the object repository.
        key (str): The key whose value needs to be retrieved.
    Returns:
        str: The value associated with the key, or the key itself if not found or on error.
    """
    try:
        data = safe_load(data)
        value = data[key]
        if value is None:
            return key
        else:
            return value
    except Exception:
        return key


def get_frames(context, xpath):
    """
    Switches to the appropriate iframe based on the provided XPath.The XPath may contain a frame name/id using the
    format: "element_xpath||frame_name".This function resets the driver to the default content and switches to the given frame.
    Args:
        context: Test context containing the WebDriver instance.
        xpath (str): XPath string, possibly with frame info.
    Returns:
        str: Cleaned XPath without the frame reference.
    """
    try:
        context.driver.switch_to.default_content()
        if (xpath.find("||")) != -1:
            split_xpath = xpath.split("||")
            context.driver.switch_to.frame(split_xpath[1])
            return split_xpath[0]
        else:
            context.driver.switch_to.default_content()
            return xpath

    except Exception as e:
        raise Exception(e)


def web_element(context, identification_type, xpath):
    """
    Fetches a single web element using the provided locator strategy and path. Supports 'xpath', 'id', and
    also handles shadow DOM elements.
    Args:
        context: Test context with WebDriver instance.
        identification_type (str): Locator type (e.g., 'xpath', 'id').
        xpath (str): The locator or JavaScript path for shadow DOM.
    Returns:
        WebElement or shadow DOM object.
    """
    if "shadowRoot" in xpath:
        locator = f"return {xpath}"
        return context.driver.execute_script(locator)
    elif identification_type.upper() == "xpath".upper():
        return context.driver.find_element(By.XPATH, xpath)
    elif identification_type.upper() == "id".upper():
        return context.driver.find_element(By.ID, xpath)


def web_elements(context, identification_type, xpath):
    """
    Fetches multiple web elements using the given locator strategy.
    Args:
        context: Test context with WebDriver instance.
        identification_type (str): Locator type (e.g., 'xpath', 'id').
        xpath (str): Locator to find matching elements.
    Returns:
        list: List of matching WebElements.
    """
    if identification_type.upper() == "xpath".upper():
        return context.driver.find_elements(By.XPATH, xpath)
    elif identification_type.upper() == "id".upper():
        return context.driver.find_elements(By.ID, xpath)


def get_text(element):
    """
    Retrieves visible or accessible text from a web element. Falls back to checking 'value', 'placeholder', or
    'data-value' attributes if `.text` is empty.
    Args:
        element (WebElement): The Selenium WebElement to extract text from.
    Returns:
        str: Extracted text content or attribute value.
    """
    text = element.text
    if not text:
        text = get_attribute(element,"value")
    if not text:
        text = get_attribute(element,"placeholder")
    if not text:
        text = get_attribute(element,"data-value")
    return text


def store_element_in_json(xpath, element_html):
    """
    Stores or updates a web element's locator and HTML content in a JSON file.
    If the locator already exists in the file, it updates the target HTML only if it's different
    or missing. Otherwise, it appends the new locator-target pair.
    Args:
        xpath (str): The XPath locator of the element.
        element_html (str): The HTML string of the element.
    """
    json_file_path = os.path.join(os.getcwd(), "steps", "htmlElement.json")
    new_data = {
        "locator": xpath,
        "target": element_html
    }
    try:
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
        existing_data = []
        if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
            with open(json_file_path, 'r') as file:
                try:
                    existing_data = json.load(file)
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data]
                except json.JSONDecodeError:
                    existing_data = []
        updated = False
        for entry in existing_data:
            if entry.get("locator") == xpath:
                if "target" not in entry or not entry["target"]:
                    entry["target"] = element_html
                elif entry.get("target") != element_html:
                    entry["target"] = element_html
                else:
                    print("Same locator and target found. No update needed.")
                updated = True
                break

        if not updated:
            existing_data.append(new_data)
        for entry in existing_data:
            if "target" in entry and isinstance(entry["target"], str):
                entry["target"] = entry["target"].replace('"', "'")
        with open(json_file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)
    except Exception as e:
        print(f" An error occurred: {str(e)}")


def get_tool_tip(element):
    """
    Retrieves the tooltip text from an element by checking its attributes or child elements
    Args:
        element (WebElement): The Selenium WebElement to extract tooltip text from.
    Returns:
        str: The tooltip text if found, otherwise the element's text.
    """
    attributes = ["alt", "title", "data-original-title", "id", "uib-tooltip", "mattooltip"]
    for attr in attributes:
        tool_tip_text = get_attribute(element,attr)
        if tool_tip_text:
            return tool_tip_text
    try:
        tool_tip_text = element.find_element(By.XPATH, ".//*[text()]").text
        if tool_tip_text and tool_tip_text.strip():
            return tool_tip_text
    except Exception as e:
        print(f"Error retrieving tooltip text: {e}")
    return element.text


def click_and_hold_and_release(context, identification_type, xpath):
    """
    Performs a click-and-hold on the first element and releases it on the second element.
    The XPath should include two parts separated by '**' indicating the source and target elements.
    Args:
        context: The test context containing WebDriver and timeout configs.
        identification_type (str): The method to locate elements (e.g., 'xpath', 'id').
        xpath (str): Combined XPath string in format "source_xpath**target_xpath".
    """
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            split_xpath = xpath.split("**")
            element_1 = web_element(context, identification_type, split_xpath[0])
            element_2 = web_element(context, identification_type, split_xpath[1])
            try:
                actions = ActionChains(context.driver)
                actions.click_and_hold(element_1).move_to_element(element_2).release().perform()
                logger.info(context, "Clicked and hold and released")
                time.sleep(2)
                break
            except:
                raise Exception("Drag and drop horizontally unsuccessful")
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        logger.error(context, f"Retry {i + 1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception(f"Unable to enter drag and drop.")


def click_action(context, identification_type, xpath):
    """
    Attempts to click an element using standard click or JavaScript fallback.
    Args:
        context: The test context with WebDriver and configuration.
        identification_type (str): The locator type (e.g., 'xpath', 'id').
        xpath (str): XPath of the element to be clicked.
    """
    i = 0
    xpath = get_frames(context, xpath)
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context, identification_type, xpath)
            context.element_html = get_attribute(element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            try:
                element.click()
                break
            except:
                context.driver.execute_script("arguments[0].click()", element)
                break
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            logger.error(context,f"Unable to click on element within timeout")
            raise Exception(f"Unable to click on element, XPath is: {xpath}")


def entered_text(context, value_to_be_entered, identification_type, xpath):
    """
    Enters the specified text into a text box identified by the given XPath.
    Args:
        context: The test context with WebDriver and input data.
        value_to_be_entered (str): The key for value to be entered (supports dynamic data).
        identification_type (str): The locator type ('xpath', 'id').
        xpath (str): XPath of the text input field.
    """
    value_to_be_entered = str(get_data(context, value_to_be_entered))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context, identification_type, xpath)
            context.element_html = get_attribute(element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            send_keys_to_element(element,value_to_be_entered)
            logger.info(context, 'Entered Value is : ' + value_to_be_entered)
            break
        except:
            logger.error(context, "Unable to enter Value")
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception(f"Unable to enter {value_to_be_entered} in Text Box")


def clear_and_enter_text(context, text_to_be_entered, identification_type, xpath):
    """ Clears existing text in an input field and enters new text. """
    text_to_be_entered = str(get_data(context, text_to_be_entered))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context, identification_type, xpath)
            context.element_html = get_attribute(element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            send_keys_to_element(element,Keys.CONTROL + "a")
            send_keys_to_element(element,Keys.DELETE)
            time.sleep(1)
            send_keys_to_element(element,text_to_be_entered)
            logger.info(context, 'Entered Value is : ' + text_to_be_entered)
            break
        except:
            logger.error(context, "Unable to clear and enter Value")
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception(f"Unable to enter {text_to_be_entered} in Text Box")


def scroll_and_enter_text(context, text_to_be_entered, identification_type, xpath):
    """This method scrolls to the specified element and enters the given text"""
    text_to_be_entered = str(get_data(context, text_to_be_entered))
    i = 0
    xpath = get_frames(context, xpath)
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context, identification_type, xpath)
            context.element_html = get_attribute(element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            try:
                context.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                send_keys_to_element(element,text_to_be_entered)
                logger.info(context, 'Entered Value is : ' + text_to_be_entered)
                break
            except:
                actions = ActionChains(context.driver)
                actions.move_to_element(element).perform()
                send_keys_to_element(element,text_to_be_entered)
                logger.info(context, 'Entered Value is : ' + text_to_be_entered)
                break
        except:
            logger.error(context, "Unable to scroll and enter Value")
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception(f"Unable to enter {text_to_be_entered} in Text Box , XPath is : {xpath}")


def scroll_and_clear_enter_text(context, text_to_be_entered, identification_type, xpath):
    """This method scrolls to the specified element, clears its existing text, and enters the new text"""
    text_to_be_entered = str(get_data(context, text_to_be_entered))
    xpath = get_frames(context, xpath)
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context, identification_type, xpath)
            context.element_html = get_attribute(element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            try:
                context.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                send_keys_to_element(element,Keys.CONTROL + "a")
                send_keys_to_element(element,Keys.DELETE)
                time.sleep(1)
                send_keys_to_element(element,text_to_be_entered)
                logger.info(context, 'Entered Value is : ' + text_to_be_entered)
                break
            except:
                actions = ActionChains(context.driver)
                actions.move_to_element(element).perform()
                send_keys_to_element(element,Keys.CONTROL + "a")
                send_keys_to_element(element,Keys.DELETE)
                time.sleep(1)
                send_keys_to_element(element,text_to_be_entered)
                logger.info(context, 'Entered Value is : ' + text_to_be_entered)
                break
        except:
            logger.info(context, "Unable to scroll and clear and enter Value")
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception(f"Unable to enter {text_to_be_entered} in Text Box , XPath is : {xpath}")


def verify_content(context, data_value, identification_type, xpath):
    """This method verifies that the content of a label matches the expected value"""
    i = 0
    data_value = str(get_data(context, data_value))
    xpath = get_frames(context, xpath)
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            web_element = web_element(context, identification_type, xpath)
            element = get_text(web_element)
            context.element_html = get_attribute(web_element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            logger.info(context,'Actual Value is : ' + element + " Expected Values is : " + data_value)
            if element.find(str(data_value)) != -1:
                return True
            return False
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i + 1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception(("Unable to verify element , XPath is:", xpath))


def is_element_present(context, param):
    """
    Checks if any element containing the specified text is present on the page.
    Args:
        context: The test context.
        param (str): The partial text to search for element
    Returns:
        bool: True if found, False otherwise.
    """
    i = 0
    xpath = "//*[contains(text(),'" + param + "')]"
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = context.driver.find_elements(By.XPATH, xpath)
            if len(elements) > 0:
                return True
            return False
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i + 1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to verify on element")


def scroll_and_click(context, identification_type, xpath):
    """This method will scroll and click the element"""
    i = 0
    xpath = get_frames(context, xpath)
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context, identification_type, xpath)
            context.element_html = get_attribute(element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            try:
                context.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                element.click()
                logger.info(context, f"Scrolled and clicked using JavaScript")
                break
            except:
                actions = ActionChains(context.driver)
                actions.move_to_element(element).perform()
                element.click()
                logger.info(context, f"Scrolled and clicked using ActionChains")
                break
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        logger.error(context, f"Unable to scroll and click the element after {i} attempts")
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to Scroll To The Element", xpath)


def remove_all_items(context, xpath):
    """This method removes items from a page based on the provided XPath"""
    i = 0
    if xpath in '**':
        split_xpath = xpath.split('**')
        while i < int(context.max_seconds_to_wait_for_control):
            try:
                element_locator_1 = (By.XPATH, split_xpath[0])
                element_1 = WebDriverWait(context.driver, 8).until(EC.visibility_of_element_located(element_locator_1))
                element_1.click()
                element_locator_2 = (By.XPATH, split_xpath[1])
                element_2 = WebDriverWait(context.driver, 8).until(EC.visibility_of_element_located(element_locator_2))
                element_2.click()
                logger.info(context, "Removed an item set")
            except:
                break
    else:
        while i < int(context.max_seconds_to_wait_for_control):
            try:
                element_locator = (By.XPATH, xpath)
                element = WebDriverWait(context.driver, 8).until(EC.visibility_of_element_located(element_locator))
                element.click()
                logger.info(context, "Removed an item")
            except:
                break


def copied_number(context, identification_type, xpath):
    """This method copies a numeric value from an element's text"""
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context, identification_type, xpath)
            context.element_html = get_attribute(element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            param = get_text(element)
            if param.find(".") != -1:
                split_prices = param.split('.')
                context.label_number = re.sub(r'\D', '', split_prices[0])
                logger.info(context, 'Copied Number : ' + context.label_number)
                break
            else:
                context.label_number = re.sub(r'\D', '', param)
                logger.info(context, f'Copied Number : {context.label_number}')
                break
        except Exception:
            logger.info(context, 'Failed to copy Number')
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("not able to copy the value , XPath is :", xpath)


def verify_copied_number(context, identification_type, xpath):
    """This method verifies if the number extracted from an element matches the previously copied number stored in context.label_number"""
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context, identification_type, xpath)
            context.element_html = get_attribute(element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            variable = get_text(element)
            if variable.find(".") != -1:
                split_prices = variable.split('.')
                actual_number = re.sub(r'\D', '', split_prices[0])
                logger.info(context, 'Actual Number : ' + actual_number + " Expected Number : " + context.label_number)
                if int(context.label_number) == int(actual_number):
                    return True
                return False
            else:
                actual_number = re.sub(r'\D', '', variable)
                logger.info(context, 'Actual Number : ' + actual_number + " Expected Number : " + context.label_number)
                if int(context.label_number) == int(actual_number):
                    return True
                return False
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i + 1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            return False


def copied_text(context, identification_type, xpath):
    """this method copy the text of the element"""
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            xpath = get_frames(context, xpath)
            try:
                element = web_element(context, identification_type, xpath)
                context.element_html = get_attribute(element,"outerHTML")
                store_element_in_json(xpath, context.element_html)
                context.label_text = get_text(element)
                logger.info(context, 'Copied Text : ' + context.label_text)
                context.web_copied_list.append(context.label_text)
                break
            except:
                select_list = Select(context.driver.find_element(By.XPATH, xpath))
                context.label_text = select_list.first_selected_option.text
                logger.info(context, f'Copied Text : {context.label_text}')
                context.web_copied_list.append(context.label_text)
                break
        except Exception:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Final attempt failed. Could not copy text.")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("not able to copy the value , XPath is : ", xpath)


def verify_copied_text(context, identification_type, xpath):
    """This method verifies if the text of an element or the selected option in a dropdown matches the previously copied text stored"""
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context, identification_type, xpath)
            context.element_html = get_attribute(element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            actual_text = get_text(element)
            logger.info(context, 'Actual Text : ' + actual_text + " Expected Text : " + context.label_text)
            if str(actual_text).find(context.label_text) != -1:
                return True
        except Exception:
            select_list = Select(web_element(context, identification_type, xpath))
            variable = select_list.first_selected_option.text
            logger.info(context, f'Actual Text : {variable} Expected Text: {context.label_text}')
            if variable in context.label_text:
                return True
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            return False


def verify_text_from_image(context, node, xpath, data_value):
    """This method takes a screenshot, extracts text from the image, and verifies if the extracted text matches the expected value"""
    i = 0
    data_value = str(get_yml_value(context.yaml_data, get_data(context, data_value)))
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            random_number = random.randint(0, 9999)
            file_name = f"screenshot_{random_number}.png"
            context.driver.save_screenshot(file_name)
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            image = Image.open(file_name)
            text = pytesseract.image_to_string(image)
            if data_value in text:
                os.remove(file_name)
                return True
            else:
                os.remove(file_name)
                return False
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i + 1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to verify text in the Image")


def scroll_and_check(context, identification_type, xpath):
    """This method scrolls to a web element, clicks it if it's not already selected, and handles scrolling"""
    xpath = get_frames(context, xpath)
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context, identification_type, xpath)
            context.element_html = get_attribute(element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            try:
                context.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                if not element.is_selected():
                    element.click()
                    logger.info(context, 'Scrolled and checked checkbox')
                break
            except:
                actions = ActionChains(context.driver)
                actions.move_to_element(element).perform()
                if not element.is_selected():
                    logger.info(context, 'Scrolled and checked checkbox')
                    element.click()
                break
        except:
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to Scroll To The Element", xpath)


def scroll_and_uncheck(context, identification_type, xpath):
    """This method scrolls to a web element and unchecks it if it is selected"""
    xpath = get_frames(context, xpath)
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context, identification_type, xpath)
            context.element_html = get_attribute(element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            try:
                context.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                if element.is_selected():
                    logger.info(context, 'Scrolled and unchecked checkbox')
                    element.click()
                break
            except:
                actions = ActionChains(context.driver)
                actions.move_to_element(element).perform()
                if element.is_selected():
                    logger.info(context, 'Scrolled and unchecked checkbox')
                    element.click()
                break
        except:
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to Scroll To The Element", xpath)


def file_upload(context, param, identification, xpath):
    """This method uploads a file by sending its path to a web element"""
    xpath = get_frames(context, xpath)
    i = 0
    param = get_data(context, param)
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context, identification, xpath)
            context.element_html = get_attribute(element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            if os.path.isabs(param):
                send_keys_to_element(element,param)
                break
            else:
                current_directory = os.getcwd()
                file_path = os.path.join(current_directory, param)
                send_keys_to_element(element,file_path)
                logger.info(context,
                            f"File uploaded successfully ")
                break
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i + 1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to perform fileupload", xpath)

def read_pdf(context, url, text):
    """ Reads a PDF from a URL and checks if a specific text is present within the PDF content."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        pdf_document = fitz.open(stream=response.content, filetype="pdf")
        extracted_text = ""
        for page in pdf_document:
            extracted_text += page.get_text()
        if text in extracted_text:
            logger.info(context,f"PDF content : {extracted_text} , Expected content : {text}")
            return True
    except requests.RequestException as req_err:
        print(f"Request error: {req_err}")
    except Exception as e:
        print(f"Error: {e}")
    return False



def verify_downloaded_file(context, file_path):
    """ Verifies if a file with the expected extension is downloaded recently."""
    if 'Extention' in file_path:
        file_type = file_path.split("_")[1]
        path = os.getcwd()
        files = glob.glob(os.path.join(path, "*.*"))
        if files:
            # Sort files by modification time in descending order
            files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            file_extension = os.path.splitext(files[0])[1][1:]
            if file_extension == file_type:
                logger.info(context, f'Actual value is : {file_extension} Expected value is : {file_type}')
                return True
        return False


def scroll_and_verify_tooltip(context, info_xpath, mouse_hover_xpath):
    """ Scrolls the page and verifies if a tooltip is displayed upon hovering."""
    context.driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(2)
    for i in range(10):
        scroll_height = (i + 1) * 100
        context.driver.execute_script(f"window.scrollTo(0, {scroll_height})")
        time.sleep(1)
        try:
            hover_element = context.driver.find_element(By.XPATH, info_xpath)
            if hover_element.is_displayed():
                actions = ActionChains(context.driver)
                actions.move_to_element(hover_element).perform()
                time.sleep(1)
                tooltip_element = context.driver.find_element(By.XPATH, mouse_hover_xpath)
                if tooltip_element.is_displayed():
                    break
        except Exception:
            pass
    return False


def get_page_source(driver):
    """Retrieves the full HTML source of the current web page."""
    try:
        page_source = driver.page_source
        return page_source
    except Exception as e:
        raise


def is_element_enabled(element):
    """
    Safely checks if the given element is enabled.
    Returns False if element is not found or not interactable.
    """
    try:
        return element.is_enabled()
    except Exception:
        return False


def is_element_selected(element):
    """
    Safely checks if the given element is selected.
    Returns False if element is not found or not interactable.
    """
    try:
        return element.is_selected()
    except Exception:
        return False


def is_element_displayed(element):
    """
    Safely checks if the given element is displayed.
    Returns False if element is not found or not interactable.
    """
    try:
        return element.is_displayed()
    except Exception:
        return False


def click_element(element):
    """
    Safely clicks on the provided web element.
    """
    try:
        element.click()
    except Exception as e:
        raise Exception(f"Click failed: {str(e)}")


def send_keys_to_element(element, text):
    """
    Sends text to the provided web element safely.
    Raises an exception if the element is not interactable or fails.
    """
    try:
        element.send_keys(text)
    except Exception as e:
        raise Exception(f"Failed to send keys to element: {str(e)}")


def get_attribute(element, attribute_name):
    """Fetches the value of a specified attribute from a web element."""
    try:
        if element is None:
            return ""
        value = element.get_attribute(attribute_name)
        return value if value is not None else ""
    except Exception:
        return ""

def dismiss_alert(driver, wait_time=15):
    """Waits for a JavaScript alert to appear and then dismisses it."""
    try:
        WebDriverWait(driver, wait_time).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.dismiss()
    except Exception as e:
        logger.error(f"An unexpected error occurred while trying to dismiss an alert: {e}")
        raise


def enter_text_and_accept_alert(driver, text_to_enter, wait_time=15):
    """Types text into a JavaScript prompt and then accepts the alert."""
    try:
        WebDriverWait(driver, wait_time).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.send_keys(text_to_enter)
        alert.accept()
    except Exception as e:
        logger.error(f"An unexpected error occurred while trying to enter text in an alert: {e}")
        raise


def get_performance_log_as_string(driver):
    """Retrieves and concatenates browser performance logs into a single string."""
    try:
        log_entries = driver.get_log('performance')
        all_messages = [entry.get('message', '') for entry in log_entries]
        return "".join(all_messages)
    except Exception as e:
        logger.error(f"An error occurred while trying to retrieve the performance log: {e}")
        return ""


def get_selected_option_text(element):
    """Returns the visible text of the currently selected option in a dropdown menu."""
    try:
        select_element = Select(element)
        return select_element.first_selected_option.text
    except Exception as e:
        logger.error(f"Failed to get selected option text. Element might not be a <select> dropdown. Error: {e}")
        raise


def right_click_element(driver, element):
    """Executes a right-click  action on a web element."""
    try:
        actions = ActionChains(driver)
        actions.context_click(element).perform()
    except Exception as e:
        logger.error(f"An error occurred during the right-click action: {e}")
        raise


def scroll_element_into_view(driver, element):
    """Scrolls the page until a specified element is visible in the viewport."""
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
    except Exception as e:
        logger.error(f"An error occurred while trying to scroll to an element: {e}")
        raise


def scroll_page(driver, instruction):
    """Scrolls the page down using keyboard actions like Page Down or Arrow Down."""
    normalized_instruction = instruction.lower().replace(" ", "")

    try:
        count = 1
        number_match = re.search(r'(\d+)', normalized_instruction)
        if number_match:
            count = int(number_match.group(1))
        if "pagedown" in normalized_instruction:
            logger.info(f"Scrolling by pressing PAGE_DOWN {count} time(s).")
            actions = ActionChains(driver)
            for _ in range(count):
                actions.send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(1)

        elif "downarrow" in normalized_instruction:
            logger.info(f"Scrolling by pressing ARROW_DOWN {count} time(s).")
            actions = ActionChains(driver)
            for _ in range(count):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                time.sleep(1)

        else:
            logger.info(f"Scrolling to the bottom of the page {count} time(s).")
            for _ in range(count):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

    except Exception as e:
        logger.error(f"An error occurred during the scroll action with instruction '{instruction}'. Error: {e}")
        raise


def scroll_horizontal(context, xpath, direction_count):
    """Performs a horizontal swipe action on an element to scroll left or right."""
    try:
        window_size = context.driver.get_window_size()
        window_width = window_size['width']
        x = window_width / 2

        xpath = get_frames(context, xpath)
        element = web_element(context, "xpath", xpath)
        context.element_html = get_attribute(element, "outerHTML")
        store_element_in_json(xpath, context.element_html)

        location = element.location
        xcoord = int(location['x'])
        ycoord = int(location['y'])

        scroll_times = int(re.sub('[^0-9]', '', direction_count))

        if "-" in direction_count:
            for _ in range(scroll_times):
                context.driver.swipe(x, ycoord, x + 200, ycoord, 400)
        else:
            for _ in range(scroll_times):
                context.driver.swipe(x, ycoord, x - 200, ycoord, 400)

    except Exception as e:
        logger.error(f"[Horizontal Scroll Failed] Error: {str(e)}")


def scroll_up(context, scroll_param):
    """Scrolls the page up using keyboard actions like Page Up or Arrow Up."""
    actions = ActionChains(context.driver)
    scroll_param = scroll_param.replace(" ", "").lower()

    try:
        if "pageup" in scroll_param:
            number = int(re.sub(r'\D', '', scroll_param))
            for _ in range(number):
                actions.send_keys(Keys.PAGE_UP).perform()
                time.sleep(1)

        elif "uparrow" in scroll_param:
            number = int(re.sub(r'\D', '', scroll_param))
            for _ in range(number):
                actions.send_keys(Keys.ARROW_UP).perform()
                time.sleep(1)

        else:
            number = int(scroll_param)
            for _ in range(number):
                context.driver.execute_script("window.scrollTo(300, 0);")
                time.sleep(1)

    except Exception as e:
        print(f"[scroll_up] Failed to scroll up: {e}")


def wait_for_element_to_be_invisible(context, xpath, timeout=15):
    """Waits for a specified element to become invisible or disappear from the DOM."""
    element_locator = (By.XPATH, xpath)
    WebDriverWait(context.driver, timeout).until(EC.invisibility_of_element_located(element_locator))


def wait_for_element_to_be_visible(context, xpath, timeout=15):
    """Pauses execution until a specified element becomes visible on the page."""
    element_locator = (By.XPATH, xpath)
    WebDriverWait(context.driver, timeout).until(EC.visibility_of_element_located(element_locator))


def click_element_if_visible(context, xpath, timeout=15):
    """Waits for an element to be visible and then performs a click action on it."""
    try:
        locator = (By.XPATH, xpath)
        element = WebDriverWait(context.driver, timeout).until(EC.visibility_of_element_located(locator))
        click_element(element)
    except Exception as e:
        raise Exception(
            f"[click_element_if_visible] Element not clickable or not found. Error: {str(e)}")


def close_application(context):
    """Closes the current browser window and terminates the WebDriver session."""
    try:
        if context.driver:
            context.driver.close()
            context.driver.quit()
            logger.info(context, "Application closed successfully.")
        else:
            logger.warn(context, "No active WebDriver session found to close.")
    except Exception as e:
        logger.error(context, f"Error while closing application: {str(e)}")
        raise


def close_browser_tab(context):
    """Closes the active browser tab and switches focus to the previous tab."""
    try:
        window_handles = context.driver.window_handles
        if len(window_handles) > 1:
            context.driver.switch_to.window(window_handles[-1])
            context.driver.close()
            context.driver.switch_to.window(window_handles[-2])
            logger.info(context, "Closed the current tab and switched to the previous tab.")
        else:
            logger.warn(context, "Only one tab is open; no tab was closed.")
    except Exception as e:
        logger.error(context, f"Error occurred while closing tab: {str(e)}")
        raise


def click_browser_back_button(context):
    """Navigates to the previous page in the browser's session history."""
    try:
        context.driver.back()
        logger.info(context, "Navigated back using browser back button.")
    except Exception as e:
        logger.error(context, f"Failed to navigate back: {str(e)}")
        raise



def open_new_tab_and_navigate(context, url):
    """Opens a new browser tab and navigates it to the specified URL."""
    try:
        context.driver.execute_script("window.open()")
        length = len(context.driver.window_handles)
        context.driver.switch_to.window(context.driver.window_handles[length - 1])
        context.driver.get(url)
        logger.info(context, f"Successfully opened a new tab and navigated to: {url}")
    except Exception as e:
        logger.error(context, f"Failed to open new tab and navigate to: {url} | Error: {str(e)}")
        raise Exception(f"Failed to open new tab and navigate. URL: {url}")


def mouse_hover(context, identification_type, xpath):
    """Moves the mouse cursor to hover over a specified web element."""
    i = 0
    logger.info(context, "Attempting to perform mouse hover.")

    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context,identification_type, xpath)
            context.element_html = get_attribute(element, "outerHTML")
            store_element_in_json(xpath, context.element_html)
            action = ActionChains(context.driver)
            action.move_to_element(element).perform()
            logger.info(context, "Mouse hover performed successfully.")
            return
        except Exception as e:
            logger.error(context, f"Retry {i + 1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
            time.sleep(int(context.time_interval_in_ms))
            i += 1

    logger.error(context, f"Unable to perform mouse hover after {i} retries.")
    raise Exception("Unable to perform mouse hover, XPath is: " + xpath)


def drag_and_drop_horizontal(context, xpath):
    """Performs a drag-and-drop action from a source element to a target element."""
    spilt_xpath = xpath.split("**")
    if len(spilt_xpath) != 2:
        raise ValueError("XPath should contain two parts separated by '**'")

    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            source_element = context.driver.find_element(By.XPATH, spilt_xpath[0])
            target_element = context.driver.find_element(By.XPATH, spilt_xpath[1])
            action_chains = ActionChains(context.driver)
            action_chains.drag_and_drop(source_element, target_element).perform()
            return
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i + 1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
            i += 1
    raise Exception("Unable to drag and drop horizontally")


def accept_alert_if_visible(context, timeout=5):
    """
    Accepts the alert if it is visible within the given timeout.
    """
    try:
        WebDriverWait(context.driver, timeout).until(EC.alert_is_present())
        alert = context.driver.switch_to.alert
        alert.accept()
        logger.info(context, "Alert accepted successfully.")
        return True
    except Exception as e:
        logger.error(context, "Alert not found or not visible.")
        return False



def open_new_browser(context, url):
    """Opens a new browser tab and navigates to the specified URL."""
    try:
        context.driver.execute_script(f"window.open('{url}', '_blank');")
        time.sleep(3)
        context.driver.switch_to.window(context.driver.window_handles[-1])
        logger.info(context, f"Opened new browser: {url}")
    except Exception as e:
        logger.error(context, f"Failed to open new browser: {url} | Error: {e}")


def paste_from_keyboard(context):
    """Simulates a keyboard paste action (Ctrl+V) into the currently focused element."""
    try:
        actions = ActionChains(context.driver)
        actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        logger.info(context, "Pasted value using keyboard shortcut CTRL+V.")
    except Exception as ex:
        logger.error(context, f"An error occurred while pasting from keyboard: {ex}")


def perform_copy_keyboard_action(context):
    """Simulates a 'select all' (Ctrl+A) followed by a 'copy' (Ctrl+C) keyboard action."""
    try:
        actions = ActionChains(context.driver)
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        actions.key_down(Keys.CONTROL).send_keys("c").key_up(Keys.CONTROL).perform()
        logger.info("Performed CTRL + A and CTRL + C")
    except Exception as ex:
        logger.error(f"Error while copying text: {ex}")


def double_click_random_element(context, elements):
    """Selects a random element from a list and performs a double-click action on it."""
    if not elements:
        raise Exception("No elements found to double-click.")

    random_element = random.choice(elements)
    action = ActionChains(context.driver)
    action.double_click(random_element).perform()
    logger.info(context, f"Double clicked on random element: {random_element.text}")


def double_click_element(context, xpath):
    """Performs a double-click action on a specific element identified by its XPath."""
    i = 0
    xpath = get_frames(context, xpath)  # Optional: if you use frame handling
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = web_element(context, "xpath", xpath)
            context.element_html = get_attribute(element,"outerHTML")
            store_element_in_json(xpath, context.element_html)
            action = ActionChains(context.driver)
            action.double_click(element).perform()
            logger.info(context, "Double Clicked on element")
            return  # success
        except Exception:
            logger.info(context, "No elements found")
            time.sleep(int(context.time_interval_in_ms))
            i += 1
    raise Exception("Unable to find the element, XPath is: " + xpath)


def select_copied_text_by_index(context, element, index):
    """ Selects a dropdown option using text previously stored in a list at a given index. """
    value = context.web_copied_list[int(index) - 1]
    dropdown = Select(element)
    dropdown.select_by_visible_text(value)
    logger.info(context, "Selected copied text by index: " + value)


def is_dropdown_empty(context, element):
    """ Checks if a dropdown contains only one option. Returns True if empty (only one option), else False. """
    context.element_html = get_attribute(element,"outerHTML")
    store_element_in_json(element, context.element_html)

    dropdown = Select(element)
    all_options = dropdown.options

    if len(all_options) == 1:
        logger.info(context, 'Drop down is Empty')
        return True
    else:
        logger.info(context, 'Drop down is not Empty')
        return False


def take_screenshot(context, f=None):
    """ Captures a screenshot of the current browser state and attaches it to the Allure report.  """
    date = str(datetime.now()).replace(' ', '').replace('-', '').replace(':', '').replace('.', '')
    img = context.list_tag + '_' + date
    directory = '%s/' % os.getcwd()
    temp_image = '/' + context.report_folder + '/screenshots/' + img + '.png'
    context.driver.save_screenshot(directory + temp_image)
    if f:  # Only write if a file handle is provided
        f.write("\nscreenshot|" + img + ".png|screenshot")
    allure.attach.file(
        directory + temp_image,
        name=f"Screenshot - {img}",
        attachment_type=allure.attachment_type.PNG
    )
 

def capture_screenshot(context):
    """ Captures a screenshot of the current browser state and attaches it to the html report. """
    date = str(datetime.now()).replace(' ', '').replace('-', '').replace(':', '').replace('.', '')
    img = context.list_tag + '_' + date
    directory = '%s/' % os.getcwd()
    tempimage = '/' + context.report_folder + '/screenshots/' + img + '.png'
    context.driver.save_screenshot(directory + tempimage)
    context.each_step_screenshot.append(img)

def select_dropdown_case_insensitive(context, identification, xpath, expected_text):
    expected_text = expected_text.strip().lower()
    select_element = web_element(context, identification, xpath)
    dropdown = Select(select_element)

    selected_option = dropdown.first_selected_option.text.strip().lower()
    logger.info("selected_option",selected_option)
    if selected_option.lower() == expected_text.lower():
        logger.info(context, f"Dropdown value '{expected_text}' is already selected. Skipping selection.")
        return
    for option in dropdown.options:
        actual_text = option.text.strip().lower()
        if actual_text == expected_text:
            dropdown.select_by_visible_text(option.text)
            return

    logger.info(context, f"No matching dropdown value found for: '{expected_text}'")
