import newspaper

def extract_article_text(url):
    # Download and parse the article
    article = newspaper.Article(url)
    article.download()
    article.parse()
    
    # Return the article's full text
    return article.text