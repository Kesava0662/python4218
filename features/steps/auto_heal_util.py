import os
from pathlib import Path
import xmltodict
import json
import xml.sax.saxutils as saxutils


def save_config_details(matching_tags_str, context):
    with open(context.log_file, "a+", encoding='utf-8') as f:
        global current_path
        current_path = os.getcwd()  # Renamed to avoid conflict with Path
        xml_path = os.path.abspath('ApplicationSettings.xml')

        with open(xml_path) as fd:
            xml_data = xmltodict.parse(fd.read())
            auto_healing = xml_data['ApplicationSettings']['AutoHealing']

            if auto_healing:
                update_xml(matching_tags_str, context)


def update_xml(matching_tags_str, context):
    target_element = get_target_from_json(context)
    object_repo_path = os.path.abspath('ObjectRepository.yml')
    working_directory = None
    os_platform = os.name

    if os_platform == 'nt':  # Windows
        appdata_path = Path(os.getenv('APPDATA'))  # Convert to Path object
        working_directory = appdata_path.parent / 'Local' / 'AlgoAF' / 'AutoHeal'/ ('web_'+matching_tags_str)
    else:  # Unix-like systems (Linux, macOS)
        working_directory = Path.home() / 'Library' / 'Application Support' / 'AlgoAF' / 'AutoHeal'/ 'web_'+matching_tags_str

    if not working_directory.exists():
        working_directory.mkdir(parents=True, exist_ok=True)

    file_path = working_directory / 'AFConfig.xml'
    web_page_path = working_directory / 'WebPage.html'

    file_content = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<Configuration>\n'
        '<AutomationType>Web</AutomationType>\n'
        '<Language_Framework>Python_Selenium</Language_Framework>\n'
        '<AutoHeal>True</AutoHeal>\n'
        f'<ObjectRepositoryFile>{saxutils.escape(object_repo_path)}</ObjectRepositoryFile>\n'
        f'<XPathKey>{saxutils.escape(context.xpath_key)}</XPathKey>\n'
        f'<XPath>{saxutils.escape(context.xpath)}</XPath>\n'
        f'<Target>{saxutils.escape(target_element)}</Target>\n'
        '<XPathUpdatedStatus>False</XPathUpdatedStatus>\n'
        '</Configuration>'
    )

    # Write the XML configuration file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)

    # Save the page source as an HTML file
    save_page_source(web_page_path, context)


def save_page_source(html_file, context):
    """Fetch and save the page source from the driver."""
    try:
        driver = context.driver  # Assuming context has a WebDriver instance
        page_source = driver.page_source  # Get the page source

        with open(html_file, "w", encoding="utf-8") as f:
            f.write(page_source)

        print("HTML data saved!")

    except Exception as e:
        print(f"Error saving page source: {e}")




def get_target_from_json(context):
    """Reads htmlElement.json, matches context.xpath with locator, and returns the corresponding target."""
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'htmlElement.json'))

    # Check if the file exists, if not, create an empty JSON file
    if not os.path.exists(json_path):
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump([], f)  # Creating an empty JSON array

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for element in data:
            if element.get("locator") == context.xpath:
                return element.get("target", "")

        print(f"No match found for XPath: {context.xpath}")
        return ""  # Return empty string if no match is found

    except Exception as e:
        print(f"Error reading json file: {e}")
        return ""
