import flask
from flask import request, jsonify
import numpy as np
import battle as bat
import newciv_bot as nc
import sys
import time

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1>" \
           "<p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/api', methods=['GET'])
def api_id():
    try:
        if 'id1' in request.args:
            team1 = min(int(request.args['id1']), 5000)
        else:
            return "Team 1 invalid."

        if 'id2' in request.args:
            team2 = min(int(request.args['id2']), 5000)
        else:
            return "Team 2 invalid."

        team1 = 0 if team1 == team2 else team1
    except:
        return "Problem with team ids."

    try:
        new_b = bat.BattleBB(team1, team2)
        test, winner = new_b.battle_bb()
        new = nc.NewcivLogin()
        new_p = new.make_newpost(test, 1054931)
        print(f"Success! Winner: {winner}")
        return "Success."
    except:
        print(f"Failure! Team1: {team1} Team2: {team2}")
        return "Failure."


@app.route('/api2', methods=['GET'])
def api_id2():
    try:
        if 'id1' in request.args:
            team1 = min(int(request.args['id1']), 5000)
        else:
            return "Team 1 invalid."

        team = bat.Team(team1)
        lvl = team.analyze()

    except:
        return "Problem with team id."

    if int(request.args['thread']) > 0:
        thread_id = int(request.args['thread'])
    else:
        thread_id = 1054931

    try:
        new_b = bat.BattleBB(team1, f"Random*{lvl}")
        test, winner = new_b.battle_bb()
        new = nc.NewcivLogin()
        new_p = new.make_newpost(test, thread_id)
        print(f"Success! Winner: {winner}")
        return "Success."
    except:
        print(f"Failure! Team1: {team1} Team2: Random*{lvl}")
        return "Failure."


@app.route('/api3', methods=['GET'])
def api_id3():
    try:
        if 'id1' in request.args:
            team1 = min(int(request.args['id1']), 5000)
        else:
            return "Team 1 invalid."

        team = bat.Team(team1)
        lvl = team.analyze()

    except:
        return "Problem with team id."

    if int(request.args['thread']) > 0:
        thread_id = int(request.args['thread'])
    else:
        return "Problem with thread."

    try:
        new_b = bat.BattleBB(team1, f"Random*{lvl}")
        test, winner = new_b.battle_bb()
        new = nc.NewcivLogin()
        new_p = new.make_newpost(test, thread_id)
        print(f"Success! Winner: {winner}")

        total = 0
        for pokemon in team.members:
            total += pokemon.level

        exp_array = []
        for pokemon in team.members:
            exp = 5 + pokemon.level / total * lvl
            if winner.user_id != '15':
                exp_array.append(round(exp))
            else:
                exp_array.append(round(exp/2))

        new = nc.NewcivLogin()
        exp_str = ','.join(map(str, exp_array))
        print(f"Team:{team.team_id} and exp:{exp_str}")
        new_r = new.reward_team(team.team_id, exp_str)
        return "Success."
    except:
        print(f"Failure! Team1: {team1} Team2: Random*{lvl}")
        return "Failure."


@app.route('/api4', methods=['GET'])
def api_id4():
    timestamp = int(time.time())
    with open(f"log/{timestamp}.txt", 'w') as f:
        sys.stdout = f
        print("hello", flush=True)

        try:
            if 'id1' in request.args:
                team1 = min(int(request.args['id1']), 5000)
            else:
                return "Team 1 invalid."

            team = bat.Team(team1)
            lvl = team.analyze()

        except:
            return "Problem with team id."

        if int(request.args['thread']) > 0:
            thread_id = int(request.args['thread'])
        else:
            return "Problem with thread."

        if 'type' in request.args:
            type = min(int(request.args['type']), 99)
        else:
            return "Invalid Gen or Gym."

        gen = np.floor(type / 10)
        badge = type % 10
        print(f"Gym*{lvl}*{gen}*{badge}", flush=True)

        try:
            new_b = bat.BattleBB(team1, f"Gym*{lvl}*{gen}*{badge}")
            test, winner = new_b.battle_bb()
            new = nc.NewcivLogin()
            new_p = new.make_newpost(test, thread_id)
            print(f"Success! Winner: {winner}", flush=True)

            total = 0
            for pokemon in team.members:
                total += pokemon.level

            exp_array = []
            for pokemon in team.members:
                exp = 5 + pokemon.level / total * lvl
                if winner.user_id != '15':
                    exp_array.append(round(exp))
                else:
                    exp_array.append(round(exp/2))

            new = nc.NewcivLogin()
            exp_str = ','.join(map(str, exp_array))
            print(f"Team:{team.team_id} and exp:{exp_str}", flush=True)
            new_r = new.reward_team(team.team_id, exp_str)
            if winner.user_id == team.user_id:
                new_gym = new.reward_gym(team.user_id, gen, badge, thread_id)
                print(f"Team:{team.team_id} and result:{new_gym}", flush=True)
                if new_gym != 'Good':
                    new_gym = new.reward_gym(team.user_id, gen, badge, thread_id)
            return "Success."
        except:
            print(f"Failure! Team1: {team1} Team2: Gym*{lvl}*{gen}*{badge}", flush=True)
            return "Failure."


if __name__ == '__main__':
    app.run(debug=True, host="0", port="9999")
