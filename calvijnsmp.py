from flask import Flask, render_template
from mcstatus import JavaServer
import socket

calvijnsmpsite = Flask(__name__)

serveradress = "goes.calvijnsmp.nl"
serverport = 48890
def check_server():
    try:
        server = JavaServer.lookup(f"{serveradress}:{serverport}")
        serverstatus = server.status(timeout=3)

        servermotd = ""
        if isinstance(serverstatus.description, dict):
            servermotd = serverstatus.description.get("text", "")
        else:
            servermotd = str(serverstatus.description)

        servermotdlower = servermotd.lower()

        offlineserver = (
            "offline" in servermotdlower
            or "connect to" in servermotdlower
            or "aternos.org" in servermotdlower
            or serverstatus.players.max == 0
            or serverstatus.version.protocol <= 0
        )

        if offlineserver:
            return {"online": False}

        playernames = []
        if serverstatus.players.sample:
            playernames = [p.name for p in serverstatus.players.sample]

        return {
            "online": True,
            "players_online": serverstatus.players.online,
            "players_max": serverstatus.players.max,
            "player_names": playernames,
        }
    
    except:
        return {"online": False}

@calvijnsmpsite.route("/")
def home():
    status = check_server()
    return render_template("calvijnsmp.html", status=status)

if __name__ == "__main__":
    calvijnsmpsite.run(host="0.0.0.0", port=5000, debug=False)