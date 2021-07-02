from enum import Enum

class DOM_IDENTIFIER_TYPE(Enum):
    ID = "ID"
    CLASS = "CLASS"
    TEXT = "TEXT"
    OBSCURE_TEXT = "OBSCURE_TEXT"
    XPATH = "XPATH"

class DOM_ACTION(Enum):
    CLICK = "CLICK"
    FILL = "FILL"
    READ = "READ"