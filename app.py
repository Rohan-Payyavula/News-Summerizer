from flask import Flask, render_template, request
import openai
import requests

app = Flask(__name__)

# Set your API keys
NEWS_API_KEY = 'api'
OPENAI_API_KEY = 'api'
openai.api_key = OPENAI_API_KEY

def fetch_news(query="technology", page_size=5):
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get('articles', [])
    return articles

def summarize_article(article_content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize this article:\n\n{article_content}"}
        ],
        max_tokens=150
    )
    summary = response['choices'][0]['message']['content'].strip()
    return summary

@app.route('/', methods=['GET', 'POST'])
def index():
    print("Index route accessed")
    summaries = []
    query = ""
    if request.method == 'POST':
        query = request.form['query']
        print(f"Search query received: {query}")
        articles = fetch_news(query=query, page_size=5)
        for article in articles:
            content = article.get('content')
            if content:
                summary = summarize_article(content)
                print(f"Article summarized: {summary}")
                summaries.append({
                    'title': article['title'],
                    'summary': summary
                })
    return render_template('index.html', summaries=summaries, query=query)


if __name__ == '__main__':
    app.run(debug=True)

