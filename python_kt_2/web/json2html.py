"""
json2htmlpy: A utility by Haranadh to convert JSON data into HTML tables.
"""

import json
import sys
# from bs4 import BeautifulSoup


# def beautify_html(html_content):
# """
# Parse the HTML content using BeautifulSoup
# Beautify HTML content by adding indentation and new lines.
#
# Args:
#     html_content (str): The raw HTML content to be beautified.
#
# Returns:
#     str: The beautified HTML content.
# """
# soup = BeautifulSoup(html_content, "html.parser")
#
# # Use the prettify method to beautify and indent the HTML content
# beautified_html = soup.prettify()
#
# return beautified_html


def json_to_html_table(data):
    """
    Convert JSON data to an HTML table format.

    Args:
        data (dict or list): The JSON data to be converted. Can be a dict or a list of dicts.

    Returns:
        str: The HTML table as a string.
    """
    if isinstance(data, dict):
        # Start a new table for a dictionary
        html = '<table border="1">'
        for key, value in data.items():
            html += "<tr>"
            html += f"<th>{key}</th>"
            html += "<td>"
            html += json_to_html_table(value)
            html += "</td>"
            html += "</tr>"
        html += "</table>"
    elif isinstance(data, list):
        # Create a table for a list
        html = '<table border="1">'
        for item in data:
            html += "<tr>"
            html += "<td>"
            html += json_to_html_table(item)
            html += "</td>"
            html += "</tr>"
        html += "</table>"
    else:
        # Base case: if it's not a list or dict, return as plain text
        html = str(data)

    return html


def convert_json_to_html(json_input, output_file):
    """
    Convert JSON data to an HTML table
    Convert JSON input from a file to an HTML file.

    Args:
        json_input (str): Path to the input JSON file.
        output_file (str): Path where the output HTML file will be saved.

    Returns:
        None
    """
    html_table = json_to_html_table(json_input)

    # Add the CSS for styling the table
    css_style = """
    <style>
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    </style>
    """

    # Wrap the table in basic HTML structure including the CSS style
    html_content = f"""
    <html>
    <head><title>JSON to HTML</title>
    {css_style}
    </head>
    <body>
    {html_table}
    </body>
    </html>
    """

    beautified = beautify_html(html_content)

    # Write to an HTML file
    with open(output_file, "w", encoding="utf-8") as html_file:
        html_file.write(beautified)


if __name__ == "__main__":
    json_data = {}
    # Check if the correct number of arguments are passed
    if len(sys.argv) != 3:
        print("Usage: python jsontohtml.py <input_json_file> <output_html_file>")
        sys.exit(1)

    # Get the input and output_file paths from command line arguments
    input_json_file = sys.argv[1]
    output_html_file = sys.argv[2]

    # Read the JSON data from the input file
    try:
        with open(input_json_file, "r", encoding="utf-8") as json_fp:
            json_data = json.load(json_fp)
    except FileNotFoundError as e:
        print(f"File not found.: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading or writing the file.: {e}")
        sys.exit(1)

    # Convert JSON to HTML and save the output
    convert_json_to_html(json_data, output_html_file)
    print(f"HTML table successfully generated and saved to {output_html_file}")
