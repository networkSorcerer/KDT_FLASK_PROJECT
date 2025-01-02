from flask import Flask
from routes.sample import subway_info, root_print

app = Flask(__name__)
app.add_url_rule('/','root_print',root_print(),methods=['GET'])
app.add_url_rule("/api/subway-data", 'subway_info',subway_info(),methods=['GET'])

if __name__ == '__main__':
    app.run()