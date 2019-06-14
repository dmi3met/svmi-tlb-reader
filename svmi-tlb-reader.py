import struct
import time
import csv


def unpack(data_format, start, length):
    (result,) = struct.unpack(data_format,
                              data[start+offset:start+length+offset])
    return result


def safe_decode(number):
    try:
        result = number.decode()
    except UnicodeDecodeError:
        result = ''
    return result

parsed_rows = []
filename = "message.tbl"

with open(filename, "rb") as f:
    data = f.read()

offset = 0
record_len = unpack('B', 2, 1) + 8
# record_len = 152(no caller id), 176 (with caller id)

for offset in range(0, len(data)-record_len, record_len):
    time1 = unpack('<i', record_len-32, 4)       # unix time
    filename = unpack('<i', 20, 4)               # 4 byte hex
    number_a = unpack('18s', record_len-92, 18)  # 18-char string
    number_b = unpack('18s', record_len-68, 18)

    time1 = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(time1))
    # for date correction 2 years (time1-63072000)
    filename = "'%08X" % filename
    number_a = safe_decode(number_a)
    number_b = safe_decode(number_b)
    parsed_rows.append({'time': time1, 'filename': filename,
                        'number_a': number_a, 'number_b': number_b})

with open('message.csv', 'w', newline='') as f:
    fieldnames = ['time', 'filename', 'number_a', 'number_b']
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(parsed_rows)
