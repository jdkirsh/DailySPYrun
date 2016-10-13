import os
import pandas as pd
import csv
import sqlite3
import ConfigParser

path = 'DailySPYrun.cfg'
config = ConfigParser.ConfigParser()
config.read(path)

SPYoptFile = config.get('Settings', 'SPYoptFile')
DATABASE = config.get('Settings', 'OIdatabase')


def DailyOIload():
    Dailyframe = pd.read_csv(SPYoptFile)
    try:
        conn = sqlite3.connect(DATABASE)
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


# ######################## Main ########################
if __name__ == '__main__':
    DailyOIload()
