import pandas as pd

import ConfigParser

path = 'DailySPYrun.cfg'
config = ConfigParser.ConfigParser()
config.read(path)

SPYoptFile = config.get('Settings', 'SPYoptFile')

Dailyframe = pd.read_csv(SPYoptFile)

Dailyframe.insert(0,'ExpirationDate','216-10-5')


Dailyframe.to_csv('TESToptFile.csv', sep=',', encoding='utf=8')
