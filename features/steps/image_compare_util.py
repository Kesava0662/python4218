# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-raised
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=no-member
# pylint: disable=consider-using-f-string

import os
import os.path
import time

import cv2
import numpy as np
from numpy import diff
from PIL import Image, ImageChops, ImageStat
import common
import pyautogui


def save_image(context, image_name, compare_image):
    """This method saves a screenshot of the current browser window,
    optionally renaming and cropping the image based on a comparison condition."""
    directory = f"{os.getcwd()}/"
    common.delete_files(directory + "/steps/images/temp")
    temp_image_path = f"/steps/images/temp/{image_name}.png"
    context.driver.save_screenshot(directory + temp_image_path)
    file_name = ''
    try:
        if eval(compare_image):
            file_name = f'/steps/images/compare/{image_name}.png'
            common.rename_file(directory + '/steps/images/compare', image_name)
        else:
            file_name = f'/steps/images/baseline/{image_name}.png'
            common.rename_file(directory + '/steps/images/baseline', image_name)
    except:
        pass
    img = cv2.imread(directory + temp_image_path)
    height, width, _ = img.shape
    crop_img = img[200:(height - 100), 0:width]
    cv2.imwrite(directory + file_name, crop_img)


def crop_image(context):
    """This method captures the current browser window size and crops a specific region from a saved screenshot."""
    size = context.driver.get_window_size(context.driver.current_window_handle)
    directory = f'{os.getcwd()}/'
    file_name = '/steps/images/compare/screenshot.png'
    img = cv2.imread(directory + file_name)
    height, width, _ = img.shape
    crop_img = img[200:(height - 100), 0:width]
    cv2.imwrite(directory + '/steps/images/compare/screenshot1.png', crop_img)


def mse(image_a, image_b):
    """The 'Mean Squared Error' between the two images is the
    sum of the squared difference between the two images."""
    # NOTE: the two images must have the same dimension
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])
    return err


def diff_remove_bg(img0, img, img1):
    """This method calculates the difference between three images and
    returns the bitwise AND of the differences to remove background noise."""
    d1 = diff(img0, img)
    d2 = diff(img, img1)
    return cv2.bitwise_and(d1, d2)


def compare_images(context, image_name, tolerance=10):
    """This method compares two images, calculates differences, and
    saves the results, returning True if the images are identical."""
    baseline_images_path = os.path.join(os.getcwd(), 'steps', 'images', 'baseline')
    os.makedirs(baseline_images_path, exist_ok=True)
    compare_images_path = os.path.join(os.getcwd(), 'steps', 'images', 'compare')
    os.makedirs(compare_images_path, exist_ok=True)
    if str(context.compare_image).lower() == 'false':
        baseline_image = os.path.join(baseline_images_path, f"{image_name}.png")
        context.driver.save_screenshot(baseline_image)
        return True
    else:
        compare_base_image = os.path.join(compare_images_path, f"{image_name}.png")
        context.driver.save_screenshot(compare_base_image)
        image_a_path = os.getcwd() + '/steps/images/baseline/' + image_name + '.png'
        image_b_path = os.getcwd() + '/steps/images/compare/' + image_name + '.png'
        img_a = Image.open(image_a_path)
        img_b = Image.open(image_b_path)
        if img_a.size != img_b.size:
            return False
        diff_image = ImageChops.difference(img_a, img_b)
        stat = ImageStat.Stat(diff_image)
        diff_mean = stat.mean[0]
        if diff_mean <= tolerance:
            return True
        else:
            return False

def verify_by_image(context, image_name,tolerance = 10):
    baseline_images_path = os.path.join(os.getcwd(), 'steps', 'images', 'baseline')
    os.makedirs(baseline_images_path, exist_ok=True)
    baseline_image = os.path.join(baseline_images_path, f"{image_name}.png")
    context.driver.save_screenshot(baseline_image)
    image_a_path = os.getcwd() + '/steps/images/baseline/' + image_name + '.png'
    image_b_path = os.getcwd() + '/steps/images/' + image_name + '.png'
    img_a = Image.open(image_a_path)
    img_b = Image.open(image_b_path)
    if img_a.size != img_b.size:
        return False
    diff_image = ImageChops.difference(img_a, img_b)
    stat = ImageStat.Stat(diff_image)
    diff_mean = stat.mean[0]
    if diff_mean <= tolerance:
        return True
    else:
        return False

def select_by_image(context,text):
    i = 0
    while i < int(context.maximum_time_in_seconds_to_wait_for_control):
        try:
            text_split = text.split(',')
            image_name = text_split[0]
            y_axis = int(text_split[1]) if len(text_split) > 1 and text_split[1] else 0
            x_axis = int(text_split[2]) if len(text_split) > 2 and text_split[2] else 0
            screenshot_path = os.path.join(os.getcwd(), "screenshot.png")
            context.driver.save_screenshot(screenshot_path)
            image_path = os.path.join(os.getcwd() + "/steps/images/" + image_name)
            screenshot = cv2.imread(screenshot_path)
            template = cv2.imread(image_path)
            if screenshot is None or template is None:
                raise ValueError("Failed to load screenshot or template image.")
            else:
                result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)
                if max_val < 0.8:
                    raise ValueError("Template not found with sufficient confidence.")
                coordinates = max_loc
                x = coordinates[0] + x_axis
                y = coordinates[1] + y_axis
                pyautogui.moveTo(x, y, duration=0.5)
                try:
                    pyautogui.click()
                    time.sleep(2)
                    os.remove(screenshot_path)
                    break
                except:
                    context.driver.execute_script("arguments[0].click()", pyautogui)
                    os.remove(screenshot_path)
                    break
        except:
            time.sleep(int(context.time_interval_in_milli_seconds))
            i += 1
        if i >= int(context.maximum_time_in_seconds_to_wait_for_control):
            raise Exception("Unable to enter in Text Box")