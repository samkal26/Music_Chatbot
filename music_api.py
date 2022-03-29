import requests

api_key = "2966a52f21f232b4195926e47799de09"
secret = "4f0498022e247e7a4a4e9669b8d89df1"

def get_track_infos(artist,track):
    url = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&artist='+artist+'&track='+track+'&api_key='+api_key+'&format=json'
    r = requests.get(url).json()
    print(url)

    if r["track"]["duration"] != "0":
        if "album" in r["track"]:
            return [r["track"]["album"]["image"][-2]["#text"] , r["track"]["wiki"]["summary"].split("<a")[0]]
        else:
            return ["No image available....", r["track"]["wiki"]["summary"].split("<a")[0]]
    else:
        return ""

def get_track_search(track):
    url = 'http://ws.audioscrobbler.com/2.0/?method=track.search&track='+track+'&api_key='+api_key+'&format=json'
    r = requests.get(url).json()
    print(url)

    matches = [(i["name"],i["artist"]) for i in r["results"]["trackmatches"]["track"]]
    return matches

def get_top_songs(artist,top_count):
    url = 'https://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist='+artist+'&limit='+top_count+'&api_key=2966a52f21f232b4195926e47799de09&format=json'
    r = requests.get(url).json()
    print(url)

    top_songs = [i["name"] for i in r["toptracks"]["track"]]
    return top_songs

def get_top_albums(artist,top_count):
    url = 'https://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist='+artist+'&limit='+top_count+'&api_key=2966a52f21f232b4195926e47799de09&format=json'
    r = requests.get(url).json()
    print(url)

    top_albums = [i["name"] for i in r["topalbums"]["album"]]
    return top_albums

def get_top_songs_by_tag(tag,top_count):
    url = 'https://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag='+tag+'&limit='+top_count+'&api_key=2966a52f21f232b4195926e47799de09&format=json'
    r = requests.get(url).json()
    print(url)

    top_songs = [[i["name"],i["artist"]["name"]] for i in r["tracks"]["track"]]
    return top_songs

def get_tags():
    url = "https://ws.audioscrobbler.com/2.0/?method=tag.getTopTags&api_key=2966a52f21f232b4195926e47799de09&format=json"
    r = requests.get(url).json()

    tags = [i["name"] for i in r["toptags"]["tag"]]
    return tags

def get_track_search_save(track,artist,user):
    url = 'http://ws.audioscrobbler.com/2.0/?method=track.search&limit=2&track='+track+'&artist='+artist+'&api_key='+api_key+'&format=json'
    r = requests.get(url).json()
    print(url)

    if(r["results"]["opensearch:totalResults"]!=0):
        
        match = [(i["name"],i["artist"]) for i in r["results"]["trackmatches"]["track"]][0]

        if user == "Samkal":
            file_object = open('history1.txt', 'a')
            file_object.write(match[0] + "/" +match[1])
            file_object.close()
        else:
            file_object = open('history2.txt', 'a')
            file_object.write(match[0] + "/" +match[1])
            file_object.close()
        return True
    else:
        return False

def get_similarity(user):
    if user == "Samkal":
        with open('history1.txt') as f:
            lines = f.readlines()
        song = lines[0].split("/") 

        url = "https://ws.audioscrobbler.com/2.0/?method=track.getsimilar&limit=10&artist="+song[0]+"&track="+song[1]+"&api_key=2966a52f21f232b4195926e47799de09&format=json"

        r = requests.get(url).json()

        matches = [(i["name"],i["artist"]["name"]) for i in r["similartracks"]["track"]]
        return matches 
    else:
        with open('history2.txt') as f:
            lines = f.readlines()
        song = lines[0].split("/") 

        url = "https://ws.audioscrobbler.com/2.0/?method=track.getsimilar&limit=10&artist="+song[0]+"&track="+song[1]+"&api_key=2966a52f21f232b4195926e47799de09&format=json"

        r = requests.get(url).json()

        matches = [(i["name"],i["artist"]["name"]) for i in r["similartracks"]["track"]]
        return matches 
