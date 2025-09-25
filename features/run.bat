@echo off
setlocal

set PROJECT_DIR=%cd%
set REPORT_DIR=%PROJECT_DIR%\temp

echo TAG argument: %1

IF "%~1"=="" (
    echo Running all scenarios...
    behave -f allure_behave.formatter:AllureFormatter -o "%REPORT_DIR%" -f pretty "%PROJECT_DIR%"
) ELSE (
    echo Running with tag: %1
    behave -f allure_behave.formatter:AllureFormatter -o "%REPORT_DIR%" -f pretty "%PROJECT_DIR%" --tags="%1"
)
