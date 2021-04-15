# $Id: csv.py 1766 2017-10-17 13:53:41Z mwall $
# Copyright 2015 Matthew Wall

import os
import os.path
import time
import syslog

import weewx
import weewx.engine
import weeutil.weeutil
import schemas.wview
import weedb.mysql

VERSION = "0.10"

def logmsg(level, msg):
    syslog.syslog(level, 'csv: %s' % msg)

def logdbg(msg):
    logmsg(syslog.LOG_DEBUG, msg)

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)

class CSV(weewx.engine.StdService):
    def __init__(self, engine, config_dict):
        super(CSV, self).__init__(engine, config_dict)
        loginf("service version is %s" % VERSION)
        d = config_dict.get('CSV', {})
        # optionally emit a header line as the first line of the file
        self.emit_header = weeutil.weeutil.to_bool(d.get('header', True))
        # mode can be append or overwrite
        self.mode = d.get('mode', 'append')
        # optionally append a datestamp to the filename
        self.append_datestamp = weeutil.weeutil.to_bool(d.get('append_datestamp', True))
        # format for the per-record timestamp
        self.timestamp_format = d.get('timestamp_format')

        # loop
        # location of the output file
        self.filename_loop = d.get('loop','filename', '/var/tmp/data_loop.csv')
        # format for the loop filename datestamp
        self.datestamp_format_loop = d.get('loop','datestamp_format', '%Y-%m-%d')
        # list of loop columns to write
        self.keys_loop = d.get('loop','keys')
        # bind to loop events
        self.bind(weewx.NEW_LOOP_PACKET, self.handle_new_loop)
        
        # archive
        # location of the output file
        self.filename_archive = d.get('archive','filename', '/var/tmp/data_archive.csv')
        # format for the archive filename datestamp
        self.datestamp_format_archive = d.get('archive','datestamp_format', '%Y-%m')
        # list of archive columns to write
        self.keys_archive = d.get('archive','keys')
        # bind to archive events
        self.bind(weewx.NEW_ARCHIVE_RECORD, self.handle_new_archive)

    def handle_new_loop(self, event):
        self.write_data(event.packet, "loop")

    def handle_new_archive(self, event):
        self.write_data(event.record, "archive")

    def write_data(self, data, binding):
        flag = "a" if self.mode == 'append' else "w"
        if binding == "loop":
            filename = self.filename_loop
            keys = self.keys_loop
            datestamp_format = self.datestamp_format_loop
        else:
            filename = self.filename_archive
            keys = self.keys_archive
            datestamp_format = self.datestamp_format_archive
        if self.append_datestamp:
            basename = filename
            ext = ''
            idx = filename.find('.')
            if idx > -1:
                basename = filename[:idx]
                ext = filename[idx:]
            tstr = time.strftime(datestamp_format,
                                 time.gmtime(data['dateTime']))
            filename = "%s-%s%s" % (basename, tstr, ext)
        header = None
        # expand data dict to always write all possible entries, defined config
        for key in keys:
            data.setdefault(key)
        # add local time in ISO 8601 format
        data['localtime'] = time.strftime("%Y-%m-dT%H:%M:%S%z",time.localtime(data['dateTime']))
        # adds name of stored variables in header
        if self.emit_header and (
            not os.path.exists(filename) or flag == "w"):
            header = '# %s\n' % ','.join(self.sort_keys(data))
        with open(filename, flag) as f:
            if header:
                f.write(header)
            f.write('%s\n' % ','.join(self.sort_data(data)))

    def sort_keys(self, record):
        fields = ['dateTime']
        for k in sorted(record):
            if k != 'dateTime':
                fields.append(k)
        return fields

    def sort_data(self, record):
        tstr = str(record['dateTime'])
        if self.timestamp_format is not None:
            tstr = time.strftime(self.timestamp_format,
                                 time.gmtime(record['dateTime']))
        fields = [tstr]
        for k in sorted(record):
            if k != 'dateTime':
                fields.append(str(record[k]))
        return fields
