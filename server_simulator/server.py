#!/usr/bin/env python

import asyncio
import datetime
import random
import websockets
import time
import json


securities = {}
securitiesNum = {}
batchMap = {}
quoteMap = {}
tighteningMap = {}
mylist = []



# 배치 
def batch(data, test=False):
	category = [
		("종목코드", 16),
		("공란", 24),
		("종목단축코드", 16),
		("상품코드", 8),
		("종목영문약명", 40), #5
		("시장구분", 3),
		("통화코드", 3),
		("상품구분", 3),
		("가격지표", 1),
		("상장일자", 8), #10
		("만기일자", 8),
		("최초교부일자", 8),
		("최종교부일자", 8),
		("업무일자", 8),
		("결제일자", 8), #15
		("전일종가", 15),
		("만기년월", 6),
		("공란", 2),
		("공란", 3),
		("가격단위", 20), #20
		("가격승수", 12),
		("공란", 70)
	] #290
	sum = 0
	result = {}
	for i in category:
		if test:
			print(i[0],data[sum:sum+i[1]])
		result[i[0].strip()] = data[sum:sum+i[1]].strip()
		sum += i[1]
		
	return result

# 실시간 호가
def realTimeQuote(data, test=False):
	category = [
		("Transaction_Code", 3),
		("시장구분", 3),
		("공란", 2),
		("전송일자", 8),
		("전송시간", 12), #5
		("종목코드", 16),
		("Message_Sequence", 10),
		("공란", 24),
		("거래일자", 8),
		("거래시간", 12), #10
		("매수1단계우선호가건수", 8),
		("매수1단계우선호가잔량", 8),
		("매수1단계우선호가가격", 15),
		("매도1단계우선호가건수", 8),
		("매도1단계우선호가잔량", 8), #15
		("매도1단계우선호가가격", 15),
		("매수2단계우선호가건수", 8),
		("매수2단계우선호가잔량", 8),
		("매수2단계우선호가가격", 15),
		("매도2단계우선호가건수", 8), #20
		("매도2단계우선호가잔량", 8),
		("매도2단계우선호가가격", 15),
		("매수3단계우선호가건수", 8),
		("매수3단계우선호가잔량", 8),
		("매수3단계우선호가가격", 15), #25
		("매도3단계우선호가건수", 8),
		("매도3단계우선호가잔량", 8),
		("매도3단계우선호가가격", 15),
		("매수4단계우선호가건수", 8),
		("매수4단계우선호가잔량", 8), #30
		("매수4단계우선호가가격", 15),
		("매도4단계우선호가건수", 8),
		("매도4단계우선호가잔량", 8),
		("매도4단계우선호가가격", 15),
		("매수5단계우선호가건수", 8), #35
		("매수5단계우선호가잔량", 8),
		("매수5단계우선호가가격", 15),
		("매도5단계우선호가건수", 8),
		("매도5단계우선호가잔량", 8),
		("매도5단계우선호가가격", 15) #40
	] #408
	sum = 0
	result = {}
	for i in category:
		if test:
			print(i[0],data[sum:sum+i[1]])
		result[i[0].strip()] = data[sum:sum+i[1]].strip()
		sum += i[1]

	return result

# 실시간 체결
def realTimeTightening(data, test=False):
	category = [
		("Transaction_Code", 3),
		("시장구분", 3),
		("공란", 2),
		("전송일자", 8),
		("전송시간", 12), #5
		("종목코드", 16),
		("Message_Sequence", 10),
		("공란", 24),
		("체결일자", 8),
		("체결시간", 12), #10
		("현재가", 15),
		("체결수량", 9),
		("누적체결수량", 9),
		("시가", 15),
		("고가", 15), #15
		("저가", 15),
		("시장상태", 2),
		("거래일자", 8)
	] #186

	sum = 0
	result = {}
	for i in category:
		if test:
			print(i[0],data[sum:sum+i[1]])
		result[i[0].strip()] = data[sum:sum+i[1]].strip()
		sum += i[1]
		
	return result

def testData():
	print("============================================")
	print("실시간 체결(trade)")
	print("============================================")
	T21testdata = "T21     201609290907030100006CZ16                                             201609290907030100007659.00000     2        3604     7644.00000     7665.00000     7642.00000       20160929"
	realTimeTightening(T21testdata, True)

	print()
	print("============================================")
	print("실시간 체결(settle)")
	print("============================================")
	T40testdata = "T40E01  20160929064123345829QMZ18                                             2016092906412334582953350                   3        52200          52475          52200          A120160928"
	realTimeTightening(T40testdata, True)

	print()
	print("============================================")
	print("실시간 체결(???)")
	print("============================================")
	T50testdata = "T50E01  201609291505537631376AZ16                                             20160929150548040000                        103082   7675           7696           7668             20160929"
	realTimeTightening(T50testdata, True)

	print()
	print("============================================")
	print("실시간 호가")
	print("============================================")
	T31testdata = "T31                         6NZ16                                             2016092909070307601012      28      7259           11      32      7261           14      43      7258           12      32      7262           16      56      7257           15      55      7263           14      52      7256           17      66      7264           14      52      7255           14      53      7265           "
	realTimeQuote(T31testdata, True)

	print()
	print("============================================")
	print("배치")
	print("============================================")
	batchtestdata = "6AH20                                   6AH0            6A      Australian Dollar Mar'20                E01USDP1042015031620200316                20160928201609287471           2020030 5 11                         0.0001                                                                      "
	batch(batchtestdata, True)

def interval(sec = 0.01):
	time.sleep(sec)

def generateByBatch():
	f = open("./data/stockData.IMDV2","r")
	while True:
		line = f.readline()
		if not line: break

		if len(line) == 291: # 배치
			r = batch(line)
			jdata = json.dumps(r, ensure_ascii=False)
			batchMap[r["종목코드"]] = jdata
			securities[r["종목영문약명"]] = r["종목코드"]
			securitiesNum[r["종목코드"]] = r["종목영문약명"]
		else:
			break
	f.close()



async def runServer(websocket, path):

	print("connected")

	generateByBatch()

	for info in batchMap:
		temp = {}
		temp["batch"] = batchMap[info]
		sdata = json.dumps(temp, ensure_ascii=False)
		print(sdata)
		await websocket.send(sdata)
		await asyncio.sleep(0.01)

	f = open("./data/stockData.IMDV2","r")

	# end of batch

	lineNum = 0
	while True:
		code = ""

		lineNum += 1
		line = f.readline()
		if not line: break

		temp = {}

		if len(line) == 291: # 배치
			pass
		elif len(line) == 187: # 실시간 채결
			r = realTimeTightening(line)
			jdata = json.dumps(r, ensure_ascii=False)
			tighteningMap[r["종목코드"]] = jdata
			code = r["종목코드"]

			temp["tightening"] = jdata
			pass
		elif len(line) == 409: # 실시간 호가
			r = realTimeQuote(line)
			jdata = json.dumps(r, ensure_ascii=False)
			quoteMap[r["종목코드"]] = jdata
			code = r["종목코드"]

			temp["quote"] = jdata
			pass
		else:
			print("wrong data")

		if code in mylist:
			sdata = json.dumps(temp, ensure_ascii=False)
			print(sdata)
			await websocket.send(sdata)
			await asyncio.sleep(0.1)

	f.close()


    # while True:
    #     now = datetime.datetime.utcnow().isoformat() + 'Z'
    #     await websocket.send(now)
    #     await asyncio.sleep(random.random() * 3)





def readFromFile():

	f = open("./data/stockData.IMDV2","r")
	lineNum = 0
	while True:
		lineNum += 1
		line = f.readline()
		if not line: break
		temp = {}

		if len(line) == 291: # 배치
			pass
		elif len(line) == 187: # 실시간 채결
			r = realTimeTightening(line)
			jdata = json.dumps(r, ensure_ascii=False)
			tighteningMap[r["종목코드"]] = jdata
			
			temp["tightening"] = jdata
			pass
		elif len(line) == 409: # 실시간 호가
			r = realTimeQuote(line)
			jdata = json.dumps(r, ensure_ascii=False)
			quoteMap[r["종목코드"]] = jdata

			temp["quote"] = jdata
			pass
		else:
			print("wrong data")
	f.close()



generateByBatch()

mylist.append("6CZ16")
mylist.append("RBJ17")
mylist.append("MJYZ16")

start_server = websockets.serve(runServer, '127.0.0.1', 5678)
print("socket server is running!")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()