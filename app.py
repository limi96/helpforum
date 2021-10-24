from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes.routes_edits
import routes.routes_navigation
import routes.routes_all
import routes.routes_question_thread
import routes.routes_user_results

