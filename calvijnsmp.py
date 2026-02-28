from flask import Flask, render_template
from mcstatus import JavaServer
import socket

calvijnsmpsite = Flask(__name__)

serveradress = "private"
serverport = private
def check_server():
    try:
        server = JavaServer.lookup(f"{serveradress}:{serverport}")
        serverstatus = server.status()

        playernames = []
        if serverstatus.players.sample:
            playernames = [p.name for p in serverstatus.players.sample]

        return {
            "online": True,
            "players_online": serverstatus.players.online,
            "players_max": serverstatus.players.max,
            "player_names": playernames,
        }

    except Exception as e:
        print("Error:", e)
        return {"online": False}

@calvijnsmpsite.route("/")
def home():
    status = check_server()
    return render_template("calvijnsmp.html", status=status)

if __name__ == "__main__":
    calvijnsmpsite.run(host="0.0.0.0", port=5000, debug=False)
