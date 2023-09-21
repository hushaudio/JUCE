import os
import xml.etree.ElementTree as ET

# Simulated Doxygen XML for demonstration
doxygen_xml = '''
<root>
    <class name="RangedAudioParameter" parent="">
        <summary>Abstract base class used in AudioProcessorParameter helper classes.</summary>
        <function name="getNormalisableRange">Gets the range of values for the parameter.</function>
        <function name="getNumSteps">Returns the number of steps based on the normalisable range.</function>
    </class>
    <class name="AudioParameterFloat" parent="RangedAudioParameter">
        <summary>Derived from RangedAudioParameter, handles float parameters.</summary>
        <function name="fromString">Converts a string to a float.</function>
    </class>
    <!-- More classes -->
</root>
'''

# Parse the XML
root = ET.fromstring(doxygen_xml)

# Create a directory to store the .md files
output_dir = '/mnt/data/class_docs'
os.makedirs(output_dir, exist_ok=True)

# Extract information and write to .md files
for class_elem in root.findall('class'):
    class_name = class_elem.get('name')
    parent_class = class_elem.get('parent')
    class_summary = class_elem.find('summary').text
    
    # Create a markdown content string
    md_content = []
    md_content.append(f"# {class_name} Class")
    
    if parent_class:
        md_content.append(f"**Parent Class**: {parent_class}\n")
    
    md_content.append(f"- {class_summary}\n")
    md_content.append("## Public Functions\n")
    
    for func_elem in class_elem.findall('function'):
        func_name = func_elem.get('name')
        func_desc = func_elem.text
        md_content.append(f"- `{func_name}`: {func_desc}\n")
    
    # Write the markdown content to a .md file
    md_file_path = os.path.join(output_dir, f"{class_name}.md")
    with open(md_file_path, 'w') as md_file:
        md_file.write('\n'.join(md_content))
