#!c:\users\aokit\pycharmprojects\autoplaycoronavirus\venv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'chromedriver-binary==83.0.4103.14.0','console_scripts','chromedriver-path'
__requires__ = 'chromedriver-binary==83.0.4103.14.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('chromedriver-binary==83.0.4103.14.0', 'console_scripts', 'chromedriver-path')()
    )
