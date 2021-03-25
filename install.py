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
                    'filename_loop' : '/mnt/nas/data_loop.csv',
                    'keys_loop' : 'dateTime, usUnits, interval, outTemp, windSpeed, windGust, windchill, radiation, radiationDiff, sun, radiation1, radiation2, radiation3',
                    'filename_archive' : '/mnt/nas/data_archive.csv',
                    'keys_archive' : 'id, temp, wind, spn1_radTot, spn1_radDiff, spn1_sun, rad_cmp1, rad_cmp2, rad_cmp3, t_unix',
                    'timestamp_format':'%Y-%m-dT%H:%M:%S%z'}},
            files=[('bin/user', ['bin/user/csv.py'])]
            )
