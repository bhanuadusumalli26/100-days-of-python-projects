from bs4 import BeautifulSoup
import requests

# Fetch the web page
response = requests.get("https://news.ycombinator.com/news")
yc_web_page = response.text
soup = BeautifulSoup(yc_web_page, "html.parser")

# Extract articles and links
articles = soup.find_all(name="a", class_="titlelink")
article_texts = []
article_links = []

for article_tag in articles:
    text = article_tag.getText()
    link = article_tag.get("href")
    article_texts.append(text)
    article_links.append(link)

# Extract upvotes
article_upvotes = []
for score_tag in soup.find_all(name="span", class_="score"):
    try:
        upvotes = int(score_tag.getText().split()[0])  # Convert to integer
        article_upvotes.append(upvotes)
    except ValueError:
        article_upvotes.append(0)  # Fallback in case of parsing error

# Ensure the lists align in length
if len(article_texts) != len(article_upvotes):
    print("Warning: Mismatch between articles and upvotes!")
    article_upvotes = article_upvotes[
        : len(article_texts)
    ]  # Truncate to match articles

# Identify the article with the most upvotes
if article_upvotes:  # Ensure upvotes list is not empty
    largest_index = article_upvotes.index(max(article_upvotes))
    print("Most Upvoted Article:")
    print(article_texts[largest_index])
    print(article_links[largest_index])
else:
    print("No upvotes found on the page.")
