import zlib, codecs
from ByteArray import ByteArray

class Records:
	__slots__ = ('client','server','Cursor')
	def __init__(self, client,server):
		self.client, self.Cursor = client, client.Cursor
		self.server = server
    
	def loadrecord(self,_id):
		packet = []
		self.Cursor.execute("select name,code from records where id = %s", [_id])
		d = self.Cursor.fetchall()
		_name = d[0][0]
		_code = int(d[0][1])
		with open(f'packets/{_id}.dat', 'rb') as f:
                        _data = f.read()
                        f.close()
		p = ByteArray(zlib.decompress(_data))
		i = p.readShort()
		x = 0 
		while i > x:
		    t = p.readInt() / 1000
		    d = p.readByte()
		    if d == 0:
                        m = b'\x00' + p.read(p.readShort())
		    else:
                        m = bytearray([d, p.readByte()])
		    packet.append([t,m])
		    x+=1
		return [_name,_code, packet]
     
	def saverecord(self,packets):
		p = ByteArray()
		p.writeShort(len(packets))
		for packet in packets:
		    p.writeInt(int(packet[0] * 1000))
		    p.writeByte(packet[1][0])
		    if packet[1][0] == 0:
                        p.writeShort(len(packet[1][1:]))
                        p.write(packet[1][1:])
		    else:
                        p.writeByte(packet[1][1])

		self.Cursor.execute("insert into records values (%s, %s, %s, %s)", [self.server.lastRecordID, self.client.playerName, str(self.server.lastRecordID)+".dat", self.client.room.mapCode])
		with open(f'packets/{self.server.lastRecordID}.dat', 'wb') as f:
                    f.write(zlib.compress(p.bytes))
		self.server.lastRecordID +=1
		self.server.updateConfig()

