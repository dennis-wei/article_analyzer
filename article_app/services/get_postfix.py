def wp_post(url):
    sections = url.split('/')
    return max(sections, key=len)

def nyt_post(url):
    sections = url.split('/')
    section = filter(lambda u: '.html' in u, sections)[0]
    idx = section.find('.html')
    return section[:idx]
