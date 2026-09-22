"""SEEDED ISSUE (style, warning):
Multiple style/convention violations for the Style subagent to catch:
inconsistent naming, no docstrings on public functions, unused import,
line length, and mixed quote styles.
"""

import os
import sys  # <-- seeded issue: unused import

def CalculateTotal(itemList):  # <-- seeded issue: function name should be snake_case
    total = 0
    for i in itemList:
        total = total + i['price'] * i['qty']  # <-- seeded issue: no docstring, could be more pythonic
    return total


def get_greeting(Name):  # <-- seeded issue: parameter should be lowercase
    return 'Hello, ' + Name + "!"  # <-- seeded issue: mixed quote styles
