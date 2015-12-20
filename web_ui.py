from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/events/<event_id>')
def event(event_id):
    pass

@app.route('/persons/<person_id>')
def person(person_id):
    pass

if __name__ == '__main__':
    app.run()

