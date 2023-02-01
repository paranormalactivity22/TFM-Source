# coding: utf-8
import re, time, random, string, time as thetime

# Library
from datetime import datetime

class Utils:

    @staticmethod
    def getTFMLangues(langueID):
        return {0:"GB", 1:"FR", 2:"RU", 3:"BR", 4:"ES", 5:"CN", 6:"TR", 7:"VK", 8:"PL", 9:"HU", 10:"NL", 11:"RO", 12:"ID", 13:"DE", 14:"AR", 15:"PH", 16:"LT", 17:"JP", 18:"CH", 19:"FI", 20:"CZ", 21:"SK", 22:"HR", 23:"BG", 24:"LV", 25:"HE", 26:"IT", 27:"ET", 28:"AZ", 29:"PT", 30:"ZA", 31:"VU", 32:"BA", 33:"AD", 34:"MW", 35:"DK", 36:"EE", 37:"NR", 38:"TO", 39:"MG", 40:"WS", 41:"MH", 42:"GL", 43:"BI", 44:"RW", 45:"KE", 46:"RW", 47:"MT", 48:"MY", 49:"HT", 50:"LU", 51:"NO", 52:"UZ", 53:"BO", 54:"ST", 55:"RU", 56:"RS", 57:"AM", 58:"BW", 59:"AL", 60:"SL", 61:"SZ", 62:"SO", 63:"SE", 64:"TL", 65:"TM", 66:"FJ", 67:"SN", 68:"NG", 69:"IS", 70:"GR", 71:"BY", 72:"KG", 73:"MD", 74:"MN", 75:"TJ", 76:"UA", 77:"KZ", 78:"IL", 79:"PK", 80:"IR", 81:"NP", 82:"IN", 83:"BD", 84:"LK", 85:"KR", 86:"KH", 87:"ER", 88:"GE", 89:"MM", 90:"BT", 91:"VI", 92:"MV", 93:"EG"}[langueID]

    @staticmethod
    def getLangues():
        return {0:"GB", 1:"FR", 2:"RU", 3:"BR", 4:"ES", 5:"CN", 6:"TR", 7:"VK", 8:"PL", 9:"HU", 10:"NL", 11:"RO", 12:"ID", 13:"DE", 14:"AR", 15:"PH", 16:"LT", 17:"JP", 18:"CH", 19:"FI", 20:"CZ", 21:"SK", 22:"HR", 23:"BG", 24:"LV", 25:"HE", 26:"IT", 27:"ET", 28:"AZ", 29:"PT", 30:"ZA", 31:"VU", 32:"BA", 33:"AD", 34:"MW", 35:"DK", 36:"EE", 37:"NR", 38:"TO", 39:"MG", 40:"WS", 41:"MH", 42:"GL", 43:"BI", 44:"RW", 45:"KE", 46:"RW", 47:"MT", 48:"MY", 49:"HT", 50:"LU", 51:"NO", 52:"UZ", 53:"BO", 54:"ST", 55:"RU", 56:"RS", 57:"AM", 58:"BW", 59:"AL", 60:"SL", 61:"SZ", 62:"SO", 63:"SE", 64:"TL", 65:"TM", 66:"FJ", 67:"SN", 68:"NG", 69:"IS", 70:"GR", 71:"BY", 72:"KG", 73:"MD", 74:"MN", 75:"TJ", 76:"UA", 77:"KZ", 78:"IL", 79:"PK", 80:"IR", 81:"NP", 82:"IN", 83:"BD", 84:"LK", 85:"KR", 86:"KH", 87:"ER", 88:"GE", 89:"MM", 90:"BT", 91:"VI", 92:"MV", 93:"EG"}
		
    @staticmethod
    def getLangueID(langue=None):
        datas = {"EN":0, "FR":1, "RU":2, "BR":3, "ES":4, "CN":5, "TR":6, "VK":7, "PL":8, "HU":9, "NL":10, "RO":11, "ID":12, "DE":13, "E2":14, "AR": 15, "PH":16, "LT":17, "JP":18, "CH":19, "FI":20, "CS":21, "HR":22, "SK": 23, "BG":24, "LV":25, "HE":26, "IT":27, "ET":28, "AZ":29, "PT":30}
        if langue in datas:
            return datas[langue]
        return 1# fr
    
    @staticmethod
    def getTime():
        return int(int(str(time.time())[:10]))

    @staticmethod
    def buildMap(*elems):
        m = {}
        i = 0
        while i < len(elems):
            m[elems[i]] = elems[i + 1]
            i += 2
        return m
        
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

    @staticmethod
    def EncodeIP(ip):
        ip = '.'.join([hex(int(x)+256)[3:].upper() for x in ip.split('.')])
        return '#' + ip

    @staticmethod
    def DecodeIP(ip):
        ip = ip[1:]
        result = []
        for i in ip.split('.'):
            if int(i, 16):
                result.append(int(i, 16))
            else:
                result.append(int(i))
        result = [str(i) for i in result]
        return '.'.join(result)