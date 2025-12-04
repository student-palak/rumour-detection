from newspaper import Article

def extract_text_from_url(url):
    a = Article(url)
    a.download()
    a.parse()
    return {
        "title": a.title,
        "authors": a.authors,
        "publish_date": a.publish_date,
        "text": a.text,
        "top_image": a.top_image
    }
