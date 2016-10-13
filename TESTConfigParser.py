import os
import pandas as pd
import sqlite3
import ConfigParser

path = 'DailySPYrun.cfg'

config = ConfigParser.ConfigParser()
config.read(path)

url = config.get('Settings', 'url_prefix')
oidatabase = config.get('Settings','oidatabase')

#oidatabase = oidatabase.replace('\\\\','\\' )

#config.set('Settings','oidatabase','r"C:\FINANCE\Python\PyCharm\Projects\DailySPYrun\SPYdb.db3"')
SPYoptFile = config.get('Settings', 'SPYoptFile')
JK = "C:\FINANCE\Python\PyCharm\Projects\DailySPYrun\SPYdb.db3"

print ("JK=",JK)
print ("oidatabase=",oidatabase)
print ("oidatabase : " ,os.path.isfile(oidatabase) )
print ("JK :", os.path.isfile(JK))



Dailyframe = pd.read_csv(SPYoptFile)
try:
    conn = sqlite3.connect(oidatabase)
    conn.text_factory = str
    cur = conn.cursor()

    oi_frame = Dailyframe[[0,1,4,5,6,7,10,11]]

    oi_frame.columns = ['Index', 'CallsLastPrice', 'CallsVolume', 'CallsOI', 'Strike', 'PutsLastPrice', 'PutsVolume', 'PutsOI']
    oi_frame.index.name='Index'
    oi_frame.to_sql('OpenInterest', conn, if_exists='append', index=False)
    conn.commit()
except sqlite3.Error as er:
    # Something is wrong with the database
    print 'er', er.message
#
# with open(path, "wb") as config_file:
#     config.write(config_file)
#
# with open (path, 'r') as f:
#     for line in f:
#         print line
