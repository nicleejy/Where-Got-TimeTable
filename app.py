from datetime import time
from flask import Flask, request, render_template
from main import main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        modules = request.form.get("modules")
        module_list = modules.split()
        starttime = int(float(request.form.get("timestart")))
        endtime = int(float(request.form.get("timeend")))

        monday = "Monday" if request.form.get("Monday") == "on" else "off"
        tuesday = "Tuesday" if request.form.get("Tuesday") == "on" else "off"
        wednesday = "Wednesday" if request.form.get("Wednesday") == "on" else "off"
        thursday = "Thursday" if request.form.get("Thursday") == "on" else "off"
        friday = "Friday" if request.form.get("Friday") == "on" else "off"

        freeday_list = filter(lambda x: x != "off", [monday, tuesday, wednesday, thursday, friday])

        interval = int(request.form.get("betweenlessons"))

        lunch = True if request.form.get("lunch") == "on" else False

        link = main(module_list, 2, starttime, endtime, freeday_list, lunch, interval)
        
        return render_template('results.html', link=link)
    else:
        return render_template('index.html')