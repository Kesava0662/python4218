# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=undefined-variable
# pylint: disable=wildcard-import
# pylint: disable=unused-import

import os
import sys
from behave import *
import assertion
import add_remove_workflow

current_dir = os.getcwd()
previous_dir = os.path.join(os.path.dirname(current_dir), 'shared', 'steps')
sys.path.append(previous_dir)


def parse_string(text):
    return text.strip()


register_type(Name=parse_string)
use_step_matcher("cfparse")


        

@when("I copied count Delete common_button in add remove")
def step(context):
     add_remove_workflow.button_delete_common_button_copied_count(context)
    

@when("I click by index Delete common_button in add remove as '{var_deletecommon_button:Name?}'")
def step(context,var_deletecommon_button):
     add_remove_workflow.button_delete_common_button_click_by_index(context,var_deletecommon_button)
    

@when("I copied list Delete common_button in add remove")
def step(context):
     add_remove_workflow.button_delete_common_button_copied_list(context)
    

@when("I click by last index Delete common_button in add remove")
def step(context):
     add_remove_workflow.button_delete_common_button_click_by_last_index(context)
    

@when("I click random Delete common_button in add remove")
def step(context):
     add_remove_workflow.button_delete_common_button_click_random(context)
    

@when("I click until not visible Delete common_button in add remove")
def step(context):
     add_remove_workflow.button_delete_common_button_click_until_not_visible(context)
    

@when("I click random Delete common_img in add remove")
def step(context):
     add_remove_workflow.image_delete_common_img_click_random(context)
    

@then("verify copied count Delete common_label in add remove")
def step(context):
    assertion.assert_true(context,add_remove_workflow.label_delete_common_label_verify_copied_count(context))
    

@when("I copied count Delete common_label in add remove")
def step(context):
     add_remove_workflow.label_delete_common_label_copied_count(context)
    

@then("verify content in column Delete common_label in add remove as '{var_deletecommon_label:Name?}'")
def step(context,var_deletecommon_label):
    assertion.assert_true(context,add_remove_workflow.label_delete_common_label_verify_content_in_column(context,var_deletecommon_label))
    

@when("I click by last index Delete common_label in add remove")
def step(context):
     add_remove_workflow.label_delete_common_label_click_by_last_index(context)
    

@when("I copied list Delete common_label in add remove")
def step(context):
     add_remove_workflow.label_delete_common_label_copied_list(context)
    

@then("verify count Delete common_link in add remove as '{var_deletecommon_link:Name?}'")
def step(context,var_deletecommon_link):
    assertion.assert_true(context,add_remove_workflow.link_delete_common_link_verify_count(context,var_deletecommon_link))
    

@when("I copied count Delete common_link in add remove")
def step(context):
     add_remove_workflow.link_delete_common_link_copied_count(context)
    

@then("verify copied count Delete common_link in add remove")
def step(context):
    assertion.assert_true(context,add_remove_workflow.link_delete_common_link_verify_copied_count(context))
    

@then("verify records displayed Delete common_link in add remove")
def step(context):
    assertion.assert_true(context,add_remove_workflow.link_delete_common_link_verify_records_displayed(context))
    

@then("verify content in column Delete common_link in add remove as '{var_deletecommon_link_1:Name?}'")
def step(context,var_deletecommon_link_1):
    assertion.assert_true(context,add_remove_workflow.link_delete_common_link_verify_content_in_column(context,var_deletecommon_link_1))
    

@when("I copied list Delete common_link in add remove")
def step(context):
     add_remove_workflow.link_delete_common_link_copied_list(context)
    

@when("I click by index Delete common_link in add remove as '{var_deletecommon_link_2:Name?}'")
def step(context,var_deletecommon_link_2):
     add_remove_workflow.link_delete_common_link_click_by_index(context,var_deletecommon_link_2)
    

@when("I click by last index Delete common_link in add remove")
def step(context):
     add_remove_workflow.link_delete_common_link_click_by_last_index(context)
    

@when("I copy available records Delete common_link in add remove")
def step(context):
     add_remove_workflow.link_delete_common_link_copy_available_records(context)
    

@when("I click random Delete common_link in add remove")
def step(context):
     add_remove_workflow.link_delete_common_link_click_random(context)
    

@when("I click until not visible Delete common_link in add remove")
def step(context):
     add_remove_workflow.link_delete_common_link_click_until_not_visible(context)
    

@then("verify count Delete common_TB in add remove as '{var_delete_common_tb1:Name?}'")
def step(context,var_delete_common_tb1):
    assertion.assert_true(context,add_remove_workflow.textbox_delete_common_tb_verify_count(context,var_delete_common_tb1))
    

@then("verify records less than given count Delete common_TB in add remove as '{var_delete_common_tb2:Name?}'")
def step(context,var_delete_common_tb2):
    assertion.assert_true(context,add_remove_workflow.textbox_delete_common_tb_verify_records_less_than_given_count(context,var_delete_common_tb2))
    

@then("verify matching records Delete common_TB in add remove as '{var_delete_common_tb3:Name?}'")
def step(context,var_delete_common_tb3):
    assertion.assert_true(context,add_remove_workflow.textbox_delete_common_tb_verify_matching_records(context,var_delete_common_tb3))
    

@then("verify content in column Delete common_TB in add remove as '{var_delete_common_tb4:Name?}'")
def step(context,var_delete_common_tb4):
    assertion.assert_true(context,add_remove_workflow.textbox_delete_common_tb_verify_content_in_column(context,var_delete_common_tb4))
    

@then("verify content not displayed in column Delete common_TB in add remove as '{var_delete_common_tb5:Name?}'")
def step(context,var_delete_common_tb5):
    assertion.assert_true(context,add_remove_workflow.textbox_delete_common_tb_verify_content_not_displayed_in_column(context,var_delete_common_tb5))
    

@when("I refresh until Refresh_U_button in add remove")
def step(context):
     add_remove_workflow.button_refresh_u_button_refresh_until(context)
    

@when("I refresh until Refresh_U_img in add remove")
def step(context):
     add_remove_workflow.image_refresh_u_img_refresh_until(context)
    

@when("I refresh until Refresh_U_label in add remove")
def step(context):
     add_remove_workflow.label_refresh_u_label_refresh_until(context)
    

@when("I refresh until Refresh_U_link in add remove")
def step(context):
     add_remove_workflow.link_refresh_u_link_refresh_until(context)
    

@when("I refresh until Refresh_U_page in add remove")
def step(context):
     add_remove_workflow.page_refresh_u_page_refresh_until(context)
    

@then("'{var_page:Name?}' is displayed with '{var_content:Name?}'")
def step(context,var_page,var_content):
    assertion.assert_true(context,add_remove_workflow.page_default_page_displayed(context,var_page))
    assertion.assert_true(context, add_remove_workflow.label_message_displayed(context,var_content))
    if str(context.soft_assertion).lower() == 'true':
        assertion.assert_all(context)