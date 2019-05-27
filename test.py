import pyodbc

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=tcp:arduino-dev.database.windows.net;'
                      'Database=ARDUINO-SENSORS-DEV;'
                      'UID=arduino-dev-admin@arduino-dev;'
                      'PWD=9120Cool;')

cursor = conn.cursor()
cursor.execute( 'SELECT ScriptDato, ScriptTid, Temp_inne, Temp_ute, Luftfuktighet_inne FROM Facts.All_Info WHERE ScriptDato > DATEADD(DAY, -2, GETDATE()) AND Temp_inne IS NOT NULL ORDER BY ScriptDato DESC, ScriptTid DESC;')

for row in cursor:
    print(row)
