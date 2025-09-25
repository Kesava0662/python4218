# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-raised
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=unused-import
import os
import re
import subprocess
import time
import glob
import json
import random
from datetime import datetime, timedelta
from collections.abc import Mapping
import pandas as pd
import pyperclip
from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from openpyxl.reader.excel import load_workbook
from percy.snapshot import percy_snapshot
from PyPDF2 import PdfReader
import common
import request_util
import image_compare_util
import logger


def attach_page(context,page_name):
    all_window_handles = context.driver.window_handles
    page_name = int(re.search(r'\d+', page_name).group())
    if 0 <= (page_name - 1) < len(all_window_handles):
        context.driver.switch_to_window(all_window_handles[int(page_name) - 1])
        return
    for handle in all_window_handles:
        context.driver.switch_to_window(handle)
        page_title = context.driver.title
        if page_name in page_title:
            break
  
        
def button_delete_common_button_copied_count(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_buttonButtonXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            links = common.web_elements(context,"XPATH",xpath)
            context.label_number = len(links)
            logger.info(context,'Copied count is : ' + str(context.label_number))
            break
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("unable to Perform this copied count",xpath)
    
def button_delete_common_button_click_by_index(context,var_deletecommon_button):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_buttonButtonXPATH",context)) 
    xpath = common.get_frames(context,xpath)
    index = str(common.get_data(context,var_deletecommon_button))
    index = int(index)
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            if 0 <= index < len(elements):
                common.click_element(elements[index])
                logger.info(context,'Clicked Delete common_button by index '+str(index))
                break
            else:
                logger.info(context,"Index {index} is out of range for the list of elements.")
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to click by index to the element , XPath is:", xpath)
     
def button_delete_common_button_copied_list(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_buttonButtonXPATH",context))
    i = 0 
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            context.web_copied_list = [common.get_text(element) for element in elements]
            logger.info(context,'Copied List : ' + str( context.web_copied_list))
            break
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to perform copied list, XPath is :",xpath)
    
def button_delete_common_button_click_by_last_index(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_buttonButtonXPATH",context))
    xpath = common.get_frames(context,xpath)
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath) 
            if elements:
                last_element = elements[-1]
                common.click_element(last_element)
                logger.info(context,"Clicked Delete common_button by last index")
            else:
                logger.info(context,"Delete common_button not found with the specified selector")
            break
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to perform click by last index, XPath is :",xpath)
    
def button_delete_common_button_click_random(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_buttonButtonXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            if elements:
                random_element = random.choice(elements)
                common.is_element_displayed(random_element)
                logger.info(context,"Clicked on random Delete common_button "+str(random_element.text))
                break
            else:
                logger.info(context,"No elements founds")
        except Exception as e:
            logger.info(context,"No elements founds")
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to click on the random element , XPath is:", xpath)
  
def button_delete_common_button_click_until_not_visible(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_buttonButtonXPATH",context))
    element_locator = (By.XPATH, xpath)
    while True:
        try:
            element = WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located(element_locator))
            common.click_element(element)
            logger.info(context, "Clicked on Delete common_button as it became visible.")
            break
        except:
            logger.error(context, "Delete common_button was not visible or click failed.")
            break
    
def image_delete_common_img_click_random(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_imgImageXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            if elements:
                random_element = random.choice(elements)
                common.is_element_displayed(random_element)
                logger.info(context,"Clicked on random Delete common_img "+str(random_element.text))
                break
            else:
                logger.info(context,"No elements founds")
        except Exception as e:
            logger.info(context,"No elements founds")
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to click on the random element , XPath is:", xpath)
  
def label_delete_common_label_verify_copied_count(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_labelLabelXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            logger.info(context,'Actual value is :' + str(len(elements)) + ' Excepted value is :' + str(context.label_number))
            if len(elements) == int(context.label_number):
                return True
            return False
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to perform verify copied count, XPath is :",xpath)
    
def label_delete_common_label_copied_count(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_labelLabelXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            links = common.web_elements(context,"XPATH",xpath)
            context.label_number = len(links)
            logger.info(context,'Copied count is : ' + str(context.label_number))
            break
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("unable to Perform this copied count",xpath)
    
def label_delete_common_label_verify_content_in_column(context,var_deletecommon_label):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_labelLabelXPATH",context))
    param = str(common.get_data(context,var_deletecommon_label))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            text_list = [common.get_text(element) for element in elements]
            if param in text_list:
                logger.info(context,"verified content in column : "+ str(param))
                return True
            logger.error(context,"Content not found ")
            return False
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to verify content in column",xpath)
    
def label_delete_common_label_click_by_last_index(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_labelLabelXPATH",context))
    xpath = common.get_frames(context,xpath)
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath) 
            if elements:
                last_element = elements[-1]
                common.click_element(last_element)
                logger.info(context,"Clicked Delete common_label by last index")
            else:
                logger.info(context,"Delete common_label not found with the specified selector")
            break
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to perform click by last index, XPath is :",xpath)
    
def label_delete_common_label_copied_list(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_labelLabelXPATH",context))
    i = 0 
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            context.web_copied_list = [common.get_text(element) for element in elements]
            logger.info(context,'Copied List : ' + str( context.web_copied_list))
            break
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to perform copied list, XPath is :",xpath)
    
def link_delete_common_link_verify_count(context,var_deletecommon_link):
    try:
        attach_page(context,'Add Remove')
    except:
        pass 
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_linkLinkXPATH",context))
    param = str(common.get_data(context,var_deletecommon_link))  
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            length = len(elements)
            logger.info(context,"Verified count is : "+str(length))
            if length == int(param):
                return True
            return False
        except Exception as e:
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception(f"Unable to find element xpath is, {xpath}")
    
def link_delete_common_link_copied_count(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_linkLinkXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            links = common.web_elements(context,"XPATH",xpath)
            context.label_number = len(links)
            logger.info(context,'Copied count is : ' + str(context.label_number))
            break
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("unable to Perform this copied count",xpath)
    
def link_delete_common_link_verify_copied_count(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_linkLinkXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            logger.info(context,'Actual value is :' + str(len(elements)) + ' Excepted value is :' + str(context.label_number))
            if len(elements) == int(context.label_number):
                return True
            return False
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to perform verify copied count, XPath is :",xpath)
    
def link_delete_common_link_verify_records_displayed(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_linkLinkXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            logger.info(context,"Actual output: Record Displayed count is : " + str(len(elements)) + ", Expected output : Record Displayed count should be greater than 0.")
            if len(elements) > 0:
                logger.info(context, f"Verification Successful: Found " + str(len(elements)) + " records.")
                return True
            logger.error(context, f"Verification Failed: Found 0 records, but expected at least 1.")
            return False
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to perform verify records displayed, XPath is :",xpath)
    
def link_delete_common_link_verify_content_in_column(context,var_deletecommon_link_1):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_linkLinkXPATH",context))
    param = str(common.get_data(context,var_deletecommon_link_1))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            text_list = [common.get_text(element) for element in elements]
            if param in text_list:
                logger.info(context,"verified content in column : "+ str(param))
                return True
            logger.error(context,"Content not found ")
            return False
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to verify content in column",xpath)
    
def link_delete_common_link_copied_list(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_linkLinkXPATH",context))
    i = 0 
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            context.web_copied_list = [common.get_text(element) for element in elements]
            logger.info(context,'Copied List : ' + str( context.web_copied_list))
            break
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to perform copied list, XPath is :",xpath)
    
def link_delete_common_link_click_by_index(context,var_deletecommon_link_2):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_linkLinkXPATH",context)) 
    xpath = common.get_frames(context,xpath)
    index = str(common.get_data(context,var_deletecommon_link_2))
    index = int(index)
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            if 0 <= index < len(elements):
                common.click_element(elements[index])
                logger.info(context,'Clicked Delete common_link by index '+str(index))
                break
            else:
                logger.info(context,"Index {index} is out of range for the list of elements.")
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to click by index to the element , XPath is:", xpath)
     
def link_delete_common_link_click_by_last_index(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_linkLinkXPATH",context))
    xpath = common.get_frames(context,xpath)
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath) 
            if elements:
                last_element = elements[-1]
                common.click_element(last_element)
                logger.info(context,"Clicked Delete common_link by last index")
            else:
                logger.info(context,"Delete common_link not found with the specified selector")
            break
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to perform click by last index, XPath is :",xpath)
    
def link_delete_common_link_copy_available_records(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_linkLinkXPATH",context))    
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            list_test = len(common.web_elements(context,"XPATH",xpath))
            context.label_number = str(list_test)
            logger.info(context,"No of Copy available record is : " + str(list_test))
            break
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("xpath is :",xpath)
    
def link_delete_common_link_click_random(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_linkLinkXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            if elements:
                random_element = random.choice(elements)
                common.is_element_displayed(random_element)
                logger.info(context,"Clicked on random Delete common_link "+str(random_element.text))
                break
            else:
                logger.info(context,"No elements founds")
        except Exception as e:
            logger.info(context,"No elements founds")
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to click on the random element , XPath is:", xpath)
  
def link_delete_common_link_click_until_not_visible(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_linkLinkXPATH",context))
    element_locator = (By.XPATH, xpath)
    while True:
        try:
            element = WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located(element_locator))
            common.click_element(element)
            logger.info(context, "Clicked on Delete common_link as it became visible.")
            break
        except:
            logger.error(context, "Delete common_link was not visible or click failed.")
            break
    
def textbox_delete_common_tb_verify_count(context,var_delete_common_tb1):
    try:
        attach_page(context,'Add Remove')
    except:
        pass 
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_TBTextBoxXPATH",context))
    param = str(common.get_data(context,var_delete_common_tb1))  
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            length = len(elements)
            logger.info(context,"Verified count is : "+str(length))
            if length == int(param):
                return True
            return False
        except Exception as e:
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception(f"Unable to find element xpath is, {xpath}")
    
def textbox_delete_common_tb_verify_records_less_than_given_count(context,var_delete_common_tb2):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_TBTextBoxXPATH",context))
    param = str(common.get_data(context,var_delete_common_tb2))
    i = 0 
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            logger.info(context,'Actual value is :' + str(len(elements)) + ' Excepted value is :' + param)
            if len(elements) < int(param):
                logger.info(context, "Verification Successful: The actual count is less than the expected count.")
                return True
            logger.error(context, f"Verification Failed: The actual count ({str(len(elements))}) is NOT less than the expected count ({param}).")
            return False
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to perform verify records less than given count, XPath is :",xpath)
    
def textbox_delete_common_tb_verify_matching_records(context,var_delete_common_tb3):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_TBTextBoxXPATH",context))    
    param = str(common.get_data(context,var_delete_common_tb3))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            logger.info(context,"Actual Values is : " + str(len(elements)) + " Excepted values is : " + param)
            if len(elements) == int(param):
                return True
            return False
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to perform verify matching records, XPath is :",xpath)
  
def textbox_delete_common_tb_verify_content_in_column(context,var_delete_common_tb4):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_TBTextBoxXPATH",context))
    param = str(common.get_data(context,var_delete_common_tb4))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            text_list = [common.get_text(element) for element in elements]
            if param in text_list:
                logger.info(context,"verified content in column : "+ str(param))
                return True
            logger.error(context,"Content not found ")
            return False
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to verify content in column",xpath)
    
def textbox_delete_common_tb_verify_content_not_displayed_in_column(context,var_delete_common_tb5):
    try:
        attach_page(context,'Add Remove')
    except:
        pass
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Deletecommon_TBTextBoxXPATH",context))
    param = str(common.get_data(context,var_delete_common_tb5))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            elements = common.web_elements(context,"XPATH",xpath)
            if len(elements) == 0:
                logger.info(context,"verified content not displayed in column")
                return True
            else:
                text_list = [common.get_text(element) for element in elements]
                if not param in text_list:
                    logger.info(context,"verified content not displayed in column")
                    return True
                logger.error(context, f"Verification Failed: Content '{param}' was found in the column, but was not expected.")
                return False
        except Exception as e:
            time.sleep(int(context.time_interval_in_ms))
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Unable to verify date format",xpath)
    
def button_refresh_u_button_refresh_until(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass    
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Refresh_U_buttonButtonXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = common.web_element(context,"XPATH",xpath)
            if common.is_element_displayed(element):
                logger.info(context, f"Refresh_U_button found on attempt {i+1}")
                break
        except Exception as e:
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
            time.sleep(int(context.time_interval_in_ms))
            context.driver.refresh()
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Element is not found")
    
def image_refresh_u_img_refresh_until(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass    
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Refresh_U_imgImageXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = common.web_element(context,"XPATH",xpath)
            if common.is_element_displayed(element):
                logger.info(context, f"Refresh_U_img found on attempt {i+1}")
                break
        except Exception as e:
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
            time.sleep(int(context.time_interval_in_ms))
            context.driver.refresh()
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Element is not found")
    
def label_refresh_u_label_refresh_until(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass    
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Refresh_U_labelLabelXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = common.web_element(context,"XPATH",xpath)
            if common.is_element_displayed(element):
                logger.info(context, f"Refresh_U_label found on attempt {i+1}")
                break
        except Exception as e:
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
            time.sleep(int(context.time_interval_in_ms))
            context.driver.refresh()
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Element is not found")
    
def link_refresh_u_link_refresh_until(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass    
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Refresh_U_linkLinkXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = common.web_element(context,"XPATH",xpath)
            if common.is_element_displayed(element):
                logger.info(context, f"Refresh_U_link found on attempt {i+1}")
                break
        except Exception as e:
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
            time.sleep(int(context.time_interval_in_ms))
            context.driver.refresh()
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Element is not found")
    
def page_refresh_u_page_refresh_until(context):
    try:
        attach_page(context,'Add Remove')
    except:
        pass    
    xpath = str(common.get_yml_object_repository_value(context.yml_data_object,"Add Remove","Refresh_U_pagePageXPATH",context))
    i = 0
    while i < int(context.max_seconds_to_wait_for_control):
        try:
            element = common.web_element(context,"XPATH",xpath)
            if common.is_element_displayed(element):
                logger.info(context, f"Refresh_U_page found on attempt {i+1}")
                break
        except Exception as e:
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
            time.sleep(int(context.time_interval_in_ms))
            context.driver.refresh()
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception("Element is not found")
    
def page_default_page_displayed(context,var_page):
    i = 0
    page =  str(common.get_data(context,var_page))
    title = context.driver.title
    if "NA" in page or "Add Remove" in page:
        return True
    else:
        all_window_handles = context.driver.window_handles
        while i < int(context.max_seconds_to_wait_for_control):
            try:
                if len(all_window_handles) > 1:
                    for handle in all_window_handles:
                        context.driver.switch_to_window(handle)
                        page_title = context.driver.title
                        if page in page_title:
                            return True
                        return False
                else:
                    if page in title:
                        return True
                    return False
            except Exception as e:
                time.sleep(int(context.time_interval_in_ms))
                logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
            i += 1
            if i >= int(context.max_seconds_to_wait_for_control):
                raise Exception(" Unable to find the element ")
    
def label_message_displayed(context,var_message):
    i = 0   
    value_to_be_enter = str(common.get_data(context,var_message)) 
    if "NA" in value_to_be_enter:
        return True
    while i < int(int(context.max_seconds_to_wait_for_control)):
        try:
            xpath = "//*[contains(text(), '" + value_to_be_enter + "')]"
            elements = common.web_elements(context, "XPATH", xpath)
            for element in elements:
                if common.is_element_displayed(element):
                    return True
        except Exception as e:
            logger.error(context, f"Retry {i+1}/{context.max_seconds_to_wait_for_control}, Error: {str(e)}")
            time.sleep(int(context.time_interval_in_ms))
        i += 1
        if i >= int(context.max_seconds_to_wait_for_control):
            raise Exception(" Unable to find the element ")
    