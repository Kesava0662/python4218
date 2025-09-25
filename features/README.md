
## Requirements

- **Python**  
  	Make sure Python is installed and added to your system environment variables / PATH.

- **Install Required Modules Using pip**
	# Image processing and comparison
	pymupdf
	pytesseract
	Pillow
	opencv-python
	numpy

	# Clipboard and screen automation
	pyperclip
	pyautogui

	# PDF and Excel handling
	PyPDF2
	openpyxl

	# API and config
	requests
	pyyaml
	xmltodict

	# Web automation
	selenium

	# BDD and data handling
	behave
	pandas
	allure-behave

	# WebDriver Managers
	webdriver-manager
	


## Folder Structure

	project-root/
	└── features/                        # Main folder for test execution
		├── <your_feature_name>.feature  # Gherkin feature file
		├── ApplicationSettings.xml      # Runtime test configuration
    	├── ObjectRepository.yml         # YAML-based locators/test data
    	├── environment.py               # Hooks module (Behave lifecycle,Setup, screenshots & video recording logic)
    	├── steps/                       # Core automation logic
    	│   ├── common.py                # Reusable helper functions
    	│   ├── requestutil.py           # API helper functions (requests lib)
   		│   ├── assertion.py             # Soft assertion utilities
    	│   └── imagecompareutil.py      # Image comparison & verification
    	├── TestReports/                 # Generated reports (HTML, Allure, screenshots)
    	└── Temp/                        # Temporary files or screenshots



### How to Run the Test Scripts
##  All test execution commands must be run from **inside the `features/` folder**.

	# Generating Allure HTML Reports
		behave -f allure_behave.formatter:AllureFormatter -o <your-features-folder>\temp -f pretty "<your-features-folder>"
	
	# Run Specific Test Case by Tag
		behave --tags="@test001" behave -f allure_behave.formatter:AllureFormatter -o <your-features-folder>\temp -f pretty "<your-features-folder>"

	# Generating Allure Report
		allure generate --single-file <json file path> -o <output path>

