import DailyOIstd
import DailyOICollect
import tableDFloader

import ConfigParser

path = 'DailySPYrun.cfg'
config = ConfigParser.ConfigParser()
config.read(path)

DailyOICollect.dailyOICollector()
DailyOIstd.archive( config.get('Settings','SPYoptFile') )
tableDFloader.DailyOIload()


