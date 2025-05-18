from flask_cors import CORS  # <--- import CORS
import traceback
import numpy as np

app = Flask(__name__)
CORS(app)  # <--- allow all origins (for development)
