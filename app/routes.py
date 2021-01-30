from app import app
from bs4 import BeautifulSoup
from moviepy.editor import * 
import requests 
from flask import request, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse


@app.route("/random_joke", methods=['POST'])
def laughy():
    incoming_msg = request.values.get("Body", "").lower()
    response = MessagingResponse()
    message = response.message()
    URL = "https://lesjoiesducode.fr/random"

    if "combi" in incoming_msg :

        res = requests.get(URL)
        response = ""
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
                message.body(f"{title}")
                message.media("https://0dd6df9e3a5c.ngrok.io/app/video.gif")
            else :
               message.body("une erreur s'est produite :(") 
            
        else :
            message.body("une erreur s'est produite :(")

    elif "help" in incoming_msg :
        message.body("Pour avoir une blague amusante demande à combi en tapant la commande *combi*. Les blagues en résultat seront du domaine du dev logiciel. Have Fun ! 😂 @d41k1")
    else :
        message.body("Commande non reconnnue. Tape *help* pour en savoir plus")
    
    

    s
    return "ok"
