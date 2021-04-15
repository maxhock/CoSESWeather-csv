# $Id: install.py 1766 2017-10-17 13:53:41Z mwall $
# installer for csvwriter
# Copyright 2015 Matthew Wall

from setup import ExtensionInstaller

def loader():
    return CSVInstaller()

class CSVInstaller(ExtensionInstaller):
    def __init__(self):
        super(CSVInstaller, self).__init__(
            version="0.10",
            name='csv',
            description='Emit loop or archive data in CSV format.',
            author="Matthew Wall",
            author_email="mwall@users.sourceforge.net",
            process_services='user.csv.CSV',
            config={
                'CSV': {
                    'timestamp_format':'%Y-%m-dT%H:%M:%S%z',
                    'loop' : {
                        'filename' : '/mnt/nas/data_loop.csv',
                        'keys' : 'dateTime, usUnits, interval, outTemp, windSpeed, windGust, windchill, radiation, radiationDiff, sun, radiation1, radiation2, radiation3',
                        'datestamp_format' : '%Y-%m-%d',
                    },
                    'archive': {
                        'filename' : '/mnt/nas/data_archive.csv',
                        'keys' : 'id, temp, wind, spn1_radTot, spn1_radDiff, spn1_sun, rad_cmp1, rad_cmp2, rad_cmp3, t_unix',
                        'datestamp_format' : '%Y-%m',
              	    }
                }
            },
            files=[('bin/user', ['bin/user/csv.py'])]
            )
