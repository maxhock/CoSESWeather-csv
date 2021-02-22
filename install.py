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
                    'filename_loop': '/var/tmp/data_loop.csv',
                    'filename_archive': '/var/tmp/data_archive.csv'}},
            files=[('bin/user', ['bin/user/csv.py'])]
            )
