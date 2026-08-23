from flask import Flask, render_template, request, jsonify
import ast
import requests

from ml.model import predict_error


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    code = data.get("code", "")

    if not code.strip():

        return jsonify({
            "success": False,
            "message": "Please enter some Python code."
        })


    # Check Python syntax

    try:

        ast.parse(code)

    except SyntaxError as error:

        return jsonify({

            "success": False,

            "status": "Syntax Error",

            "error_type": "SyntaxError",

            "explanation": error.msg,

            "line": error.lineno

        })


    # Ask the ML model for a prediction

    analysis = predict_error(code)


    return jsonify({

        "success": True,

        "status": "Analysis Complete",

        "error_type": analysis["error_type"],

        "confidence": analysis["confidence"],

        "explanation": analysis["explanation"],

        "fix": analysis["fix"],

        "line": None

    })
@app.route("/github/<username>")
def github_profile(username):

    user_url = f"https://api.github.com/users/{username}"

    user_response = requests.get(
        user_url,
        timeout=10
    )

    if user_response.status_code == 404:

        return jsonify({
            "success": False,
            "message": "GitHub user not found."
        })

    if user_response.status_code != 200:

        return jsonify({
            "success": False,
            "message": "Unable to connect to GitHub."
        })


    user_data = user_response.json()


    # Get repositories

    repo_url = (
        f"https://api.github.com/users/{username}/repos"
        "?sort=updated&per_page=6"
    )

    repo_response = requests.get(
        repo_url,
        timeout=10
    )


    repositories = []


    if repo_response.status_code == 200:

        repo_data = repo_response.json()


        for repo in repo_data:

            repositories.append({

                "name": repo.get("name"),

                "description":
                    repo.get("description"),

                "language":
                    repo.get("language"),

                "stars":
                    repo.get("stargazers_count"),

                "forks":
                    repo.get("forks_count"),

                "url":
                    repo.get("html_url")

            })


    return jsonify({

        "success": True,

        "username":
            user_data.get("login"),

        "name":
            user_data.get("name"),

        "bio":
            user_data.get("bio"),

        "avatar":
            user_data.get("avatar_url"),

        "followers":
            user_data.get("followers"),

        "following":
            user_data.get("following"),

        "repositories":
            user_data.get("public_repos"),

        "profile_url":
            user_data.get("html_url"),

        "repo_list":
            repositories

    })

if __name__ == "__main__":

    app.run(debug=True)