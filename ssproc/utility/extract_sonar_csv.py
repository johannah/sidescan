import pandas as pd
import os, sys
from glob import glob
import numpy as np
import utm
import struct
import pandas as pd
"""
Author: JRH with base parsing information taken from previous work by Anqi Xu
This file parses the binary logdoc file produced by the starfish 453
sidescan sonar into space separated by spaces. There exists long data entries
information for the port/stbd data from the sonar.  These are stored under their
respective port/stbd names and seperated by a comma.
"""

# values for parsing binary logdoc for various headers
pos_opcode = 0x21
hdg_opcode = 0x20
dpt_opcode = 0x24
vel_opcode = 0x22
xxx_opcode = 0x29
sss_opcode = 0x26
pos_bytes = 43
hdg_bytes = 25
dpt_bytes = 25
vel_bytes = 25
xxx_bytes = 25
sss_bytes = 1057
# format of binary logdocs - only tested on 0x01
fmt_version = 0x01


def parse_pos(s):
    assert(len(s) >= pos_bytes)
    assert(ord(s[0]) == fmt_version)
    assert(ord(s[1]) == pos_opcode)
    idx = 2
    (year, month, day, hour, minute, millisec, post_utc_unknown_word, delim) = struct.unpack('<HBBBBHIH', s[idx:(idx+14)])
    assert(delim == 0)
    idx += 14
    # time zone
    #TODO maybe fix to UTM?
    zone_char = s[idx]
    zone_num = ord(s[idx+1])
    zone_str = '%d%s' % (zone_num, zone_char)

    (northing, easting, utm_sixth_field) = struct.unpack('<ddd', s[(idx+2):(idx+26)])
    checksum = s[idx+26]

    latlon = utm.to_latlon(easting, northing, zone_num, zone_char)
    latitude = latlon[0]
    longitude = latlon[1]

    date_str = '%02d/%02d/%04d' %(day, month, year)
    time_str = '%02d:%02d:%02.3f' %(hour, minute, millisec/1000.0)
    #utm_str = '%s,%.16f,%.16f,%.16f' % (zone_str, northing, easting, utm_sixth_field)
    return date_str, time_str, '%.16f'%latitude, '%.16f'%longitude

def parse_hdg(s):
    fmt_version = 0x01
    assert(len(s) >= hdg_bytes)

    assert(ord(s[0]) == fmt_version)
    assert(ord(s[1]) == hdg_opcode)
    idx = 2

    (year, month, day, hour, minute, millisec, post_utc_unknown_word, delim) = struct.unpack('<HBBBBHIH', s[idx:(idx+14)])
    assert(delim == 0)
    idx += 14

    hdg = struct.unpack('<d', s[(idx):(idx+8)])[0]
    checksum = s[idx+8]

    date_str = '%02d/%02d/%04d' %(day, month, year)
    time_str = '%02d:%02d:%02.3f' %(hour, minute, millisec/1000.0)
    return round(hdg, 2)


def parse_dpt(s):
    assert(len(s) >= dpt_bytes)

    assert(ord(s[0]) == fmt_version)
    assert(ord(s[1]) == dpt_opcode)
    idx = 2

    (year, month, day, hour, minute, millisec, post_utc_unknown_word, delim) = struct.unpack('<HBBBBHIH', s[idx:(idx+14)])
    assert(delim == 0)
    idx += 14

    depth = struct.unpack('<d', s[(idx):(idx+8)])[0]
    checksum = s[idx+8]

    date_str = '%02d/%02d/%04d' %(day, month, year)
    time_str = '%02d:%02d:%02.3f' %(hour, minute, millisec/1000.0)
    return round(depth, 2)


def parse_vel(s):
    assert(len(s) >= vel_bytes)

    assert(ord(s[0]) == fmt_version)
    assert(ord(s[1]) == vel_opcode)
    idx = 2

    (year, month, day, hour, minute, millisec, post_utc_unknown_word, delim) = struct.unpack('<HBBBBHIH', s[idx:(idx+14)])
    assert(delim == 0)
    idx += 14

    vel = struct.unpack('<d', s[(idx):(idx+8)])[0]
    checksum = s[idx+8]

    date_str = '%02d/%02d/%04d' %(day, month, year)
    time_str = '%02d:%02d:%02.3f' %(hour, minute, millisec/1000.0)
    return round(vel, 2)


def parse_xxx(s):
    assert(len(s) >= vel_bytes)

    assert(ord(s[0]) == fmt_version)
    assert(ord(s[1]) == vel_opcode)
    idx = 2

    (year, month, day, hour, minute, millisec, post_utc_unknown_word, delim) = struct.unpack('<HBBBBHIH', s[idx:(idx+14)])
    assert(delim == 0)
    idx += 14

    xxx = struct.unpack('<d', s[(idx):(idx+8)])[0]
    checksum = s[idx+8]

    date_str = '%02d/%02d/%04d' %(day, month, year)
    time_str = '%02d:%02d:%02.3f' %(hour, minute, millisec/1000.0)
    return xxx


def parse_sss(s):
    assert(len(s) >= sss_bytes)

    assert(ord(s[0]) == fmt_version)
    assert(ord(s[1]) == sss_opcode)
    idx = 2

    (year, month, day, hour, minute, millisec, post_utc_unknown_word, delim) = struct.unpack('<HBBBBHIH', s[idx:(idx+14)])
    date_str = '%02d/%02d/%04d' %(day, month, year)
    time_str = '%02d:%02d:%02.3f' %(hour, minute, millisec/1000.0)
    assert(delim == 0)
    idx += 14

    port_floats = struct.unpack('<ffff', s[idx:(idx+16)])
    port_num_bytes = struct.unpack('<I', s[(idx+16):(idx+20)])[0]
    idx += 20
    port_intensities = [ord(v) for v in s[idx:(idx+port_num_bytes)]]
    idx += port_num_bytes

    stbd_floats = struct.unpack('<ffff', s[idx:(idx+16)])
    stbd_num_bytes = struct.unpack('<I', s[(idx+16):(idx+20)])[0]
    idx += 20
    stbd_intensities = [ord(v) for v in s[idx:(idx+stbd_num_bytes)]]
    idx += stbd_num_bytes

    checksum = s[idx]

    port_floats_str = '%.1f,%.1f,%.1f,%.2f' % port_floats
    port_int_str = ','.join('%d' % v for v in port_intensities)
    stbd_floats_str = '%.1f,%.1f,%.1f,%.2f' % stbd_floats
    stbd_int_str = ','.join('%d' % v for v in stbd_intensities)
    return port_int_str, stbd_int_str, port_floats_str, stbd_floats_str

def parse_logdoc(input_file):
    # read input file
    with open(input_file, 'rb') as f:
        data = f.read()
    f.close()

    output_file = '.'.join(input_file.split('.')[:-1]) + '.log'
    idx = 0
    # read header
    off_head = 65664
    #header_line = data[idx:(idx+off_head)]
    header_line = data[idx:(idx+65664)]
    idx += 65664
    # iterate through the file byte at time
    codes = {pos_opcode:['POS', pos_bytes, 'parse_pos(ss)'],
             hdg_opcode:['HDG', hdg_bytes, 'parse_hdg(ss)'],
             dpt_opcode:['DPT', dpt_bytes, 'parse_dpt(ss)'],
             vel_opcode:['VEL', vel_bytes, 'parse_vel(ss)'],
             xxx_opcode:['XXX', xxx_bytes, 'parse_xxx(ss)'],
             sss_opcode:['SSS', sss_bytes, 'parse_sss(ss)'],
             }
    count = 0
    ping = 0
    all_data = []
    while idx < len(data):
        # skip FF FF FF FF
        idx += 4
        # last line
        if idx+1 >= len(data):
            break
        # get data type
        opcode = ord(data[idx+1])

        name = codes[opcode][0]
        num_bytes = codes[opcode][1]
        ss = data[idx:idx+num_bytes]
        func = codes[opcode][2]
        ##if opcode == pos.opcode:
        if name == 'POS':
            # each data point always starts with a POS value
            # so write last ping's value now
            # TODO
            if ping:
                all_data.append([ping, date_str, time_str, lat, lon, hdg, dpt, vel,
                            port_settings, stbd_settings, port, stbd])
            date_str, time_str, lat, lon = eval(func)
            ping += 1
            if not ping%100:
               print("Reading Ping %s" %ping)
        elif name == 'HDG':
            hdg = eval(func)
        elif name == 'DPT':
            dpt = eval(func)
        elif name == 'VEL':
            vel = eval(func)
        elif name == 'SSS':
            port, stbd, port_settings, stbd_settings = eval(func)
        idx += num_bytes
        count += 1
        ## debug
        #for c in data[idx-10:idx+10]:
        #    print('%02X' %ord(c))

    allpd = pd.DataFrame(columns=['ping', 'date', 'time', 'lat', 'lon',
                                'hdg', 'depth', 'vel', 'port_settings',
                                 'stbd_settings', 'port', 'stbd'], data=all_data)
    allpd.to_csv(output_file, sep=' ', index=False, header=True)


if __name__ == '__main__':
    infile = sys.argv[1]
    parse_logdoc(infile)
