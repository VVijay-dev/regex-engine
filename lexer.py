from dataclasses import dataclass
from typing import List, Optional
from enum import Enum,auto


class TokenType(Enum):
    # Quantifiers 
    QUESTION = auto()  #  Zero and one time repeat only like as works optional ?

    DOT = auto() # .  it will accept any character except new line

    PLUS = auto() # +  one or more time repeat

    STAR = auto() # *  zero or more time repeat

    DASH = auto() # - range like [0-9]

    DOLLAR = auto() # $ last word must an should be match excatly

    CARET = auto() # ^ first word must should be match or follow 

    PIPE =  auto() # | or operator which means either first or second value

    # Range quantifiers - generally used together
    # For example,
    # {n}: Matches the preceding token exactly n times.
    # {n,}: Matches the preceding token n or more times.
    # {n,m}: Matches the preceding token at least n times but no more than m times
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()

    CHAR = auto()  # Regular character (A-Z, a-z, 0-9, etc.)

    # Grouping
    # Generally has 2 purposes:
    # 1. Quantifier - (ha)+ matches "ha", "haha", "hahaha". Without parens, ha+ would match "ha", "haa", "haaa".
    # 2. Capture Grouping - to capture the matched text. For example, if we have regex like (\d{3})-(\d{4}) used on "555-1212", it captures "555" as group 1 and "1212" as group 2.
    LPAREN = auto()  # (
    RPAREN = auto()  # )

    # The escape character. It has two main jobs:
    # It removes the special meaning from a metacharacter.
    # It signals the start of a special sequence (like \d).
    # Example (Escape): To match a literal dot, you use \.. To match a literal plus sign, you use \+.
    # Example (Sequence): \d matches a digit.
    BACKSLASH = auto()  # \ (for escape sequences)


    DIGIT = auto()  # \d matches a digit (0-9)

    NON_DIGIT = auto()  # \D matches a non-digit character

    WORD = auto()  # \w matches a word character (alphanumeric or underscore)

    NON_WORD = auto()  # \W matches a non-word character

    SPACE = auto()  # \s matches a whitespace character (space, tab, newline)

    NON_SPACE = auto()  # \S matches a non-whitespace character

    # Word boundary - Matches the position between a word character (\w) and a non-word character (\W), or the start/end of the string.
    # Example: \bcat\b matches "cat" in "The cat sat" but does not match "cat" in "tomcat".
    WORD_BOUNDARY = auto()  # \b
    NON_WORD_BOUNDARY = auto()  # \B


    BACKREFERENCE = auto()  # \1, \2, etc. Matches the same text as previously matched by a capturing group.

    # Lookahead/Lookbehind markers
    LOOKAHEAD_POS = (
        auto()
    )  # (?= -> Password(?=.*[0-9]) checks if the password contains at least one digit. Example: "Password123" matches, "Password abc" does not but "Password abc 123" does. Asserts that the pattern inside (?=...) must follow the current position, but isn't part of the match.
    LOOKAHEAD_NEG = (
        auto()
    )  # (?! -> Password(?!.*[0-9]) checks if the password does not contain any digits. Example: "Password" matches, "Password123" and "Password abc 123" do not match. Asserts that the pattern inside (?!...) must NOT follow the current position, but isn't part of the match.
    LOOKBEHIND_POS = (
        auto()
    )  # (?<= -> (?<=abc) checks if the string contains "abc" before the current position. Example: "abcxyz" matches, "xyzabc" does not. Asserts that the pattern inside (?<=...) must precede the current position, but isn't part of the match.
    LOOKBEHIND_NEG = (
        auto()
    )  # (?<! -> (?<!abc) checks if the string does not contain "abc" before the current position. Example: "abcxyz" does not match, "xyzabc" matches. Asserts that the pattern inside (?<!...) must NOT precede the current position, but isn't part of the match.
    NON_CAPTURING = (
        auto()
    )  # (?: -> (?:http|https):// groups "http" and "https" for the | operator, but you can't reference it with \1. Doesnt capture anything.

    LBRACKET = auto() # [
    RBRACKET = auto() # ] 
    EOF = auto()


@dataclass
class Token:
    type:TokenType
    value:Optional[str] = None
    position: int = 0


class Lexer:
    def __init__(self,pattern):
        self.pattern = pattern 
        self.pos = 0
        self.length = len(pattern)



    
    def get_current_char(self) -> Optional[str]:
        if self.pos < self.length:
            return self.pattern[self.pos]
        return None
    


    def tokenize(self) -> List[Token]:
        tokens = []

        while self.pos < self.length:
            char = self.get_current_char()
            start_pos  = self.pos

            if char == '\\':
                token = self._handle_escape()
                if token:
                    tokens.append(token)
                continue 
            elif char == "(":
                token = self._handle_start_group()
                tokens.append(token)
            elif char == ")":
                tokens.append(Token(TokenType.RPAREN,")",start_pos))
                self.advance()
            elif char == "*":
                tokens.append(Token(TokenType.STAR ,"*",start_pos))
                self.advance()
            elif char == "?":
                tokens.append(Token(TokenType.QUESTION,"?",start_pos))
                self.advance()
            elif char == "+":
                tokens.append(Token(TokenType.PLUS,"+",start_pos))
                self.advance()
            elif char == "{":
                tokens.append(Token(TokenType.LBRACE,"{",start_pos))
                self.advance()
            elif char == "}":
                tokens.append(Token(TokenType.RBRACE,"}",start_pos))
                self.advance()
            elif char == ",":
                tokens.append(Token(TokenType.COMMA,",",start_pos))
                self.advance()
            elif char == "|":
                tokens.append(Token(TokenType.PIPE ,"|",start_pos))
                self.advance()
            elif char == "[":
                tokens.append(Token(TokenType.LBRACKET,"[",start_pos))
                self.advance()
            elif char == "]":
                tokens.append(Token(TokenType.RBRACKET,"]",start_pos))
                self.advance()
            elif char == "^":
                tokens.append(Token(TokenType.CARET,"^",start_pos))
                self.advance()
            elif char == "-":
                tokens.append(Token(TokenType.DASH,"-",start_pos))
                self.advance()
            elif char == "$":
                tokens.append(Token(TokenType.DOLLAR,"$",start_pos))
                self.advance()
            elif char == ".":
                tokens.append(Token(TokenType.DOT,".",start_pos))
                self.advance()
            else:
                tokens.append(Token(TokenType.CHAR, char,start_pos))
                self.advance()
        tokens.append(Token(TokenType.EOF,None,start_pos))
        return tokens







    
    
    def advance(self) -> Optional[str]:
        char = self.get_current_char()
        self.pos +=1
        return char
    


    def _handle_start_group(self) -> Token:
        start_pos = self.pos
        self.advance()

        

        if self.get_current_char() ==  "?":
            self.advance()

            next_char = self.get_current_char()

            if next_char == ":":
                self.advance()
                return Token(TokenType.NON_CAPTURING,"(?:",start_pos)
            elif next_char == "=":
                self.advance()
                return Token(TokenType.LOOKAHEAD_POS,"(?=",start_pos)
            elif next_char == "!":
                self.advance()
                return Token(TokenType.LOOKAHEAD_NEG,"(?!",start_pos)
            elif next_char == "<":
                self.advance()

                look_char = self.get_current_char()
                
                if look_char == "=":
                    self.advance()
                    return Token(TokenType.LOOKBEHIND_POS,"(?<=",start_pos)
                elif look_char == "!":
                    self.advance()
                    return Token(TokenType.LOOKBEHIND_NEG,"(?<!",start_pos)
                else:
                    raise ValueError(f"Invalid group syntax at position {start_pos}")

            else:
                raise ValueError(
                    f"Unknown group modifier '?{next_char}' at position {start_pos}"
                )
        else:
            self.advance()
            return Token(TokenType.LPAREN,"(",start_pos)
        
                
    
    def _handle_escape(self) -> Token:

        start_pos  = self.pos
        self.advance()

        next_char  =  self.get_current_char()

        if next_char is None:
            raise ValueError(f"pattern cannot end with backslash at position {start_pos}")

        if next_char == 'd':
            self.advance()
            return Token(TokenType.DIGIT, r"\d",start_pos)
        elif next_char == "D":
            self.advance()
            return Token(TokenType.NON_DIGIT,r"\D",start_pos)
        elif next_char == "w":
            self.advance()
            return Token(TokenType.WORD,r"\w",start_pos)
        elif next_char == "W":
            self.advance()
            return Token(TokenType.NON_WORD ,r"\W",start_pos)
        elif next_char == "s":
            self.advance()
            return Token(TokenType.SPACE ,r"\s",start_pos)
        elif next_char == "S":
            self.advance()
            return Token(TokenType.NON_SPACE, r"\S",start_pos)
        elif next_char == "b":
            self.advance()
            return Token(TokenType.WORD_BOUNDARY, r"\b",start_pos)
        elif next_char == "B":
            self.advance()
            return Token(TokenType.NON_WORD_BOUNDARY,r"\B",start_pos)
        elif next_char.isdigit():
            num = ""

            while self.get_current_char and self.get_current_char.isdigit():
                num += self.advance()
            return Token(TokenType.BACKREFERENCE,num,start_pos)
        elif next_char == "n":
            self.advance()
            return Token(TokenType.CHAR ,"\n",start_pos)
        elif next_char == "t":
            self.advance()
            return Token(TokenType.CHAR , "\t",start_pos)
        elif next_char  == "r":
            self.advance()
            return Token(TokenType.CHAR,"\r",start_pos)
        else:
            self.advance()
            return Token(TokenType.CHAR,next_char,start_pos)
        

