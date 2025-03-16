from flask import Flask, request, render_template, send_file
import requests
import pandas as pd
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == "POST":
            query = request.form.get("query")
            if not query:
                return render_template("index.html", error="Please enter a keyword or phrase.")

            # Get keyword suggestions
            app.logger.debug(f"Fetching keyword suggestions for: {query}")
            keywords = get_keyword_suggestions(query)
            if not keywords:
                return render_template("index.html", error="No keywords found. Please try again.")

            # Generate metrics
            app.logger.debug("Generating metrics")
            metrics = generate_metrics(keywords)

            # Convert to DataFrame for CSV export
            df = pd.DataFrame(metrics)

            # Save to CSV
            df.to_csv("keyword_results.csv", index=False)

            return render_template("index.html", results=metrics, query=query)

        # Render the form for GET requests
        app.logger.debug("Rendering form")
        return render_template("index.html")

    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return render_template("index.html", error="An unexpected error occurred. Please try again.")

# Function to fetch keyword suggestions
def get_keyword_suggestions(query):
    url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={query}"
    response = requests.get(url, timeout=5)  # Add a timeout
    if response.status_code == 200:
        return response.json()[1]
    return []

# Function to generate dummy search volume and difficulty
def generate_metrics(keywords):
    metrics = []
    for keyword in keywords:
        metrics.append({
            "Keyword": keyword,
            "Search Volume": f"{len(keyword) * 100}",  # Dummy search volume
            "Difficulty": "Low" if len(keyword) < 10 else "Medium" if len(keyword) < 20 else "High"  # Dummy difficulty
        })
    return metrics

@app.route("/download")
def download():
    return send_file("keyword_results.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)