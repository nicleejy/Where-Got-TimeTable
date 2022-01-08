from datetime import time
from flask import Flask, request, render_template
import requests
from main import main
from webscraping import get_download_link, save_image


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        modules = request.form.get("modules")
        module_list = [i.upper() for i in modules.split()]
        starttime = int(float(request.form.get("timestart")))
        endtime = int(float(request.form.get("timeend")))

        semester = int(request.form.get("semester"))

        monday = "Monday" if request.form.get("Monday") == "on" else "off"
        tuesday = "Tuesday" if request.form.get("Tuesday") == "on" else "off"
        wednesday = "Wednesday" if request.form.get("Wednesday") == "on" else "off"
        thursday = "Thursday" if request.form.get("Thursday") == "on" else "off"
        friday = "Friday" if request.form.get("Friday") == "on" else "off"

        freeday_list = list(filter(lambda x: x != "off", [monday, tuesday, wednesday, thursday, friday]))
        print(f'asdf{freeday_list}')

        interval_input = request.form.get("betweenlessons")
        interval = False if interval_input == "" else int(interval_input)

        lunch = True if request.form.get("lunch") == "on" else False

        link = main(module_list, semester, starttime, endtime, freeday_list, lunch, interval)

        if link == False:
            return render_template('error.html')

        dl_link = get_download_link(link)
        
        save_image(dl_link, 'static/My Timetable.png')
        
        return render_template('results.html', link=link)
    else:
        return render_template('index.html')