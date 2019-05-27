# [START gae_python37_app]

import io
import pyodbc
from datetime import datetime
from flask import Flask, render_template, request, Response, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
#matplotlib.use('agg')


app = Flask(__name__)
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                    'Server=tcp:arduino-dev.database.windows.net;'
	            'Database=ARDUINO-SENSORS-DEV;'
	            'UID=arduino-dev-admin@arduino-dev;'
	            'PWD=9120Cool;')
curs = conn.cursor()


# Retrieve last data from database
def getLastData():
    for row in curs.execute('SELECT TOP 1 ScriptDato, ScriptTid, Ovn, Avfukter, Temp_inne, Temp_ute, Luftfuktighet_inne, Luftfuktighet_ute, Gassverdi_inne, Temp_Ute2, Lys_ute FROM Facts.All_Info WHERE ScriptDato > DATEADD(DAY, -7, GETDATE()) AND Temp_inne IS NOT NULL ORDER BY ScriptDato DESC, ScriptTid DESC;'):
        date = str(row[0])
        time = str(row[1])
        heater = row[2]
        dehumid = row[3]
        temp_inside = row[4]
        temp_outside = (row[5]+row[9])/2
        hum_inside = row[6]
        hum_outside = row[7]
        air_inside = row[8]
        light_outside = row[9]
    #conn.close()
    return date, time, heater, dehumid, temp_inside, temp_outside, hum_inside, hum_outside, air_inside, light_outside

# Get 'x' samples of historical data
def getHistData (numSamples):
    curs.execute('SELECT TOP '+str(numSamples)+' ScriptDato, ScriptTid, Temp_inne, Temp_ute, Luftfuktighet_inne FROM Facts.All_Info WHERE ScriptDato > DATEADD(DAY, -7, GETDATE()) AND Temp_inne IS NOT NULL ORDER BY ScriptDato DESC, ScriptTid DESC;')
    data = curs.fetchall()
    datetimes = []
    temps_inside = []
    temps_outside = []
    hums_inside = []
    for row in reversed(data):
        datetimes.append(datetime(row[0].year,row[0].month,row[0].day,row[1].hour,row[1].minute,row[1].second))
        #datetimes.append(datetime.time(row[1].hour,row[1].minute,row[1].second))
        #datetimes.append(row[1])
        temps_inside.append(row[2])
        temps_outside.append(row[3])
        hums_inside.append(row[4])
    return datetimes, cleanData(temps_inside), cleanData(temps_outside), cleanData(hums_inside)

# Test data and clean out possible "out of range" values
def cleanData(values):
    n = len(values)
    for i in range(0, n-1):
        if (values[i] < -1000 or values[i] > 1000):
            values[i] = 0
    return values

# Get Max number of rows (table size)
def maxRowsTable():
    for row in curs.execute("Select COUNT(*) FROM Facts.All_Info"):
        maxNumberRows=row[0]
    return maxNumberRows

# Get sample frequency in minutes
def freqSample():
    datetimes, temps1, temps2, hums = getHistData(2)
    #fmt = '%Y-%m-%d %H:%M:%S'
    freq = datetimes[1]-datetimes[0]
    freq = int(round(freq.total_seconds()/60))
    return (freq)

# define and initialize global variables
global freqSamples
freqSamples = freqSample()

global rangeTime
rangeTime = 12

global numSamples
numSamples = rangeTime*60 // freqSamples

# main route
@app.route("/")
def index():
    date, time, heater, dehumid, temp_inside, temp_outside, hum_inside, hum_outside, air_inside, light_outside = getLastData()
    templateData = {
        'date': date,
        'time': time,
        'heater': heater,
        'dehumid': dehumid,
        'temp_inside': temp_inside,
        'temp_outside': temp_outside,
        'hum_inside': hum_inside,
        'hum_outside': hum_outside,
        'air_inside': air_inside,
        'light_outside': light_outside,
        'freq': freqSamples,
        'rangeTime': rangeTime
    }
    return render_template('index.html', **templateData)

@app.route('/', methods=['POST'])
def my_form_post():
    global numSamples
    global freqSamples
    global rangeTime
    rangeTime = int (request.form['rangeTime'])
    if (rangeTime*60 < freqSamples):
        rangeTime = freqSamples + 1
    numSamples = rangeTime*60 // freqSamples #Entering rangeTime in hours on webpage
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)

    date, time, heater, dehumid, temp_inside, temp_outside, hum_inside, hum_outside, air_inside, light_outside = getLastData()
    templateData = {
        'date': date,
        'time': time,
        'heater': heater,
        'dehumid': dehumid,
        'temp_inside': temp_inside,
        'temp_outside': temp_outside,
        'hum_inside': hum_inside,
        'hum_outside': hum_outside,
        'air_inside': air_inside,
        'light_outside': light_outside,
        'freq': freqSamples,
        'rangeTime': rangeTime
    }
    return render_template('index.html', **templateData)


@app.route('/plot/temp')
def plot_temp():
    datetimes, temps_inside, temps_outside, hums_inside = getHistData(numSamples)
    ys1 = temps_inside
    ys2 = temps_outside
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Temperature inside and outside [°C]")
    axis.set_xlabel("Date & time")
    axis.grid(True)
    xs = datetimes
    axis.plot(xs, ys1)
    axis.plot(xs, ys2)
    fig.autofmt_xdate() # rotate and align the tick labels so they look better
    timeFormat = mdates.DateFormatter('%H:%M:%S')
    axis.xaxis.set_major_formatter(timeFormat)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/plot/hum')
def plot_hum():
    datetimes, temps_inside, temps_outside, hums_inside = getHistData(numSamples)
    ys1 = hums_inside
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Humidity inside [%]")
    axis.set_xlabel("Date & time")
    axis.grid(True)
    xs = datetimes
    axis.plot(xs, ys1)
    fig.autofmt_xdate() # rotate and align the tick labels so they look better
    timeFormat = mdates.DateFormatter('%H:%M')
    axis.xaxis.set_major_formatter(timeFormat)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

#if __name__ == '__main__':
#    app.run(host='127.0.0.1', port=8080, debug=True)


# [END gae_python37_app]
