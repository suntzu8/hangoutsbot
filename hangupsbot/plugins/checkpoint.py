import datetime
import math
import pytz

import hangups
import plugins

# 5 hours per checkpoint
CHECKPOINT = 5*60*60
# 7 25 hour 'days' per cycle
CYCLE = 7*25*60*60

def formatTime( dt ):
    return dt.strftime("%I%p on %Y-%m-%d").lstrip("0")

def formatDuration( seconds ):
    seconds = int(seconds)
    hours = seconds // 3600
    seconds = seconds - (hours * 3600)
    minutes = seconds // 60
    seconds = seconds - (minutes * 60)
    return '%sh%sm%ss' % (hours, minutes, seconds)

def _initialise(bot):
    plugins.register_user_command(["checkpoint","cp"])

def cp(bot, event, *args):
    return checkpoint(bot, event, args)

def checkpoint(bot, event, *args):
    now = datetime.datetime.utcnow()
    epoch = datetime.datetime(1970, 1, 1)
    nowTs = (now - epoch).total_seconds()


    cycleStartTs = math.floor(nowTs / CYCLE) * (CYCLE)
    cycleEndTs = cycleStartTs + CYCLE
    cycleEndUtc = datetime.datetime.fromtimestamp(cycleEndTs, pytz.utc)
    cycleEndLocal = cycleEndUtc.astimezone(pytz.timezone("America/New_York"))
    cycleEndsIn = cycleEndTs - nowTs

    checkpointStartTs = math.floor(nowTs / CHECKPOINT) * (CHECKPOINT)
    checkpointEndTs = checkpointStartTs + CHECKPOINT
    checkpointEnd = datetime.datetime.fromtimestamp(checkpointEndTs, pytz.utc)
    checkpointEndLocal = checkpointEnd.astimezone(pytz.timezone("America/New_York"))
    checkpointEndsIn = checkpointEndTs - nowTs

    checkpointsUntilCycle = math.ceil(cycleEndsIn / CHECKPOINT)

    msg = "Checkpoint in <b>{}</b> at <b>{}</b>".format(formatDuration(checkpointEndsIn), formatTime(checkpointEndLocal)) + "<br />" + "Cycle ends in <b>{}</b> at <b>{}</b> ({} checkpoints left)".format(formatDuration(cycleEndsIn), formatTime(cycleEndLocal), checkpointsUntilCycle)
    yield from bot.coro_send_message(event.conv, msg)
    return
