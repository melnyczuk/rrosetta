import sys
from flask import Flask
import citation_json
import img_anal
import txt_anal

app = Flask(__name__)
noun = sys.argv[1]

@app.route('/')
def html():
    return 'Hello, world?'

@app.route(r'^/$')
def takenoun():
    citation_json.main(noun, "citation_jsons")
    img_anal.analyse(noun)
    txt_anal.analyse(noun)

if __name__ == '__main__':
    app.config['noun'] = sys.argv[1]
    app.run()
    html()
    takenoun()