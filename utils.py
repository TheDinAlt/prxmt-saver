import json

def config(value: str = None):
    with open("config.json", "r", encoding='utf-8') as f:
        file = json.load(f)
    f.close()
    if value is None:
        return file
    else:
        return file[value]
    

def count():
    with open("count.txt", "r", encoding='utf-8') as f:
        file = json.load(f)
    v = file["count"] + 1
    with open("count.txt", "w", encoding='utf-8') as f:
        f.write(str(v))
        f.close()
    
def validate_url(url):
    result = {}
    if "youtube" in url or "youtu.be" in url:
        result["service"] = "youtube"
    else:
        return False
    result["url"] = url
    return result