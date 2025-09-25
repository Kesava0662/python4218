# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-raised
# pylint: disable=unused-argument

def assert_equal(context, actual, expected, message=None):
    """This method asserts that the `actual` value is equal to the `expected` value."""
    if str(context.soft_assertion).lower() == 'true':
        try:
            assert actual == expected, message
            step_name = str(context.current_step.name)
            status = 'true'
            failure_info = {'name': step_name, 'status': status}
            context.soft_failure_list.append(failure_info)
        except AssertionError:
            step_name = str(context.current_step.name)
            status = 'false'
            failure_info = {'name': step_name, 'status': status}
            context.soft_failure_list.append(failure_info)
    else:
        assert actual == expected, message


def assert_true(context, condition, message=None):
    """This method asserts that a given `condition` is true"""
    if str(context.soft_assertion).lower() == 'true':
        try:
            assert condition, message
            step_name = str(context.current_step.name)
            status = 'true'
            failure_info = {'name': step_name, 'status': status}
            context.soft_failure_list.append(failure_info)
        except AssertionError:
            step_name = str(context.current_step.name)
            status = 'false'
            failure_info = {'name': step_name, 'status': status}
            context.soft_failure_list.append(failure_info)
    else:
        assert condition, message


def assert_false(context, condition, message=None):
    """This method asserts that a given `condition` is false"""
    if str(context.soft_assertion).lower() == 'true':
        try:
            assert not condition, message
            step_name = str(context.current_step.name)
            status = 'true'
            failure_info = {'name': step_name, 'status': status}
            context.soft_failure_list.append(failure_info)
        except AssertionError:
            step_name = str(context.current_step.name)
            status = 'false'
            failure_info = {'name': step_name, 'status': status}
            context.soft_failure_list.append(failure_info)
    else:
        assert not condition, message


def assert_all(context, message=None):
    """This method is typically used to ensure that all soft assertions are evaluated at the end of the test,
     and any failures are reported as exceptions, causing the test to fail."""
    for step_info in context.soft_failure_list:
        step_name = step_info['name']
        if step_info['status'] == 'false':  # Corrected from 'false' to 'failed'
            raise Exception('Failed in step: {}'.format(step_name))
    assert True
