from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_table import Table, Col
import requests
import json
import datetime

app = Flask(__name__)

values = [200, 400, 600, 800, 1000, 1200, 1600, 2000]


class CluesTable(Table):
    clue_id = Col("Clue ID")
    category_id = Col("Category ID")
    category = Col("Category")
    question = Col("Question")
    answer = Col("Correct Answer")
    difficulty = Col("Difficulty/Value")
    airdate = Col("Air Date")


class Clues(object):
    def __init__(self, clue_id, category, category_id, question, difficulty, answer, airdate):
        self.clue_id = clue_id
        self.category = category
        self.category_id = category_id
        self.question = question
        self.answer = answer
        self.difficulty = difficulty
        self.airdate = airdate


@app.route('/', methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home_page.html", values = values)

    elif request.method == "POST":

        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        category_id = request.form.get('category_id')
        difficulty = request.form.get('difficulty')
        
        request_param = {}

        if start_date != "" and start_date != None:
            request_param["min_date"] = start_date
        if end_date != "" and end_date != None:
            request_param["max_date"] = end_date
        if category_id != "" and category_id != None:
            request_param["category"] = str(category_id)
        if difficulty != "" and difficulty != None:
            request_param["value"] = difficulty

        if "min_date" in request_param and "max_date" not in request_param:
            request_param["max_date"] = str(datetime.datetime.now())

        if len(request_param) == 0:
            res = requests.get('http://jservice.io/api/random?count=100')
        
        else:
            query = ""
            for param, param_value in request_param.items():
                query += str(param) + "=" + str(param_value) + "&"
            
            query = query[:-1]
            text = ""
            for entry in request_param:
                text += str(request_param[entry])


            res = requests.get('http://jservice.io/api/clues?' + query)
        
        json_data = json.loads(res.text)

        all_clues = []
        for clue in json_data:
            clue_id = clue["id"]
            answer = clue["answer"]

            if "<i>" in answer:
                answer = answer[3:-4]
            
            question = clue["question"]

            if "<i>" in question:
                question = question[3:-4]

            difficulty = clue["value"]
            airdate = clue["airdate"][:10]
 
            category = clue["category"]["title"]
            category_id = clue["category"]["id"]

            new_clue = Clues(clue_id, category, category_id, question, difficulty, answer, airdate)
            all_clues.append(new_clue)


        table = CluesTable(all_clues)
        table.border = True
    
    
        return render_template("home_page.html", values = values, table = table)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug = True, host = '0.0.0.0', port = port)