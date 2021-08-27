job_list = []
#future - add to os.environ


def check_timestamp(timestamp):
    if (len(timestamp) < 4 or len(timestamp) > 5):
        return -1  #Wrong format timestamps
    if len(timestamp) == 4:
        timestamp = "0" + timestamp
    hh = timestamp[:2]
    mm = timestamp[3:]
    try:
        hh = int(hh)
        mm = int(mm)
        if hh > 23 or mm > 59:
            return -3
        else:
            return 1  #Timestamp correct
    except:
        return -2  #Timestamp is not numbers


def format_timestamp(timestamp):
    if len(timestamp) == 4:
        timestamp = "0" + timestamp
    hh = timestamp[:2]
    mm = timestamp[3:]
    return "{}:{}".format(hh, mm)


def add_daily(timestamp, commands):
    global job_list
    resp = check_timestamp(timestamp)
    if resp < 0:
        return resp
    # if formatting true..
    saved_time = gmt7_to_utc(timestamp)
    temp_dict = {'timestamp': saved_time, 'command': commands}
    job_list.append(temp_dict)
    return 1


def utc_to_gmt7(timestamp):  # must be formatted.
    print(timestamp)
    timestamp = format_timestamp(timestamp)
    hh = int(timestamp[:2])
    mm = int(timestamp[3:])
    hh = (hh + 7) % 24
    return "{}:{}".format(hh, mm)


def gmt7_to_utc(timestamp):
    timestamp = format_timestamp(timestamp)
    hh = int(timestamp[:2])
    mm = int(timestamp[3:])
    hh = (int(hh) - 7) % 24
    return "{}:{}".format(hh, mm)


def get_schedule(print_obj=None):
    global job_list
    count = 1
    for x in job_list:
        sent_string = "(" + str(count) + ")" + utc_to_gmt7(
            x["timestamp"]) + "-" + x['command']
        if print_obj is not None:
            print(sent_string)
            print_obj(sent_string)
        else:
            print(sent_string)
        count += 1


def get_raw_schedule():
    global job_list
    return job_list


def del_daily(index):
    assert type(index) == int
    try:
        job_list.pop(index - 1)
        print("--- Deleted schedule ->", index, "---")
        return 1  # success deletion
    except:
        return -1  # delete failed


# def edit_daily () # Not implemented yet.
# #examples...
# add_daily("12.23", "!halo")
# add_daily("13.40", "Test")

# get_schedule()

# del_daily(1)
# get_schedule()
