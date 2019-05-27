# [START gae_python37_app]

from flask import Flask, render_template, request
app = Flask(__name__)
import pyodbc

# Retrieve data from database
def getData():
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=tcp:arduino-dev.database.windows.net;'
	                  'Database=ARDUINO-SENSORS-DEV;'
	                  'UID=arduino-dev-admin@arduino-dev;'
	                  'PWD=9120Cool;')
    curs=conn.cursor()
    for row in curs.execute('SELECT TOP 1 ScriptDato, ScriptTid, Temp_inne, Temp_ute, Luftfuktighet_inne FROM Facts.All_Info WHERE ScriptDato > DATEADD(DAY, -2, GETDATE()) AND Temp_inne IS NOT NULL ORDER BY ScriptDato DESC, ScriptTid DESC;'):
    	date = str(row[0])
    	time = str(row[1])
    	temp_inside = row[2]
    	temp_outside = row[3]
    	hum_inside = row[4]
    conn.close()
    return date, time, temp_inside, temp_outside, hum_inside

# main route
@app.route("/")
def index():
    date, time, temp_inside, temp_outside, hum_inside = getData()
    templateData = {
        'date': date,
        'time': time,
        'temp_inside': temp_inside,
        'temp_outside': temp_outside,
        'hum_inside': hum_inside
    }
    return render_template('index.html', **templateData)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)


# [END gae_python37_app]
