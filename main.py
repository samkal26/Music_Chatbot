import discord
from wit import wit_question
from music_api import get_similarity,get_track_search_save,get_tags,get_track_infos,get_track_search,get_top_songs,get_top_albums,get_top_songs_by_tag

client = discord.Client()

@client.event
async def on_ready():
    print("Le bot est prêt")

@client.event
async def on_message(message):
    
    if message.content == "!help":
        help = """
        - You can ask me to provides some information about a certain song by an artist

- Ask a song title and search for artists the made tracks wit the words

- Get the top albums or top songs of a specific artist

- Get the best songs based on tag (enter !tags to get the list)

- Tell me the songs you like and then ask for recommandation
        """
        await message.channel.send(help) 
    elif message.content == "!tags":
        for tag in get_tags():
            await message.channel.send("- " + tag)
    elif message.content == "!clear_history":
        for tag in get_tags():
            await message.channel.send("- " + tag)
    else:       
        if str(message.author) != "Bot_Music#6976":
            res = wit_question(message.content)
            for intent in res["intents"]:
                if intent["name"] == "greeting":
                    await message.channel.send("Hello " + message.author.name + " I'm feeling nice today !!")
                    await message.channel.send("I'm here to help you for your music ! Enter !help to know the things I can do")
                    
                if intent["name"] == "song_information":
                    if "song:song" in res["entities"] and "artist:artist" in res["entities"]:
                        artist = res["entities"]["artist:artist"][0]["body"]
                        track = res["entities"]["song:song"][0]["body"]

                        infos = get_track_infos(artist,track)
                        await message.channel.send(infos[0])
                        await message.channel.send(infos[1])
                    elif "song:song" in res["entities"] and "artist:artist" not in res["entities"]:
                        track = res["entities"]["song:song"][0]["body"]
                        matches = get_track_search(track)

                        for match in matches:
                            await message.channel.send("Do you mean " +match[0] + " by " + match[1] + " ?")
                            message = await client.wait_for('message')
                            
                            while message.content.lower() not in ["no","yes"]:
                                await message.channel.send("Sorry, I didn't understand your answer")
                                await message.channel.send("Do you mean " +match[0] + " by " + match[1] + " ?")
                                message = await client.wait_for('message')
                            
                            if message.content.lower() == "yes":
                                infos = get_track_infos(match[1],match[0])
                                await message.channel.send(infos[0])
                                await message.channel.send(infos[1])
                                break    
                    else:
                        await message.channel.send("Sorry, I didn't understand the song nor the artist")            
                if intent["name"] == "songs_by_artist":
                    top_count = "10"
                    if "top_count:top_count" in res["entities"]:
                        top_count = res["entities"]["top_count:top_count"][0]["body"]
                    if "artist:artist" in res["entities"]:
                        artist = res["entities"]["artist:artist"][0]["body"]

                        top_songs = get_top_songs(artist,top_count)
                        
                        index = 0
                        for song in top_songs:
                            index += 1
                            await message.channel.send("Rank " + str(index) + " - " + song)
                    else:
                        await message.channel.send("Sorry, I didn't understand the artist")
                if intent["name"] == "albums_by_artist":
                    top_count = "5"
                    if "top_count:top_count" in res["entities"]:
                        top_count = res["entities"]["top_count:top_count"][0]["body"]
                    if "artist:artist" in res["entities"]:
                        artist = res["entities"]["artist:artist"][0]["body"]

                        top_albums = get_top_albums(artist,top_count)
                        
                        index = 0
                        for album in top_albums:
                            index += 1
                            await message.channel.send("Rank " + str(index) + " - " + album)
                    else:
                        await message.channel.send("Sorry, I didn't understand the artist")
                if intent["name"] == "songs_by_tag":
                    top_count = "10"
                    if "top_count:top_count" in res["entities"]:
                        top_count = res["entities"]["top_count:top_count"][0]["body"]
                    if "tag:tag" in res["entities"]:
                        tag = res["entities"]["tag:tag"][0]["body"]

                        top_songs = get_top_songs_by_tag(tag,top_count)
                        
                        index = 0
                        for song in top_songs:
                            index += 1
                            await message.channel.send(song[0] + " - " + song[1])
                    else:
                        await message.channel.send("Sorry, I didn't understand the artist")

                if intent["name"] == "songs_liked":
                    if "song:song" in res["entities"] and "artist:artist" in res["entities"]:
                        artist = res["entities"]["artist:artist"][0]["body"]
                        track = res["entities"]["song:song"][0]["body"]

                        if get_track_search_save(artist,track,message.author.name):
                            await message.channel.send("Noted, I have added this song to your history")
                        else:
                            await message.channel.send("I couldn't find the song you like")
                    else:
                        await message.channel.send("Sorry, I didn't understand the song nor the artist")  
                if intent["name"] == "recommandations":
                    matches = get_similarity(message.author.name)

                    await message.channel.send("Hey " + message.author.name+ ", here is the top 10 songs I would recommand you listening !")
                    for match in matches:
                        await message.channel.send(match[0] + " - " + match[1])

client.run("OTU4MTA0OTY4NTAwNTEwNzQx.YkIeyQ.10sipttyTWnxCfswJQXoNiXtdRM")