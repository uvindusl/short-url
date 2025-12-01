import os
from flask import Flask, jsonify, request, render_template, redirect
from flask_mysqldb import MySQL
from datetime import datetime
from dotenv import load_dotenv
import uuid
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
mysql = MySQL(app)
CORS(app)

app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT", 3306)) 
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")

def genearate_short_code():
    return uuid.uuid4().hex[:8] 

@app.route("/")
def root():
    return render_template('index.html')
    # return jsonify(message="Server is running", status="success"), 200

@app.route("/shorten", methods=["POST"])
def create_short_url():
    data = request.get_json()
    if not data: 
        return jsonify(message="No data provided", status="error"), 400

    url = data.get("url")

    if not url:
        return jsonify(message="URL is required", status="error"), 400
    
    try:
        short_code = genearate_short_code() 
        created_at = datetime.now()
        updated_at = datetime.now()

        cur = mysql.connection.cursor()
        res = cur.execute(
            "INSERT INTO url (url, short_code, created_at, updated_at) VALUES (%s, %s, %s, %s)", (url, short_code, created_at, updated_at)
        )

        mysql.connection.commit()
        cur.close()

        if res > 0:              
            return jsonify({"url":url, "shortCode":short_code, "createdAt":created_at, "udpatedAt":updated_at}), 201
        else:
            return jsonify(message="Data insert unsuccessfull", status="error"), 500

    except Exception as e:
        return jsonify(message=f"Error: {str(e)}", status="error"), 500

@app.route("/shorten/<shortcode>", methods=["GET"])
def get_url_using_shortcode(shortcode):
    try:
        cur = mysql.connection.cursor()
        res = cur.execute(
            "SELECT * FROM url WHERE short_code=%s", [shortcode]
        )

        if res > 0:
            result = cur.fetchone()
            url = result[1]
            # return jsonify({"Id":id, "url":url, "shortCode":short_code, "createdAt":created_at, "udpatedAt":updated_at}), 200
            return redirect(url, 301) 

    except Exception as e:
        return jsonify(message=f"Error: {str(e)}", status="error"), 500

@app.route("/shorten/<shortcode>", methods=["PUT"])
def update_url(shortcode):
    data = request.get_json()
    if not data: 
        return jsonify(message="No data provided", status="error"), 400

    url = data.get("url")

    if not url:
        return jsonify(message="URL is required", status="error"), 400

    try:
        cur = mysql.connection.cursor()
        res = cur.execute(
            "UPDATE url SET url=%s WHERE short_code=%s", (url, [shortcode])
        )

        mysql.connection.commit()
        cur.close()

        if res > 0:
            return jsonify(message="udapte successfully", status="success"), 200
        else:
            return jsonify(message="Error", status="error"), 500

    except Exception as e:
        return jsonify(message=f"Error: {str(e)}", status="error"), 500


@app.route("/shorten/<shortcode>", methods=["DELETE"])
def delete_url(shortcode):
    try:
        cur = mysql.connection.cursor()
        res = cur.execute(
            "DELETE FROM url WHERE short_code=%s", [shortcode]
        )

        mysql.connection.commit()
        cur.close()

        if res > 0:
            return jsonify(message="delete successfully", status="success"), 200
        else:
            return jsonify(message="Error", status="error"), 500

    except Exception as e:
        return jsonify(message=f"Error: {str(e)}", status="error"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
