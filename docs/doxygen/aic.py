import xml.etree.ElementTree as ET
import os
import re 

def recursive_text(element):
    text = element.text or ""
    for child in element:
        text += recursive_text(child)
    text += element.tail or ""
    return text.strip()

def sanitize_class_name(class_name):
    # Remove invalid characters from the class name and replace with underscores
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', class_name)
    return sanitized_name

def generate_brief_context(xml_content):

    # Read the XML file
    xml_string = open(xml_content, 'r').read()

    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Initialize an empty string to collect the output
    output = ""

    # Extract the relevant information
    for compounddef in root.findall(".//compounddef[@kind='class']"):
        class_name = compounddef.find('compoundname').text
        # Sanitize the class name
        class_name = sanitize_class_name(class_name)

        output += f"About the class {class_name}\n"
        
        output += "#Classes\n"
        for innerclass in compounddef.findall(".//innerclass"):
            output += f"{innerclass.text} \n"
        
        output += "#Public Member Functions\n"
        for func in compounddef.findall(".//sectiondef[@kind='public-func']/memberdef"):
            briefdesc = func.find('briefdescription')
            if briefdesc is not None:
                output += f"{func.find('name').text}: {recursive_text(briefdesc)}\n"
            else:
                output += f"{func.find('name').text}: \n"
                
        output += "#Public Attributes\n"
        for attr in compounddef.findall(".//sectiondef[@kind='public-attrib']/memberdef"):
            briefdesc = attr.find('briefdescription')
            if briefdesc is not None:
                output += f"{attr.find('name').text}: {recursive_text(briefdesc)}\n"
            else:
                output += f"{attr.find('name').text}: \n"

    # Construct the output filename with underscores
    output_filename = f"./aidocs/{class_name}.md"
    
    # Write the output to a file
    with open(output_filename, 'w') as f:
        f.write(output)
        
def generate_detailed_context(xml_content):

    # Your XML file path
    xml_content = './doxml/classAudioProcessorValueTreeState.xml'

    # Read the XML file
    xml_string = open(xml_content, 'r').read()

    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Initialize an empty string to collect the output
    output = ""

    # Extract the relevant information
    for compounddef in root.findall(".//compounddef[@kind='class']"):
        class_name = compounddef.find('compoundname').text
        # Replace double colons with underscores in the class name
        class_name = class_name.replace("::", "_")

        output += f"About the class {class_name}\n"
        
        output += "#Classes\n"
        for innerclass in compounddef.findall(".//innerclass"):
            output += f"{innerclass.text}: Connects a {innerclass.text.split('::')[-1]} to a parameter.\n"
        
        output += "#Public Member Functions\n"
        for func in compounddef.findall(".//sectiondef[@kind='public-func']/memberdef"):
            briefdesc = func.find('detaileddescription')
            if briefdesc is not None:
                output += f"{func.find('name').text}: {recursive_text(briefdesc)}\n"
            else:
                output += f"{func.find('name').text}: \n"
                
        output += "#Public Attributes\n"
        for attr in compounddef.findall(".//sectiondef[@kind='public-attrib']/memberdef"):
            briefdesc = attr.find('detaileddescription')
            if briefdesc is not None:
                output += f"{attr.find('name').text}: {recursive_text(briefdesc)}\n"
            else:
                output += f"{attr.find('name').text}: \n"
        
        output += "#Notes\n"
        output += "The class is not realtime-safe for certain operations.\n"

    # Write the output to a file using the path doxygen/compounddef/compoundname as the filename
    with open(f"./aidocs/{compounddef.find('compoundname').text}.md", 'w') as f:
        f.write(output)

def process_xml_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml') and filename.startswith('class'):
            generate_brief_context('./doxml/'+filename)

            
# Your XML file path
process_xml_files_in_folder('./doxml')