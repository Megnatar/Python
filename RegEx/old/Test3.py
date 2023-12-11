from re import findall as RegexFindall
from re import match as RegexMatch
from re import sub as RegexSub
import re
import requests
import os
import unicodedata as unc
import encodings
import codecs 
from time import sleep
from time import perf_counter
from random import uniform
assignment_expression = 1
try_stmt  ::=  try1_stmt | try2_stmt
try1_stmt ::=  "try" ":" suite
               ("except" [expression ["as" identifier]] ":" suite)+
               ["else" ":" suite]
               ["finally" ":" suite]
try2_stmt ::=  "try" ":" suite
               "finally" ":" suite

