import flask

app = flask.Flask(__name__, template_folder="./templates", static_folder="./static")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route("/")
def main_page():
    return flask.render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
