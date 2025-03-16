from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Function to fetch keyword suggestions from Google Suggest API
def get_keyword_suggestions(query):
    clients = ["firefox", "chrome", "youtube"]
    all_keywords = []

    for client in clients:
        url = f"http://suggestqueries.google.com/complete/search?client={client}&q={query}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            if response.text:  # Check if the response is not empty
                keywords = response.json()[1]  # Extract the keyword suggestions
                all_keywords.extend(keywords)
            else:
                print(f"Empty response for client: {client}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching suggestions for client: {client}. Error: {e}")
        except ValueError as e:
            print(f"Invalid JSON response for client: {client}. Error: {e}")

    # If no keywords are found, use default suggestions
    if not all_keywords:
        print("Using default suggestions.")
        all_keywords = [
            f"{query} free",
            f"{query} best",
            f"{query} online",
            f"{query} 2023",
            f"{query} tool",
            f"{query} guide",
            f"{query} tips",
            f"{query} tutorial",
            f"{query} for beginners",
            f"{query} examples"
        ]

    # Remove duplicates
    all_keywords = list(set(all_keywords))
    return all_keywords

# Function to generate long-tail keywords
def get_long_tail_keywords(query):
    modifiers = [
        "free", "best", "how to", "online", "2023", "tool", "guide", "tips",
        "cheap", "easy", "quick", "top", "review", "download", "software",
        "tutorial", "for beginners", "vs", "alternatives", "examples"
    ]
    return [f"{query} {modifier}" for modifier in modifiers]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        if not query:
            return render_template("index.html", error="Please enter a keyword or phrase.")
        
        # Fetch keyword suggestions
        keywords = get_keyword_suggestions(query)
        if not keywords:
            return render_template("index.html", error="No keywords found. Please try again.")
        
        # Add long-tail keywords
        long_tail_keywords = get_long_tail_keywords(query)
        all_keywords = keywords + long_tail_keywords
        
        return render_template("index.html", results=all_keywords, query=query)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)