#! /usr/bin/env python
"""
Anqi's code to convert logdoc to csv file
"""
import math
import struct
import sys
import utm


'''
def d2r(d, num_digits=15): # double to rounded double, with max # of digits
  is_neg = (d < 0)
  if is_neg:
    d *= -1
  num_whole = int(math.ceil(math.log10(d)))
  if num_whole < num_digits:
    m = math.pow(10, num_digits-num_whole)
    d = round(d*m)/m
  if is_neg:
    d *= -1
  return d
'''


def d2s(d, num_digits=15): # double to string, with max # of digits, 2nd try
  is_neg = (d < 0)
  if is_neg:
    d *= -1
  num_whole = int(math.ceil(math.log10(d)))
  if num_whole >= num_digits:
    s = '%d' % d
  else:
    m = math.pow(10, num_digits-num_whole)
    d = round(d*m)/m
    fmt = '%%.%df' % num_digits
    s = fmt % d
    if len(s) > num_digits+1: # +1 accounts for decimal point
      s = s[:num_digits+1]
      if s[-1] == '.':
        s = s[:-1]
  if is_neg:
    s = '-' + s
  return s


def srtrim(s): # trim trailing '0' from string
  idx = len(s)
  while idx > 0 and s[idx-1] == '0':
    idx -= 1
  return s[:idx]


class POS:
  NUM_BYTES = 43
  OPCODE = 0x21

  def __init__(self):
    self.fmt_version = 0x01
    self.opcode = POS.OPCODE
    self.year = 0
    self.month = 0
    self.day = 0
    self.hour = 0
    self.minute = 0
    self.millisec = 0
    self.post_utc_unknown_word = 0
    self.delim = 0
    self.zone_char = ''
    self.zone_num = 0
    self.zone_str = ''
    self.northing = 0
    self.easting = 0
    self.latitude = 0
    self.longitude = 0
    self.utm_sixth_field = 0
    self.checksum = 0

  def parse(self, s):
    assert(len(s) >= POS.NUM_BYTES)

    assert(ord(s[0]) == self.fmt_version)
    assert(ord(s[1]) == self.opcode)
    idx = 2

    (self.year, self.month, self.day, self.hour, self.minute, self.millisec, self.post_utc_unknown_word, self.delim) = struct.unpack('<HBBBBHIH', s[idx:(idx+14)])
    assert(self.delim == 0)
    idx += 14

    self.zone_char = s[idx]
    self.zone_num = ord(s[idx+1])
    self.zone_str = '%d%s' % (self.zone_num, self.zone_char)

    (self.northing, self.easting, self.utm_sixth_field) = struct.unpack('<ddd', s[(idx+2):(idx+26)])
    self.checksum = s[idx+26]
    latlon = utm.to_latlon(self.easting, self.northing, self.zone_num, self.zone_char)
    self.latitude = latlon[0]
    self.longitude = latlon[1]

  def __str__(self):
    #date_str = '%02d/%02d/%04d %02d:%02d:%02d' % (self.day, self.month, self.year, self.hour, self.minute, round(self.millisec/1000))
    date_str = '%02d/%02d/%04d %02d:%02d:%02.3f' % (self.day, self.month, self.year, self.hour, self.minute, self.millisec/1000.0)
    #latlon_str = '%s,%s' % (d2s(self.latitude), d2s(self.longitude))
    #utm_str = '%s,%s,%s,%s' % (self.zone_str, d2s(self.northing), d2s(self.easting), d2s(self.utm_sixth_field))
    latlon_str = '%.16f,%.16f' % (self.latitude, self.longitude)
    utm_str = '%s,%.16f,%.16f,%.16f' % (self.zone_str, self.northing, self.easting, self.utm_sixth_field)
    return 'POS,%s,%s,%s' % (date_str, latlon_str, utm_str)


class HDG:
  NUM_BYTES = 25
  OPCODE = 0x20

  def __init__(self):
    self.fmt_version = 0x01
    self.opcode = HDG.OPCODE
    self.year = 0
    self.month = 0
    self.day = 0
    self.hour = 0
    self.minute = 0
    self.millisec = 0
    self.post_utc_unknown_word = 0
    self.delim = 0
    self.data = 0
    self.checksum = 0

  def parse(self, s):
    assert(len(s) >= HDG.NUM_BYTES)

    assert(ord(s[0]) == self.fmt_version)
    assert(ord(s[1]) == self.opcode)
    idx = 2

    (self.year, self.month, self.day, self.hour, self.minute, self.millisec, self.post_utc_unknown_word, self.delim) = struct.unpack('<HBBBBHIH', s[idx:(idx+14)])
    assert(self.delim == 0)
    idx += 14

    self.data = struct.unpack('<d', s[(idx):(idx+8)])[0]
    self.checksum = s[idx+8]

  def __str__(self):
    #date_str = '%02d/%02d/%04d %02d:%02d:%02d' % (self.day, self.month, self.year, self.hour, self.minute, self.millisec/1000.0)
    date_str = '%02d/%02d/%04d %02d:%02d:%02.3f' % (self.day, self.month, self.year, self.hour, self.minute, self.millisec/1000.0)
    data_str = '%.1f' % (self.data)
    return 'HDG,%s,%s' % (date_str, data_str)


class DPT:
  NUM_BYTES = 25
  OPCODE = 0x24

  def __init__(self):
    self.fmt_version = 0x01
    self.opcode = 0x24
    self.year = 0
    self.month = 0
    self.day = 0
    self.hour = 0
    self.minute = 0
    self.millisec = 0
    self.post_utc_unknown_word = 0
    self.delim = 0
    self.data = 0
    self.checksum = 0

  def parse(self, s):
    assert(len(s) >= DPT.NUM_BYTES)

    assert(ord(s[0]) == self.fmt_version)
    assert(ord(s[1]) == self.opcode)
    idx = 2

    (self.year, self.month, self.day, self.hour, self.minute, self.millisec, self.post_utc_unknown_word, self.delim) = struct.unpack('<HBBBBHIH', s[idx:(idx+14)])
    assert(self.delim == 0)
    idx += 14

    self.data = struct.unpack('<d', s[(idx):(idx+8)])[0]
    self.checksum = s[idx+8]

  def __str__(self):
    #date_str = '%02d/%02d/%04d %02d:%02d:%02d' % (self.day, self.month, self.year, self.hour, self.minute, self.millisec/1000.0)
    date_str = '%02d/%02d/%04d %02d:%02d:%02.3f' % (self.day, self.month, self.year, self.hour, self.minute, self.millisec/1000.0)
    data_str = '%.2f' % (self.data)
    return 'DPT,%s,%s' % (date_str, data_str)


class VEL:
  NUM_BYTES = 25
  OPCODE = 0x22

  def __init__(self):
    self.fmt_version = 0x01
    self.opcode = VEL.OPCODE
    self.year = 0
    self.month = 0
    self.day = 0
    self.hour = 0
    self.minute = 0
    self.millisec = 0
    self.post_utc_unknown_word = 0
    self.delim = 0
    self.data = 0
    self.checksum = 0

  def parse(self, s):
    assert(len(s) >= VEL.NUM_BYTES)

    assert(ord(s[0]) == self.fmt_version)
    assert(ord(s[1]) == self.opcode)
    idx = 2

    (self.year, self.month, self.day, self.hour, self.minute, self.millisec, self.post_utc_unknown_word, self.delim) = struct.unpack('<HBBBBHIH', s[idx:(idx+14)])
    assert(self.delim == 0)
    idx += 14

    self.data = struct.unpack('<d', s[(idx):(idx+8)])[0]
    self.checksum = s[idx+8]

  def __str__(self):
    #date_str = '%02d/%02d/%04d %02d:%02d:%02d' % (self.day, self.month, self.year, self.hour, self.minute, round(self.millisec/1000))
    date_str = '%02d/%02d/%04d %02d:%02d:%02.3f' % (self.day, self.month, self.year, self.hour, self.minute, self.millisec/1000.0)
    data_str = '%.9f' % (self.data)
    return 'VEL,%s,%s' % (date_str, srtrim(data_str))


class XXX: # unspecified struct, not found in June's logdoc or csv
  NUM_BYTES = 25
  OPCODE = 0x29

  def __init__(self):
    self.fmt_version = 0x01
    self.opcode = XXX.OPCODE
    self.year = 0
    self.month = 0
    self.day = 0
    self.hour = 0
    self.minute = 0
    self.millisec = 0
    self.post_utc_unknown_word = 0
    self.delim = 0
    self.data = 0
    self.checksum = 0

  def parse(self, s):
    assert(len(s) >= VEL.NUM_BYTES)

    assert(ord(s[0]) == self.fmt_version)
    assert(ord(s[1]) == self.opcode)
    idx = 2

    (self.year, self.month, self.day, self.hour, self.minute, self.millisec, self.post_utc_unknown_word, self.delim) = struct.unpack('<HBBBBHIH', s[idx:(idx+14)])
    assert(self.delim == 0)
    idx += 14

    self.data = struct.unpack('<d', s[(idx):(idx+8)])[0]
    self.checksum = s[idx+8]

  def __str__(self):
    #date_str = '%02d/%02d/%04d %02d:%02d:%02d' % (self.day, self.month, self.year, self.hour, self.minute, round(self.millisec/1000))
    date_str = '%02d/%02d/%04d %02d:%02d:%02.3f' % (self.day, self.month, self.year, self.hour, self.minute, self.millisec/1000.0)
    data_str = '%.13f' % (self.data)
    return 'XXX,%s,%s' % (date_str, data_str)


class SSS:
  NUM_BYTES = 1057
  OPCODE = 0x26

  def __init__(self):
    self.fmt_version = 0x01
    self.opcode = SSS.OPCODE
    self.year = 0
    self.month = 0
    self.day = 0
    self.hour = 0
    self.minute = 0
    self.millisec = 0
    self.post_utc_unknown_word = 0
    self.delim = 0
    self.p_floats = [0,0,0,0]
    self.p_num_bytes = 0
    self.p_intensities = []
    self.s_floats = [0,0,0,0]
    self.s_num_bytes = 0
    self.s_intensities = []
    self.checksum = 0

  def parse(self, s):
    assert(len(s) >= SSS.NUM_BYTES)

    assert(ord(s[0]) == self.fmt_version)
    assert(ord(s[1]) == self.opcode)
    idx = 2

    (self.year, self.month, self.day, self.hour, self.minute, self.millisec, self.post_utc_unknown_word, self.delim) = struct.unpack('<HBBBBHIH', s[idx:(idx+14)])
    assert(self.delim == 0)
    idx += 14

    self.p_floats = struct.unpack('<ffff', s[idx:(idx+16)])
    self.p_num_bytes = struct.unpack('<I', s[(idx+16):(idx+20)])[0]
    idx += 20
    self.p_intensities = [ord(v) for v in s[idx:(idx+s
                                                 :lf.p_num_bytes)]]
    idx += self.p_num_bytes

    self.s_floats = struct.unpack('<ffff', s[idx:(idx+16)])
    self.s_num_bytes = struct.unpack('<I', s[(idx+16):(idx+20)])[0]
    idx += 20
    self.s_intensities = [ord(v) for v in s[idx:(idx+self.p_num_bytes)]]
    idx += self.s_num_bytes

    self.checksum = s[idx]

  def __str__(self):
    #date_str = '%02d/%02d/%04d %02d:%02d:%02d' % (self.day, self.month, self.year, self.hour, self.minute, round(self.millisec/1000))
    date_str = '%02d/%02d/%04d %02d:%02d:%02.3f' % (self.day, self.month, self.year, self.hour, self.minute, self.millisec/1000.0)
    p_floats_str = '%.1f,%.1f,%.1f,%.2f' % self.p_floats
    p_int_str = ','.join('%d' % v for v in self.p_intensities)
    p_str = '%s,%d,%s' % (p_floats_str, self.p_num_bytes, p_int_str)
    s_floats_str = '%.1f,%.1f,%.1f,%.2f' % self.s_floats
    s_int_str = ','.join('%d' % v for v in self.s_intensities)
    s_str = '%s,%d,%s' % (s_floats_str, self.s_num_bytes, s_int_str)
    return 'SSS,%s,P,%s,S,%s' % (date_str, p_str, s_str)


def parse_bin(input_file, output_file):
  with open(input_file, 'rb') as f:
    data = f.read()
  f.close()
  #out_file = open(output_file, 'w+')
  out_file = open(output_file, 'w')
  # OLD WAY: doesn't work if checksum == 0xFF
  #token = struct.pack('>i', -1)
  #lines = data.split(token)
  #header_line = lines[0]
  #lines = lines[1:]

  # BF WAY: count
  idx = 0
  header_line = data[idx:(idx+65664)]
  idx += 65664

  count = 0
  while idx < len(data):
    idx += 4 # skip FF FF FF FF
    # Scan for type
    if idx+1 >= len(data):
      break
    opcode = ord(data[idx+1])
    count +=1
    if opcode == POS.OPCODE:
      d = POS()
      line = data[idx:(idx+d.NUM_BYTES)]
      idx += d.NUM_BYTES
      d.parse(line)
      out_file.write(str(d)+"\n")
    elif opcode == HDG.OPCODE:
      d = HDG()
      line = data[idx:(idx+d.NUM_BYTES)]
      idx += d.NUM_BYTES
      d.parse(line)
      out_file.write(str(d)+"\n")
    elif opcode == DPT.OPCODE:
      d = DPT()
      line = data[idx:(idx+d.NUM_BYTES)]
      idx += d.NUM_BYTES
      d.parse(line)
      out_file.write(str(d)+"\n")
    elif opcode == VEL.OPCODE:
      d = VEL()
      line = data[idx:(idx+d.NUM_BYTES)]
      idx += d.NUM_BYTES
      d.parse(line)
      out_file.write(str(d)+"\n")
    elif opcode == SSS.OPCODE:
      d = SSS()
      line = data[idx:(idx+d.NUM_BYTES)]
      idx += d.NUM_BYTES
      d.parse(line)
      out_file.write(str(d)+"\n")
    elif opcode == XXX.OPCODE:
      d = XXX()
      line = data[idx:(idx+d.NUM_BYTES)]
      idx += d.NUM_BYTES
      d.parse(line)
      out_file.write(str(d)+"\n")
    else:
      print 'WARNING!!!'
      print 'WARNING!!!'
      print 'WARNING!!!'
      print 'Cannot parse further since encountered unknown opcode: %d == 0x%02x' % (opcode, opcode)
      for c in data[idx:idx+10]:
        print '%02X' % ord(c)
      out_file.close()
      return


if __name__ == '__main__':
  '''
  if False:
    pos_str = '01 21 e0 07 06 17 0d 27 c0 ab 02 02 1a 00 00 00 53 0d 8f 38 74 cd 30 84 4f 41 d5 f8 1d bb 04 41 0e 41 f5 2a 56 44 2c 62 0a 40 2f '
    pos_s = ''.join(chr(int(s,16)) for s in pos_str.split())
    p = POS()
    p.parse(pos_s)
    print p

  if False:
    hdg_str = '01 22 e0 07 06 17 0d 27 c0 ab 02 01 08 00 00 00 3a 8a 80 fe d3 11 10 40 c3 '
    hdg_s = ''.join(chr(int(s,16)) for s in hdg_str.split())
    h = VEL()
    h.parse(hdg_s)
    print h

  if False:
    pos_str = '01 26 e0 07 06 17 0d 27 c0 ab 01 01 10 04 00 00 00 00 18 42 00 00 00 00 00 00 28 c2 00 00 a0 41 f4 01 00 00 3c 2b 00 66 68 70 73 7e 7b 74 75 7b 78 71 6e 7b 76 6d 72 69 6b 6d 6c 64 6c 69 6c 67 5d 76 6f 6e 6c 70 70 78 6c 61 68 68 63 6c 6a 69 71 69 69 6c 70 6c 6b 6d 67 6a 68 71 6a 6b 65 5f 52 63 5c 5e 5f 65 64 50 5d 64 5c 61 63 69 6b 65 61 5e 61 5a 67 6a 61 5b 68 70 6f 6d 6e 6d 78 79 6a 74 77 78 75 66 6d 79 70 7e 7a 82 73 68 73 70 72 75 78 76 7a 76 68 68 6f 6b 74 73 6e 66 68 68 6f 75 74 75 71 6e 6b 6d 75 71 5e 6d 63 74 6c 6b 66 69 6e 69 5e 62 62 63 68 71 72 63 68 6b 6b 65 6b 6b 68 60 68 6e 6c 67 6e 6d 64 60 6e 6a 73 71 67 6e 70 5e 6c 6a 73 70 6b 5f 58 5d 60 61 72 6b 6e 76 69 6f 66 6c 6e 6f 6b 75 74 6a 6e 6a 6f 75 6f 71 60 71 78 6a 6d 6a 68 73 75 77 79 75 6a 60 6d 6a 6e 65 6e 70 72 71 71 73 76 66 77 74 73 72 71 6a 67 71 71 6f 79 6e 6f 6c 6d 73 73 76 72 77 71 73 68 5b 6b 6f 6b 63 77 76 73 74 72 6f 63 75 72 72 74 75 62 5e 70 78 6f 70 6f 74 75 62 65 6e 6e 6b 68 70 76 72 68 68 6f 79 5d 71 71 75 6d 6e 6b 6d 76 6b 66 73 70 77 78 77 64 7b 7f 7d 7b 7f 83 7e 77 83 7a 7d 88 7f 86 85 7f 7f 77 89 77 78 7a 76 76 7e 83 83 7b 7e 75 76 6c 6f 75 74 69 73 7d 7b 76 72 73 6a 70 71 75 71 75 7d 75 71 6e 64 76 76 74 75 74 79 81 75 76 72 76 6e 71 76 76 6e 6d 7b 7a 76 74 7d 72 6e 6f 64 70 7a 69 6c 6f 75 72 75 76 69 72 73 73 7e 6f 66 7e 73 74 6c 64 68 6a 66 66 75 78 72 71 70 77 75 77 79 83 85 75 79 7c 73 72 6e 68 74 6d 75 73 6c 68 78 75 77 74 73 76 74 79 73 76 6f 75 72 6b 6d 6f 67 71 70 74 78 7b 7c 7d 76 73 75 71 75 6d 6f 6c 74 75 71 67 63 66 72 7b 71 73 74 7b 71 6b 5d 72 6c 68 6c 64 61 7a 6c 70 77 73 70 77 77 00 00 18 42 00 00 00 00 00 00 28 c2 00 00 a0 41 f4 01 00 00 0f 05 00 67 7e 80 7f 79 79 73 81 82 75 6e 6a 60 79 79 61 6d 6a 70 72 74 71 6a 69 72 65 6f 6e 5e 5b 5d 64 6b 6e 6e 6c 69 6d 6d 64 69 6c 5c 67 59 65 67 66 65 60 64 60 61 64 5f 66 68 64 4f 67 5d 60 69 69 65 67 64 5b 5a 65 5a 5f 5f 5e 5d 5b 4f 53 60 56 63 73 74 6d 74 6c 72 6c 79 6e 7f 6c 73 79 7c 96 8c 71 74 77 6d 73 6d 79 72 6e 79 75 72 6f 6c 73 75 73 73 75 75 73 65 6f 6b 5f 6b 68 5d 67 65 65 60 54 67 67 65 65 5e 6a 6a 63 62 62 5e 67 66 64 6b 69 5d 5f 64 60 5b 5f 5d 63 62 61 6b 62 62 67 68 65 64 62 5e 66 5e 63 63 62 65 65 66 5f 66 5f 61 66 6e 71 66 5c 63 65 65 62 61 6d 75 62 68 6e 6c 58 66 61 62 6a 65 66 67 58 65 5a 61 65 65 60 6b 6c 60 5e 6c 67 61 5d 68 60 66 5d 5e 5d 6c 67 63 69 6b 61 61 69 6c 69 69 60 5c 6b 69 6b 66 65 6b 5a 6b 5e 6c 6a 6c 6b 59 67 69 6b 65 62 69 68 67 6c 6c 6f 6b 61 6c 6c 69 66 5f 67 69 67 65 68 64 62 68 6a 67 65 5e 67 61 66 66 64 62 61 62 67 6c 67 6d 60 65 62 67 6d 6e 64 69 6d 6f 6c 5d 60 65 66 65 6c 6e 6b 65 68 6a 6d 6c 68 70 71 70 6d 6f 79 7b 69 61 5f 66 6b 6a 70 6b 66 65 6a 6b 6d 6d 61 63 6a 75 6c 59 67 60 61 64 67 6a 68 68 69 6d 6b 60 64 64 6d 65 6b 65 62 6b 6a 64 67 64 63 5f 6a 5b 63 62 62 60 5f 69 5e 64 64 68 6d 6c 65 57 5f 56 5b 69 69 6e 71 72 68 6b 5c 6c 6b 6e 71 70 56 6a 67 6f 73 72 63 6d 6e 6a 61 6c 6b 71 75 72 75 71 65 6c 67 6d 71 6e 71 70 66 68 67 6b 6c 65 70 72 6d 69 6b 66 69 68 63 6a 70 70 6b 70 6f 6d 64 6b 6a 6d 66 66 6a 6d 6b 6d 71 69 6d 69 60 67 6e 67 71 6f 66 6d 6e 71 73 6c 67 6d 6e 6b 62 68 75 6e 6e 6c 6a 78 61 68 68 6a 65 6a 64 5c 65 61 74 '
    pos_s = ''.join(chr(int(s,16)) for s in pos_str.split())
    p = SSS()
    p.parse(pos_s)
    print p
  '''

  if len(sys.argv) < 2:
    print 'Usage: %s FILE.logdoc' % (sys.argv[0])
  else:
    input_file = sys.argv[1]
    output_file = sys.argv[1].replace('.logdoc', '.csv')
    parse_bin(input_file, output_file)
