# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=undefined-variable
# pylint: disable=wildcard-import
# pylint: disable=unused-import

import os
import sys
from behave import *
import assertion
import home_page_workflow

current_dir = os.getcwd()
previous_dir = os.path.join(os.path.dirname(current_dir), 'shared', 'steps')
sys.path.append(previous_dir)


def parse_string(text):
    return text.strip()


register_type(Name=parse_string)
use_step_matcher("cfparse")


        

@given("I have access to application")
def step(context):
     home_page_workflow.page_loginpage_accesstopage(context)
    