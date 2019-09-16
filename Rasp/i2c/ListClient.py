from multiprocessing.connection import Client
import time

address = ('localhost', 21122)
conn = Client(address, authkey=b'Welti')
conn.send('{"1":[21, "FALLING"]}')
time.sleep(1)
conn.send('{"1":[18, "RISING"]}')
time.sleep(2)
conn.send('{"3":["DiveideByZero"]}')
conn.send('{"5":[]}')
# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])

# Json string to transmit: {"number of command":[Array of Arguments]}
# Json string to recieve: {"number of event":[Array of Arguments]}
# e.g. {"4":[2,"test"]} | {} required

conn.close()