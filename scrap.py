import newspaper

def extract_article_text(url):
    article = newspaper.Article(url)
    try:
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"Error extracting article: {str(e)}"
