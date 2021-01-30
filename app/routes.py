from app import app
from bs4 import BeautifulSoup
from moviepy.editor import * 
import requests 
from flask import request, jsonify
# from twilio.twiml.messaging_response import MessagingResponse

# endpoint to get a joke /random_joke
@app.route("/random_joke/<command>", methods=["GET"])
def laughy(command):
    # incoming_msg = request.values.get("Body", "").lower()
    incoming_msg = command 
    URL = "https://lesjoiesducode.fr/random"
    response = {}

    # trigger on the command "combi"
    if "combi" in incoming_msg :

        res = requests.get(URL)
        if res.ok :
            soup = BeautifulSoup(res.content, "html.parser")
            title = soup.select_one('h1[class="blog-post-title single-blog-post-title"]').text
            video_url = soup.select_one('source[type="video/webm"]').get("src")
            r = requests.get(video_url, stream = True )

            if r.ok : 
                with open("app/video.webm", "wb") as video_file:
                    for chunk in r.iter_content(chunk_size = 1024*1024):
                        if chunk:
                            video_file.write(chunk)
                
                clip = VideoFileClip("app/video.webm").write_gif("app/video.gif")
                response["title"] = title
                response["video"] = video_url
                response["error"] = ""
            else :
               response["error"] = "une erreur s'est produite :("
            
        else :
            response["error"] = "une erreur s'est produite :("

    elif "help" in incoming_msg :
        response["error"] = "Pour avoir une blague amusante demande à combi en tapant la commande *combi*. Les blagues en résultat seront du domaine du dev logiciel. Have Fun ! 😂 @d41k1"
    else :
        response["error"] = "Commande non reconnnue. Envoyer *help* pour en savoir plus"
    
    return jsonify(response)
