# $Id: install.py 1766 2017-10-17 13:53:41Z mhock $
# installer for csvwriter
# Copyright 2021 Maximilian Hock
# Original code by Matthew Wall

from setup import ExtensionInstaller

def loader():
    return CSVInstaller()

class CSVInstaller(ExtensionInstaller):
    def __init__(self):
        super(CSVInstaller, self).__init__(
            version="1.2.3",
            name='csv',
            description='Emit loop and archive data in CSV format.',
            author="Maximilian Hock",
            author_email="max.hock@tum.de",
            process_services='user.csv.CSV',
            config={
                'CSV': {
                    'timestamp_format':'%Y-%m-%dT%H:%M:%S%z',
                    'loop' : {
                        'filename' : '/mnt/nas/data_loop.csv',
                        'keys' : 'dateTime,usUnits,interval,outTemp,windSpeed,windGust,windchill,radiation,radiationDiff,sun,radiation1,radiation2,radiation3',
                        'datestamp_format' : '%Y-%m-%d',
                    },
                    'archive': {
                        'filename' : '/mnt/nas/data_archive.csv',
                        'keys' : 'dateTime,usUnits,interval,outTemp,windSpeed,windGust,windchill,radiation,radiationDiff,sun,radiation1,radiation2,radiation3',
                        'datestamp_format' : '%Y-%m',
              	    }
                }
            },
            files=[('bin/user', ['bin/user/csv.py'])]
            )
