from lexer import Lexer
from matcher import Matcher
from parser import Parser


lexer = Lexer(r"ab*c|d")
tokens = lexer.tokenize()
parser = Parser(tokens=tokens)
ast_node = parser.parse()
matcher = Matcher(ast=ast_node)
print(matcher.findall("vijayabbckumarabbc"))

