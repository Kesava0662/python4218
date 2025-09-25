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
  
        
def page_loginpage_accesstopage(context):
    try:
        context.driver.get(context.url)
        logger.info(context, f"Successfully navigated to URL: {context.url}")
    except Exception as e:
        logger.error(context, f"Exception occurred while navigating to URL: {context.url} | Error: {str(e)}")
        if context.handle_timeout_error.upper() == "TRUE":
            print("Except")
    