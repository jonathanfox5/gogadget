__author__ = "Jonathan Fox"
__copyright__ = "Copyright 2024, Jonathan Fox"
__license__ = "GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html"
__full_source_code__ = "https://github.com/jonathanfox5/gogadget"

from .config import APP_NAME
from .main import app

app(prog_name=APP_NAME)
