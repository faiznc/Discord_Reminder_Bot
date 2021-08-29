from datetime import datetime
from replit import db

job_list = []  # Will be unused soon..


def get_now(with_second=False):
    hh = datetime.now().hour
    mm = datetime.now().minute
    hh, mm = reformat_timestamp(hh, mm)
    if with_second:
        ss = datetime.now().second
        return "{}:{}:{}".format(hh, mm, ss)
    else:
        return "{}:{}".format(hh, mm)


def get_sent_now(
):  # get all text and its channel to send by comparing to recent time
    text_list = []
    channel_list = []
    now = get_now()
    fmt = '%H:%M'
    job = ""
    channel_ids = db.keys()
    for channel_id in channel_ids:
        for schedule in db[channel_id]:
            job = schedule['timestamp']
            delta = datetime.strptime(job, fmt) - datetime.strptime(now, fmt)
            if delta.total_seconds() == 0:
                text_list.append(parse_text_command(schedule['command']))
                channel_list.append(channel_id)
    return text_list, channel_list


def parse_text_command(text):  # convert @. to @. Used when schedule match.
    return text.replace("@.", "@")


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


def add_daily(channel_id, timestamp, commands):
    channel_id = str(channel_id)
    local_dict = []
    resp = check_timestamp(timestamp)
    if resp < 0:
        return resp
    # if formatting true..
    saved_time = gmt7_to_utc(timestamp)
    commands = parse_tag(commands)
    temp_dict = {'timestamp': saved_time, 'command': commands}
    if check_channel(channel_id) is True:
        local_dict = db[channel_id]
    local_dict.append(temp_dict)
    db[channel_id] = local_dict
    return 1


def check_channel(channel_id: str):
    try:  # check if channel already exist
        db[channel_id]
        return True  # return 1 if channel exist
    except:  #if does not exist, create empty channel dict
        db[channel_id] = []
        return False


def utc_to_gmt7(timestamp):
    timestamp = format_timestamp(timestamp)
    hh = int(timestamp[:2])
    mm = int(timestamp[3:])
    hh = (hh + 7) % 24
    hh, mm = reformat_timestamp(hh, mm)
    return "{}:{}".format(hh, mm)


def gmt7_to_utc(timestamp):
    timestamp = format_timestamp(timestamp)
    hh = int(timestamp[:2])
    mm = int(timestamp[3:])
    hh = (int(hh) - 7) % 24
    hh, mm = reformat_timestamp(hh, mm)
    return "{}:{}".format(hh, mm)


def reformat_timestamp(hh, mm):
    if mm < 10:
        mm = "0" + str(mm)
    if hh < 10:
        hh = "0" + str(hh)
    return hh, mm


def get_schedule():  #Local to this file
    global job_list
    count = 1
    for x in job_list:
        sent_string = "(" + str(count) + ") " + utc_to_gmt7(
            x["timestamp"]) + " - " + x['command']
        print(sent_string)
        count += 1


def get_raw_schedule(channel_id):
    channel_id = str(channel_id)
    channel_jobs = db[
        channel_id]  #add exception ketika blum ada jadwal / channel di db
    return channel_jobs


def del_daily(channel_id, index):
    assert type(index) == int
    channel_id = str(channel_id)
    try:
        channel_jobs = db[channel_id]
    except:
        return -1  # Channel not found in db.
    try:
        channel_jobs.pop(index - 1)
        # print("--- Deleted schedule ->", index, "---")
        db[channel_id] = channel_jobs
        return 1  # success deletion
    except:
        return -1  # delete failed


def del_all_schedule(channel_id):
    channel_id = str(channel_id)
    try:
        del db[channel_id]
        return True  # channel id deleted.
    except:
        return False  # channel id not found.


def developer_see_all_schedule():
    keys = db.keys()
    print(keys)

    for x in keys:
        print(db[x])

    x, y = get_sent_now()
    print(x)
    print(y)


def see_all():
    channel_ids = db.keys()
    for channel_id in channel_ids:
        job_list = get_raw_schedule(channel_id)
        print("--- ( ID", channel_id, ") ---")
        count = 1
        if len(job_list) < 1:
            print("(No schedule.)")
        else:
            for x in job_list:
                sent_string = "(" + str(count) + ") " + utc_to_gmt7(
                    x["timestamp"]) + " - " + remove_tag(x['command'])
                print(sent_string)
                count += 1
