from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes_edits
import routes_navigation
import routes_all
import routes_question_thread
import routes_user_results

