import xml.etree.ElementTree as ET
from xml.dom import minidom
from token_ import Token, OperandType, TokenType

HEADER = '<?xml version="1.0" encoding="UTF-8"?>'
DTD = '''<!DOCTYPE program [ 
  <!ELEMENT program (tac+)>
  <!ELEMENT tac (dst?,src1?,src2?)>
  <!ELEMENT dst (#PCDATA)>
  <!ELEMENT src1 (#PCDATA)>
  <!ELEMENT src2 (#PCDATA)>
  <!ATTLIST program name CDATA #IMPLIED>
  <!ATTLIST tac opcode CDATA #REQUIRED>
  <!ATTLIST tac order CDATA #REQUIRED>  
  <!ATTLIST dst type (integer|string|variable|label) #REQUIRED>
  <!ATTLIST src1 type (integer|string|variable) #REQUIRED>
  <!ATTLIST src2 type (integer|string|variable) #REQUIRED>
  <!ENTITY language "IPPeCode">
  <!ENTITY eol "&#xA;">
  <!ENTITY lt "&lt;">
  <!ENTITY gt "&gt;">
]>'''


def generate_xml(tokens: list[Token], name_of_program: str) -> str:
    program = ET.Element('program', {
                         'name': name_of_program})
    order: int = 0
    for i, token in enumerate(tokens):
        if token.token_type == TokenType.OPCODE:
            order += 1
            tac = ET.SubElement(
                program, 'tac', {'opcode': token.token_value.upper(), 'order': str(order)})
            continue
        if token.operand_type == OperandType.DST:
            dst = ET.SubElement(tac, 'dst', {'type': token.token_type.value})
            dst.text = token.token_value
        elif token.operand_type == OperandType.SRC1:
            src1 = ET.SubElement(tac, 'src1', {'type': token.token_type.value})
            src1.text = token.token_value
        elif token.operand_type == OperandType.SRC2:
            src2 = ET.SubElement(tac, 'src2', {'type': token.token_type.value})
            src2.text = token.token_value

    # Create a string representation of the XML tree
    xml_string = ET.tostring(program, encoding='utf-8', method='xml')

    # Parse the XML string with minidom
    xml_pretty_str = minidom.parseString(xml_string).toprettyxml(indent="  ")

    # Replace the default XML header with the custom one
    xml_pretty_str = xml_pretty_str.replace(
        '<?xml version="1.0" ?>', HEADER + '\n' + DTD)

    # Replace colliding characters with their respective entities
    xml_pretty_str = xml_pretty_str.replace('&amp;', '&')
    xml_pretty_str = xml_pretty_str.replace('&lt;', '<')
    xml_pretty_str = xml_pretty_str.replace('&gt;', '>')
    xml_pretty_str = xml_pretty_str.replace('&quot;', '"')
    xml_pretty_str = xml_pretty_str.replace('\\n;', '$eol;')

    return xml_pretty_str
