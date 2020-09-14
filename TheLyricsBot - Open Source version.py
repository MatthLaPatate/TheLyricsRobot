


############################
##### The Lyrics Robot #####
##### By @MatthLaPatate ####
#####    (on Twitter)  #####
############################



### Importing ###

import tweepy
from time import sleep
import lyricsgenius


### Launch Robot print ###

print('The Lyrics Robot ! \n')


### Twitter Keys & Tokens ###

consumer_key='' # Our consumer_key
consumer_secret='' # Our consuumer_secret
access_key='' # Our access_key
access_secret='' # Our access_secret


### Twitter API set ###

auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api=tweepy.API(auth)


### Genius Keys & Tokens ###

genius_access_token = '' # Our genius_access_token


### Genius API set ###

genius = lyricsgenius.Genius(genius_access_token)
genius.skip_non_songs = True
genius.excluded_terms = ['(Live)', '(Remix)', 'Remix', '(Show)', '(Music awards)', '(Victoire de la musique)', '(Accapella)']

### Create var ###

FILE_NAME = '.txt' # Our .txt file with an id (you can use: 1300371234081968129)

Lyrics = ''



### Functions ###

def retrieve_last_seen_id(file_name): # Retrieve the last seen id

    f_read = open(file_name, 'r')

    last_seen_id = int(f_read.read().strip())

    f_read.close()

    return last_seen_id



def store_last_seen_id(last_seen_id, file_name): # Write the new last seen id

    f_write = open(file_name, 'w')

    f_write.write(str(last_seen_id))

    f_write.close()

    return



def retrieve_initial_tweet(ID_INITIAL_TWEET):

    initial_tweet = api.get_status(ID_INITIAL_TWEET)
    print(str(initial_tweet.text))

    return str(initial_tweet.text)




def search_song(LYRICS_OF_SONG):
    song_title = genius.search_genius_web(LYRICS_OF_SONG,1)

    # We search to know if genius has find a answer or not, if not : all components of song_title are empty, else : return the song_response

    if song_title == {'sections': [{'type': 'top_hit', 'hits': []}, {'type': 'song', 'hits': []}, {'type': 'lyric', 'hits': []}, {'type': 'artist', 'hits': []}, {'type': 'album', 'hits': []}, {'type': 'video', 'hits': []}, {'type': 'article', 'hits': []}, {'type': 'user', 'hits': []}]}:
        pass

    else :
        print(song_title['sections'][0]['hits'][0]['result']['title_with_featured']) # print title with featured
        print(song_title['sections'][0]['hits'][0]['result']['primary_artist']) # print artist
        song_response = str('Le titre est ' + "'" + song_title['sections'][0]['hits'][0]['result']['title_with_featured'] + "'" # create a response (french)
                            + ' par le phénomène ' + song_title['sections'][0]['hits'][0]['result']['primary_artist']['name'])

        return song_response




### Main Function ###

def reply_to_tweets():

    print('retrieving and replying to tweets...', flush=True)

    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    # NOTE: We need to use tweet_mode='extended' below to show all full tweets (with full_text). Without it, long tweets would be cut off.

    mentions = api.mentions_timeline(

                        last_seen_id,

                        tweet_mode='extended')

    for mention in reversed(mentions):

        print(str(mention.id) + ' - ' + mention.full_text + ' - ' + str(mention.in_reply_to_status_id), flush=True)

        last_seen_id = mention.id

        store_last_seen_id(last_seen_id, FILE_NAME)


        
        if '#gms' or '#givemethesong' in mention.full_text.lower():


            print('found a tweet !', flush=True)


            if mention.in_reply_to_status_id != None : # Verify if the tweet with mention reply to an other tweet
                id_initial_tweet = str(mention.in_reply_to_status_id)
                print(id_initial_tweet)

                lyrics = retrieve_initial_tweet(id_initial_tweet)

                print('Search the name of the song ...', flush=True)
                song_name = search_song(lyrics)

                if song_name != None : # If Genius find a answer

                    print('responding back...', flush=True)

                    api.update_status(('@' + mention.user.screen_name + ' ' + song_name +
                                       ' ! Profites bien du son chakal ! #PythonVie 🖖🖖🏻🖖🏼🖖🏽🖖🏾🖖🏿'), mention.id) #response (french with joke)

                    print('reply sent !', flush = True)


                else : # If Genius don't find a answer


                    print('No answer !', flush = True)

                    api.update_status(('@' + mention.user.screen_name +
                               ''' Bah alors mon soce, tu m'as trouvé ça où ? Je connaîs pas ce charabia moi. '''), mention.id) #response (french with joke)

                    print('reply sent !', flush = True)


            else :

                print("Initial tweet don't exist ", flush=True)

                api.update_status(('@' + mention.user.screen_name +
                               ''' Si tu me mentionnes pas en dessous d'un tweet, je peux pas t'aider mon p'tit pote '''), mention.id) #response (french with joke)

                print('reply sent !', flush = True)
    sleep(15)
    reply_to_tweets()



reply_to_tweets() #First call

### Isn't the entire version of my bot : @TheLyricsRobot (on Twitter) but the other functions was more simple than this principal function (below) and use the script below.
### For the settings of Tweepy, i was helped by the YouTube video of CSdojo : "Create a Twitter bot with Python".
### Thanks to the peoples who helped me on Github page of Lyrics Genius when i was problems with this package.
### If you have some questions or problems about this bot, contact me on my Github or on my personnal Twitter account (@MatthLaPatate).
### 🖖🖖🏻🖖🏼🖖🏽🖖🏾🖖🏿
