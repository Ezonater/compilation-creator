import re
def valid_link(link):
    if re.search('(?:https?:\\/\\/)?(?:www\\.)?youtu\\.?be(?:\\.com)?\\/?.*(?:watch|embed)?(?:.*v=|v\\/|\\/)([\\w\\-_]+)\\&?', link):
        return True
    else: return False
