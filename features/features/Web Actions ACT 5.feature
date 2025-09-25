Feature: Web Actions ACT 51
#Regression Type
#Correct Values = true
#Incorrect Values = false
#Illegal Values = false
#Invalid Values = false
#Boundary Values = false
#Edge Cases Values = false

@The_Internet_3
@uida1166347387
@set21
@test001
@Add_Remove
Scenario Outline: Add Remove Elements
Given I have access to application
When I scroll and click Add Remove link in the internet
And I clicked Add Element in add remove
And I clicked Add Element in add remove
And I clicked Add Element in add remove
And I clicked Add Element in add remove
And I clicked Add Element in add remove
And I clicked Add Element in add remove
And I clicked Add Element in add remove
And I clicked Add Element in add remove
And I clicked Add Element in add remove
And I clicked Add Element in add remove
And I clicked Add Element in add remove
And I clicked Add Element in add remove
And I clicked Add Element in add remove
And I clicked Add Element in add remove
And I clicked Add Element in add remove
Then verify count Delete common_link in add remove as 'Deletecommon_link'
And verify count Delete common_TB in add remove as '<Delete common_TB1>'
When I copied count Delete common_button in add remove
Then verify copied count Delete common_label in add remove
When I copied count Delete common_link in add remove
Then verify copied count Delete common_link in add remove
When I copied count Delete common_label in add remove
Then verify copied count Delete common_label in add remove
And verify records displayed Delete common_link in add remove
And verify records less than given count Delete common_TB in add remove as '<Delete common_TB2>'
And verify matching records Delete common_TB in add remove as '<Delete common_TB3>'
And verify content in column Delete common_link in add remove as 'Deletecommon_link_1'
And verify content in column Delete common_label in add remove as 'Deletecommon_label'
And verify content in column Delete common_TB in add remove as '<Delete common_TB4>'
And verify content not displayed in column Delete common_TB in add remove as '<Delete common_TB5>'
When I click by index Delete common_button in add remove as 'Deletecommon_button'
And I copied list Delete common_link in add remove
And I click by index Delete common_link in add remove as 'Deletecommon_link_2'
And I copied list Delete common_button in add remove
And I click by last index Delete common_link in add remove
And I click by last index Delete common_label in add remove
And I click by last index Delete common_button in add remove
And I copy available records Delete common_link in add remove
And I copied list Delete common_label in add remove
And I click random Delete common_button in add remove
And I click random Delete common_link in add remove
And I click random Delete common_img in add remove
And I click until not visible Delete common_button in add remove
And I selected Add Element in add remove
And I selected Add Element in add remove
And I click until not visible Delete common_link in add remove
And I refresh until Refresh_U_button in add remove
And I refresh until Refresh_U_link in add remove
And I refresh until Refresh_U_img in add remove
And I refresh until Refresh_U_page in add remove
And I refresh until Refresh_U_label in add remove
Then '<page>' is displayed with '<content>'

Examples:
|SlNo.|Delete common_TB1|Delete common_TB2|Delete common_TB3|Delete common_TB4|Delete common_TB5|page|content|
|1|Deletecommon_TB|Deletecommon_TB_1|Deletecommon_TB|Deletecommon_TB_2|Deletecommon_TB_3|Add Remove|NA|

#Total No. of Test Cases : 1

