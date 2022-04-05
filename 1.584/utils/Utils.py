# coding: utf-8
import re, time, random, string, time as thetime

# Library
from datetime import datetime

class Utils:

    @staticmethod
    def getTFMLangues(langueID):
        return {0:"EN", 1:"FR", 2:"RU", 3:"BR", 4:"ES", 5:"CN", 6:"TR", 7:"VK", 8:"PL", 9:"HU", 10:"NL", 11:"RO", 12:"ID", 13:"DE", 14:"E2", 15:"AR", 16:"PH", 17:"LT", 18:"JP", 19:"CH", 20:"FI", 21:"CZ", 22:"SK", 23:"HR", 24:"BG", 25:"LV", 26:"HE", 27:"IT", 29:"ET", 30:"AZ", 31:"PT"}[langueID]

    @staticmethod
    def getLangues():
        return {0:"EN", 1:"FR", 2:"RU", 3:"BR", 4:"ES", 5:"CN", 6:"TR", 7:"VK", 8:"PL", 9:"HU", 10:"NL", 11:"RO", 12:"ID", 13:"DE", 14:"E2", 15:"AR", 16:"PH", 17:"LT", 18:"JP", 19:"CH", 20:"FI", 21:"CZ", 22:"SK", 23:"HR", 24:"BG", 25:"LV", 26:"HE", 27:"IT", 29:"ET", 30:"AZ", 31:"PT"}[langueID]
		
    @staticmethod
    def getTime():
        return int(int(str(time.time())[:10]))

    @staticmethod
    def getValue(*array):
        return random.choice(array)

    @staticmethod
    def getDate():
        return str(datetime.now()).replace("-", "/").split(".")[0].replace(" ", " - ")
        
    @staticmethod
    def getHoursDiff(endTimeMillis):
        startTime = Utils.getTime()
        startTime = datetime.fromtimestamp(float(startTime))
        endTime = datetime.fromtimestamp(float(endTimeMillis))
        result = endTime - startTime
        seconds = (result.microseconds + (result.seconds + result.days * 24 * 3600) * 10 ** 6) / float(10 ** 6)
        hours = int(int(seconds) / 3600) + 1
        return hours
    
    @staticmethod
    def getDiffDays(time):
        diff = time - Utils.getTime()
        return diff / (24 * 60 * 60)

    @staticmethod
    def getSecondsDiff(endTimeMillis):
        return int(int(str(thetime.time())[:10]) - endTimeMillis)

    @staticmethod
    def getRandomChars(size):
        return "".join(random.choice(string.digits + string.ascii_uppercase + string.ascii_lowercase) for x in range(size))

    @staticmethod
    def getDaysDiff(endTimeMillis):
        startTime = datetime.fromtimestamp(float(Utils.getTime()))
        endTime = datetime.fromtimestamp(float(endTimeMillis))
        result = endTime - startTime
        return result.days + 1

    @staticmethod
    def parsePlayerName(playerName):
        return (playerName[0] + playerName[1:].lower().capitalize()) if playerName.startswith("*") or playerName.startswith("+") else playerName.lower().capitalize()

    @staticmethod
    def joinWithQuotes(list):
        return "\"" + "\", \"".join(list) + "\""

    @staticmethod
    def getYoutubeID(url):
        matcher = re.compile(".*(?:youtu.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=)([^#\\&\\?]*).*").match(url)
        return matcher.group(1) if matcher else None

    @staticmethod
    def Duration(duration):
        time = re.compile('P''(?:(?P<years>\d+)Y)?''(?:(?P<months>\d+)M)?''(?:(?P<weeks>\d+)W)?''(?:(?P<days>\d+)D)?''(?:T''(?:(?P<hours>\d+)H)?''(?:(?P<minutes>\d+)M)?''(?:(?P<seconds>\d+)S)?'')?').match(duration).groupdict()
        for key, count in time.items():
            time[key] = 0 if count is None else time[key]
        return (int(time["weeks"]) * 7 * 24 * 60 * 60) + (int(time["days"]) * 24 * 60 * 60) + (int(time["hours"]) * 60 * 60) + (int(time["minutes"]) * 60) + (int(time["seconds"]) - 1)

    @staticmethod
    def getUptime(time):
        text = ""
        time = str(time).split(".")[0].split(":")
        hours = time[0]
        minutes = time[1]
        seconds = time[2]

        minutes = minutes.replace("00", "0") if minutes == "00" else minutes.replace("0", "") if len("0") == 1 and not minutes in ["10", "20", "30", "40", "50", "60"] else minutes
        seconds = seconds.replace("00", "0") if seconds == "00" else seconds.replace("0", "") if len("0") == 1 and not seconds in ["10", "20", "30", "40", "50", "60"] else seconds
        if hours > "0": text += hours + (" hours " if hours > "1" else " hour ")
        if minutes > "0": text += minutes + (" minutes " if minutes > "1" else " minute ")
        if seconds > "0": text += seconds + (" seconds " if seconds > "1" else " second ")
        return text
