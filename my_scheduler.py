from datetime import datetime

job_list = []


def get_now():
    h = datetime.now().hour
    m = datetime.now().minute
    return "{}:{}".format(h, m)


def get_sent_now():  # get all text to send by comparing to recent time
    response_list = []
    now = get_now()
    fmt = '%H:%M'
    job = ""
    for x in job_list:
        job = x['timestamp']
        delta = datetime.strptime(job, fmt) - datetime.strptime(now, fmt)
        if delta.total_seconds() == 0:
            response_list.append(x['command'])
    return response_list


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


def parse_tag(command):
    if command.startswith('@.'):
        command = command[2:]
        command = '@' + command
    return command


def remove_tag(command):
    if command.startswith('@'):
        command = command[1:]
        command = '@.' + command
    return command


def add_daily(timestamp, commands):
    global job_list
    resp = check_timestamp(timestamp)
    if resp < 0:
        return resp
    # if formatting true..
    saved_time = gmt7_to_utc(timestamp)
    commands = parse_tag(commands)
    temp_dict = {'timestamp': saved_time, 'command': commands}
    job_list.append(temp_dict)
    return 1


def utc_to_gmt7(timestamp):
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


def get_schedule():
    global job_list
    count = 1
    for x in job_list:
        sent_string = "(" + str(count) + ") " + utc_to_gmt7(
            x["timestamp"]) + " - " + x['command']
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


# get_job_env()

# # def edit_daily () # Not implemented yet.
# # #examples...
# add_daily("18.47", "!halo")
# add_daily("17.18", "Test")

# print(job_list)

# get_schedule()

# # del_daily(1)
# # get_schedule()

# # print("now UTC=", get_now())
# print("now GMT+7=", utc_to_gmt7(get_now()))

# print(get_sent_now())

# print("Last------------")
# get_job_env()

# set_job_to_env()
