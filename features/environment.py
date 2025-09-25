# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=broad-exception-raised
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=no-member
import os
import shutil
import subprocess
import threading
from datetime import datetime
import cv2
import numpy as np
import pyautogui
import xmltodict
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from steps import auto_heal_util,common, log_config,logger


def before_all(context):
    def get_yml_data(file):
        return yaml.safe_load(file)

    start_time = datetime.now()
    print("before all method")
    try:
        test_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'TestData.yml'))
        with open(test_data_path, 'r', encoding='utf-8') as file:
            context.yaml_data = str(get_yml_data(file))
    except FileNotFoundError:
        context.yaml_data = None
    try:
        object_repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ObjectRepository.yml'))
        with open(object_repo_path, 'r', encoding='utf-8') as file:
            context.yml_data_object = str(get_yml_data(file))
    except FileNotFoundError:
        context.yml_data_object = None
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_experimental_option('w3c', False)
    context.chrome_options = chrome_options
    xml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ApplicationSettings.xml'))
    with open(xml_path) as fd:
        xml_data = xmltodict.parse(fd.read())
    context.aut_name = xml_data['ApplicationSettings']['URL']
    context.browser_name = xml_data['ApplicationSettings']['browserName']

    context.compare_image = xml_data['ApplicationSettings']['EnableCompareImage']
    context.failure_screenshot = xml_data['ApplicationSettings']['EnableScrenshotForFailure']
    context.passed_screenshot = xml_data['ApplicationSettings']['EnableScrenshotForSucess']
    context.all_steps_screenshot = xml_data['ApplicationSettings']['EnableScrenshotForAllSteps']
    context.recording_on_success = xml_data['ApplicationSettings']['EnableVideoCaptureForSucess']
    context.recording_on_failure = xml_data['ApplicationSettings']['EnableVideoCaptureForFailure']
    context.parallel_execution = xml_data['ApplicationSettings']['ParallelExecution']
    context.separate_failure_report = xml_data['ApplicationSettings']['EnableSeprateFailureReport']
    context.report_folder = xml_data['ApplicationSettings']['ReportFolder']
    context.incognito = xml_data['ApplicationSettings']['Incognito']
    context.max_seconds_to_wait_for_control = xml_data['ApplicationSettings'][
        'MaximumTimeInSecondsToWaitForControl']
    context.max_ms_to_wait_for_page = xml_data['ApplicationSettings'][
        'MaximumTimeInMilliSecondsToWaitForPage']
    context.url = xml_data['ApplicationSettings']['URL']
    context.file_download = xml_data['ApplicationSettings']['EnableFileDownload']
    context.browser_type = xml_data['ApplicationSettings']['BrowserType']
    context.soft_assertion = xml_data['ApplicationSettings']['EnableSoftAssertion']
    context.automation_type = xml_data['ApplicationSettings']['AutomationType']
    context.webdriver_path = xml_data['ApplicationSettings']['WebdriverPath']
    context.test_environment = xml_data['ApplicationSettings']['testEnvironment']
    context.browser_version = xml_data['ApplicationSettings']['browserVersion']
    context.platform_name = xml_data['ApplicationSettings']['platformName']
    context.user_name = xml_data['ApplicationSettings']['LT_USERNAME']
    context.access_key = xml_data['ApplicationSettings']['LT_ACCESS_KEY']
    context.logger_config = xml_data['ApplicationSettings']['Logger']
    os_version = ""
    user = ""
    report_dir = os.path.join(os.getcwd(), context.report_folder)
    screenshots_dir = os.path.join(report_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    context.log_file = os.path.join(report_dir, "Report.txt")
    with open(context.log_file, "w+", encoding="utf-8") as f:
        f.write(f"Start_Time= {start_time}")
        f.write(f"\nOS={os_version}")
        f.write(f"\nUser={user}")
        f.write(f"\nautName={context.aut_name}")
        f.write(f"\nFailureScreenshot={context.failure_screenshot}")
        f.write(f"\nSuccessScreenshot={context.passed_screenshot}")
        f.write(f"\nAllStepScreenshot={context.all_steps_screenshot}")
        f.write(f"\nseparateFailReport={context.separate_failure_report}")
    context.list_tags = []
    context.status = ''
    context.scenario_name = ''
    context.time_interval_in_ms = 1
    context.dict_api_response = {}
    context.each_step_message = []
    context.each_step_screenshot = []
    context.web_copied_list = []
    context.web_copied_key = {}
    context.soft_failure_list = []
    log_config.setup_logger(context.logger_config)
    logger.get_logger()
    logger.log_info("****************************** Starting tests... **********************")


def after_scenario(context, scenario):
    common.take_screenshot(context)
    try:
        if context.recording_on_success.upper() == "TRUE" or context.recording_on_failure.upper() == "TRUE":
            stop_recording(context)
        if context.recording_on_failure.upper() == "TRUE" and scenario.status == 'passed':
            delete_recorded_file(context)
    except Exception as e:
        print(f"Error stopping recording: {str(e)}")

    if context.status == 'failed':
        context.driver.close()
        context.driver.quit()
        context.status = ''
    else:
        list_tags = scenario.tags
        for i in list_tags:
            if i.find("set2") or i.find("set3") != -1:
                try:
                    context.driver.close()
                    context.driver.quit()
                    break
                except Exception:
                    pass
    if context.web_copied_list:
        context.web_copied_list.clear()
    logger.log_info("******Scenario ended:" + context.scenario_name + scenario.status.name.upper()+" ******")

def before_scenario(context, scenario):
    browser = str(context.browser_type).lower()
    headless = "headless" in browser
    implicit_wait_time = int(context.max_ms_to_wait_for_page)
    download_dir = os.getcwd() if str(context.file_download).lower() == "true" else None
    driver_path = context.webdriver_path
    tags = [tag.lower() for tag in scenario.tags]
    if any("api" in tag for tag in tags):
        headless = True
    if context.test_environment == 'lambdatest':
        options = webdriver.ChromeOptions()
        options.set_capability = {
            'build': 'LambdaTest Web Automation',
            'w3c': True,
            'platformName': context.platform_name,
            'browserName': context.browser_name,
            'browserVersion': context.browser_version,
        }
        url = "https://" + context.user_name + ":" + context.access_key + "@hub.lambdatest.com/wd/hub"
        context.driver = webdriver.Remote(url, options=options)
    elif context.test_environment == 'browserstack':
        url = "http://" + context.user_name + ":" + context.access_key + "@hub-cloud.browserstack.com/wd/hub"
        options = webdriver.ChromeOptions()
        options.set_capability = {
            'platformName': context.platform_name,
            'browserName': context.browser_name,
            'browserVersion': context.browser_version}
        context.driver = webdriver.Remote(command_executor=url, options=options)
    else:
        if driver_path and "na" not in driver_path.lower():
            if "firefox" in browser:
                driver_path = os.path.join(driver_path, "geckodriver.exe")
            elif "edge" in browser:
                driver_path = os.path.join(driver_path, "msedgedriver.exe")
            else:  # Default to Chrome
                driver_path = os.path.join(driver_path, "chromedriver.exe")
        else:
            driver_path = None  # Ignore the path if it contains "na"
        if "firefox" in browser:  # Firefox setup
            context.firefox_options = FirefoxOptions()
            if headless:
                context.firefox_options.add_argument("--headless")
            if str(context.incognito).lower() == "true":
                context.firefox_options.add_argument("-private-window")
            if download_dir:
                profile = webdriver.FirefoxProfile()
                profile.set_preference("browser.download.folderList", 2)
                profile.set_preference("browser.download.dir", download_dir)
                profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
                profile.set_preference("pdfjs.disabled", True)
                context.firefox_options.profile = profile
            if driver_path and os.path.exists(driver_path):
                service = FirefoxService(executable_path=driver_path)  # Use manual driver path
            else:
                service = FirefoxService(GeckoDriverManager().install())  # Use WebDriverManager
            context.driver = webdriver.Firefox(service=service, options=context.firefox_options)
        elif "edge" in browser:  # Edge setup
            context.edge_options = EdgeOptions()
            if headless:
                context.edge_options.add_argument("--headless")
            if str(context.incognito).lower() == "true":  # Add InPrivate browsing
                context.edge_options.add_argument("--inprivate")
            context.edge_options.use_chromium = True
            if download_dir:
                context.edge_options.add_experimental_option('prefs', {
                    "download.default_directory": download_dir,
                    "download.prompt_for_download": False,
                    "directory_upgrade": True,
                    "safebrowsing.enabled": True
                })
            if driver_path and os.path.exists(driver_path):
                service = EdgeService(executable_path=driver_path)  # Use manual driver path
            else:
                service = EdgeService(EdgeChromiumDriverManager().install())  # Use WebDriverManager
            context.driver = webdriver.Edge(service=service, options=context.edge_options)
        else:  # Chrome setup (default)
            context.chrome_options = ChromeOptions()
            if str(context.incognito).lower() == "true":
                context.chrome_options.add_argument('--incognito')
            context.chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
            context.chrome_options.add_experimental_option("perfLoggingPrefs", {"enableNetwork": True})
            if headless:
                context.chrome_options.add_argument("--headless")
            if download_dir:
                context.chrome_options.add_experimental_option('prefs', {
                    "download.default_directory": download_dir,
                    "download.prompt_for_download": False,
                    "directory_upgrade": True,
                    "safebrowsing.enabled": True
                })
            if driver_path and os.path.exists(driver_path):
                service = ChromeService(executable_path=driver_path)  # Use manual driver path
            else:
                service = ChromeService(ChromeDriverManager().install())  # Use WebDriverManager
            context.driver = webdriver.Chrome(service=service, options=context.chrome_options)
    context.driver.implicitly_wait(implicit_wait_time)
    context.driver.maximize_window()
    context.parent_window_handle = context.driver.current_window_handle
    context.step_number = 0
    context.list_tags = scenario.tags
    context.scenario_name = scenario.name
    context.list_tag = ""
    for i in context.list_tags:
        if "test" in i:
            context.list_tag = i
    if context.recording_on_success.upper() == "TRUE" or context.recording_on_failure.upper() == "TRUE":
        start_recording(context)
    logger.log_info(
        "****************************** TAGS: " + ', '.join(context.list_tags) + " ******************************")
    logger.log_info("****** Scenario started: " + context.scenario_name + " ******")


def before_step(context, step):
    context.current_step = step
    logger.log_info("****** Step started:" + str(context.current_step) + "******")


def after_step(context, step):
    context.step_number = context.step_number + 1
    with open(context.log_file, "a+", encoding="utf-8") as f:
        f.write("\n" + str(context.list_tags))
        f.write("\n" + str(context.scenario_name))
        f.write("\n" + str(step) + "StepNumber|" + str(context.step_number) + "|StepNumber")
        if context.all_steps_screenshot == "True":
            common.take_screenshot(context,f)
        else:
            if context.failure_screenshot == "True" and step.status == 'failed':
                common.take_screenshot(context,f)
            if context.passed_screenshot == "True" and "then" in str(step) and step.status == 'passed':
                common.take_screenshot(context,f)
        logger.log_info(
            "****** Step ended: " + str(context.current_step) + " | Status:" + step.status.name.upper() + "******")
        if context.each_step_screenshot:
            for message in context.each_step_screenshot:
                single_line_message = message.replace("\n", " ").replace("\r", " ") 
                multi_screenshot = "screenshot|" + single_line_message + ".png|screenshot"
                f.write("\n" + multi_screenshot)
            context.each_step_screenshot.clear()
        if context.each_step_message:
            for message in context.each_step_message:
                single_line_message = message.replace("\n", " ").replace("\r", " ")
                f.write("\nMessage|" + single_line_message + "|Message")
            context.each_step_message.clear()
    if step.status == 'failed':

            # matching_tags = [tag for tag in context.list_tags if "uid" in tag]
            # matching_tags_str = matching_tags[0] if matching_tags else ""
            auto_heal_util.save_config_details(context.list_tags[0], context)


def after_all(context):
    end_time = datetime.now()
    f = open(context.log_file, "a+", encoding='utf-8')
    f.write(f"\nEnd_Time={end_time}")
    f.close()
    try:
        if str(context.automation_type).lower().replace(" ", "").__contains__("ios"):
            report_folder = os.getcwd() + "/TestReports"
            if not os.path.exists(report_folder):
                os.makedirs(report_folder)
            final_report_file = report_folder + "/TestReport_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            if not os.path.exists(final_report_file):
                os.makedirs(final_report_file)
            old_path = os.getcwd() + "/Temp"
            file_names = os.listdir(old_path)
            for file_name in file_names:
                shutil.move(os.path.join(old_path, file_name), final_report_file)
            os.rmdir(old_path)
            report_path = final_report_file + "/report.html"
            allure_path = os.getcwd() + "/reports" + "/allure_report"
            cmd_command = ('mono algoReport.exe behave "' + final_report_file + '" "' + report_path + '" && ''allure generate --clean --single-file "' + final_report_file + '" ''-o "' + allure_path + '"' )
            target_directory = os.getcwd()
            os.chdir(target_directory)
            subprocess.run(cmd_command, shell=True, check=True)
        else:
            report_folder = os.getcwd() + "\\TestReports"
            if not os.path.exists(report_folder):
                os.makedirs(report_folder)
            final_report_file = report_folder + "\\TestReport_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            if not os.path.exists(final_report_file):
                os.makedirs(final_report_file)
            old_path = os.getcwd() + "\\Temp"
            file_names = os.listdir(old_path)
            for file_name in file_names:
                shutil.move(os.path.join(old_path, file_name), final_report_file)
            os.rmdir(old_path)
            report_path = final_report_file + "\\report.html"
            allure_path = os.getcwd() + "/reports" + "/allure_reports"
            cmd_command = ('algoReport.exe behave "' + final_report_file + '" "' + report_path + '" && ''allure generate --clean --single-file "' + final_report_file + '" ''-o "' + allure_path + '"')
            target_directory = os.getcwd()
            os.chdir(target_directory)
            subprocess.run(cmd_command, shell=True, check=True)
            json_files = [f for f in os.listdir(final_report_file) if f.endswith(".json")]
            if json_files:
                subprocess.run(["pdfReport.exe", report_path], check=True)
    except Exception as e:
        print(f"Exception------------ {e}")


def start_recording(context):
    try:
        name = str(context.scenario_name).replace(" ", '_')
        # date = datetime.now().strftime('%Y%m%d_%H%M%S')
        screen_recording_dir = os.path.join(context.report_folder, "ScreenRecordings")
        os.makedirs(screen_recording_dir, exist_ok=True)
        context.video_path = os.path.join(screen_recording_dir, f"{name}.mp4")
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        context.video_writer = cv2.VideoWriter(context.video_path, fourcc, 20.0,
                                               (screen_size.width, screen_size.height))
        if not context.video_writer.isOpened():
            raise Exception("VideoWriter failed to open")
        context.is_recording = True
        context.recording_thread = threading.Thread(target=record_screen, args=(context,))
        context.recording_thread.start()
    except Exception as e:
        print(f"Error starting recording: {e}")


def record_screen(context):
    try:
        while context.is_recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            context.video_writer.write(frame)
    except Exception as e:
        print(f"Error during screen recording: {e}")


def stop_recording(context):
    try:
        if hasattr(context, 'is_recording') and context.is_recording:
            context.is_recording = False
            if hasattr(context, 'recording_thread'):
                context.recording_thread.join()
            if hasattr(context, 'video_writer'):
                context.video_writer.release()
    except Exception as e:
        print(f"Error stopping recording: {e}")


def delete_recorded_file(context):
    try:
        if hasattr(context, 'video_path') and os.path.exists(context.video_path):
            os.remove(context.video_path)
    except Exception as e:
        print(f"Error deleting video file: {e}")
