"""
After the mandatory XML header5
, the root element program (including mandatory text attribute
language with value IPPeCode) follows. The root element consists of elements tac for individual
instructions. Every tac element includes the mandatory order attribute that holds the order of the
instruction (unbroken sequence starting with 1, no leading zeros) and the mandatory opcode attribute
storing the value of operation code always written in upper case. In addition, tac element contains
the elements for the operands/arguments of the instruction: dst for the destination operand, src1 for
the potential first source operand and src2 for the second potential operand. The operand elements
include mandatory attribute type with possible values: integer, string, label, and variable
determining that the contained textual element represents integer literal, string literal (without the
surrounding quotation marks), label (including @ at the beginning), or variable name, respectively.
There is no conversion of the integer values (do not throw away even plus sign) before their write
up into XML. For string literal, leave escape sequences untouched, convert only colliding characters
because of XML format (i.e., <, >, & using XML entities &lt;, &gt;, &amp;). Resolve the problematic
characters in identifiers as well.
A string literal is just a content of the corresponding XML element with attribute type="string".
The end of line cannot be represented in a string literal.
"""
import xml.etree.ElementTree as ET
from token_ import TokenType, OperandType, Token
from lexical_tokenizer import LexicalTokenizer
from exception_handler import ExceptionHandler

from xml.dom import minidom


def generate_xml(tokens: list[Token]):
    program = ET.Element('program', {'language': 'IPPeCode'})
    for i, token in enumerate(tokens):
        tac = ET.SubElement(program, 'tac', {'order': str(
            i+1), 'opcode': token.token_value.upper()})
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

    # Write the pretty XML string to the output file
    with open('output.xml', 'w') as f:
        f.write(xml_pretty_str)
