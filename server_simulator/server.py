# -*- coding: utf8 -*-
#!/usr/bin/env python

import asyncio
import datetime
import random
import websockets
import time
import json
import sys
import re
import codecs
import threading


securities = {}
securitiesNum = {}
batchMap = {}
quoteMap = {}
tighteningMap = {}
mylist = []

def isHangul(text):
	#Check the Python Version
	pyVer3 =  sys.version_info >= (3, 0)

	if pyVer3 : # for Ver 3 or later
		encText = text
	else: # for Ver 2.x
		if type(text) is not unicode:
			encText = text.decode('utf-8')
		else:
			encText = text

	hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', encText))
	return hanCount > 0



# 배치 A0011
def batch(data, test=False):
	category = [
		("DATA구분", 2),
		("정보구분", 2),
		("시장구분", 1),
		("종목코드", 12),
		("일련번호", 8),
		("단축코드", 9),
		("종목한글약명", 40),
		("종목영문약명", 40),
		("영업일자", 8),
		("정보분배그룹번호", 5),
		("증권그룹ID", 2),
		("단위매매체결여부", 1),
		("락구분코드", 2),
		("액면가변경구분코드", 2),
		("시가기준가격종목여부", 1),
		("재평가종목사유코드", 2),
		("기준가격변경종목여부", 1),
		("임의종료발동조건코드", 1),
		("시장경보경고예고여부", 1),
		("시장경보구분코드", 2),
		("지배구조우량여부", 1),
		("관리종목여부", 1),
		("불성실공시지정여부", 1),
		("우회상장여부", 1),
		("거래정지여부", 1),
		("지수업종대분류코드", 3),
		("지수업종중분류코드", 3),
		("지수업종소분류코드", 3),
		("업종ID", 10),
		("KOSPI200섹터업종", 1),
		("시가총액규모코드", 1),
		("(유가)제조업여부(코스닥)중소기업여부", 1),
		("KRX100종목여부", 1),
		("FILLER", 1),
		("(유가)지배구조지수종목여부(코스닥)소속부구분코드", 1),
		("투자기구구분코드", 2),
		("(유가)KOSPI여부", 1),
		("(유가)KOSPI100여부(코스닥)FILLER", 1),
		("(유가)KOSPI50여부", 1),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("기준가격", 9),
		("전일종가구분코드", 1),
		("전일종가", 9),
		("전일누적체결수량", 12),
		("전일누적거래대금", 18),
		("상한가", 9),
		("하한가", 9),
		("대용가격", 9),
		("액면가", 12),
		("발행가격", 9),
		("상장일자", 8),
		("상장주식수(상장증권수)", 15),
		("정리매매여부", 1),
		("주당순이익(EPS)부호", 1),
		("주당순이익(EPS)", 9),
		("주가수익율(PER)부호", 1),
		("주가수익율(PER)", 6),
		("주당순이익산출제외여부", 1),
		("주당순자산가치(BPS)부호", 1),
		("주당순자산가치(BPS)", 9),
		("주당순자산비율(PBR)부호", 1),
		("주당순자산비율(PBR)", 6),
		("주당순자산가치산출제외여부", 1),
		("결손여부", 1),
		("주당배당금액", 8),
		("주당배당금액산출제외여부", 1),
		("배당수익율", 7),
		("존립개시일자", 8),
		("존립종료일자", 8),
		("행사기간개시일자", 8),
		("행사기간종료일자(권리행사기간만료일자)", 8),
		("ELW신주인수권증권_행사가격", 12),
		("자본금", 21),
		("신용주문가능여부", 1),
		("지정가호가조건구분코드", 5),
		("시장가호가조건구분코드", 5),
		("조건부지정가호가조건구분코드", 5),
		("최유리지정가호가조건구분코드", 5),
		("최우선지정가호가조건구분코드", 5),
		("증자구분코드", 2),
		("종류주권구분코드", 1),
		("국민주여부", 1),
		("평가가격", 9),
		("최저호가가격", 9),
		("최고호가가격", 9),
		("정규장매매수량단위", 5),
		("시간외매매수량단위", 5),
		("리츠종류코드", 1),
		("목적주권종목코드", 12),
		("FILLER", 1),
		("FILLER", 3),
		("FILLER", 1),
		("FILLER", 4),
		("통화ISO코드", 3),
		("국가코드", 3),
		("시장조성가능여부", 1),
		("시간외매매가능여부", 1),
		("장개시전시간외종가가능여부", 1),
		("장개시전시간외대량매매가능_여부", 1),
		("장개시전시간외바스켓가능_여부", 1),
		("예상체결가공개여부", 1),
		("공매도가능여부", 1),
		("FILLER", 3),
		("추적수익율배수부호", 1),
		("추적수익율배수", 11),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 3),
		("FILLER", 1),
		("FILLER", 1),
		("Regulation_S_적용종목여부", 1),
		("기업인수목적회사여부", 1),
		("과세유형코드", 1),
		("대용가격사정비율", 11),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("FILLER", 1),
		("(코스닥)투자주의환기종목여부", 1),
		("상장폐지일자", 8),
		("FILLER", 1),
		("단기과열종목구분코드", 1),
		("ETF복제방법구분코드", 1),
		("FILLER", 1),
		("KOSPI200고배당지수여부", 1),
		("KOSPI200저변동성지수여부", 1),
		("FILLER", 3),
		("만기일자", 8),
		("FILLER", 3),
		("분배금형태코드", 2),
		("만기상환가격결정시작일자", 8),
		("만기상환가격결정종료일자", 8),
		("ETP상품구분코드", 1),
		("지수산출기관코드", 1),
		("지수시장분류ID", 6),
		("지수일련번호", 3),
		("추적지수레버리지인버스구분코드", 2),
		("참고지수레버리지인버스구분코드", 2),
		("지수자산분류ID1", 6),
		("지수자산분류ID2", 6),
		("LP주문가능여부", 1),
		("KOSDAQ150지수종목여부", 1),
		("저유동성여부", 1),
		("이상급등여부", 1),
		("FILLER", 149),
		("FF", 1)
	] #800
	sum = 0
	result = {}
	for i in category:
		# 한글 파싱 (한글자당 2길이)
		if(i[0].strip() == "종목한글약명"):
			rlength = i[1]
			count = 0
			rcount = 0
			while(rlength > rcount):
				token = data[sum+count:sum+count+1]
				rcount += 1
				count += 1
				if(isHangul(token)):
					rcount +=1
			result[i[0].strip()] = data[sum:sum+count].strip()
			sum += count

		else:
			result[i[0].strip()] = data[sum:sum+i[1]].strip()
			sum += i[1]

		if test:
			print(i[0].strip(),result[i[0].strip()])

	return result

# 실시간 호가 B6011
def realTimeQuote(data, test=False):
	category = [
		("DATA구분", 2),
		("정보구분", 2),
		("시장구분", 1),
		("종목코드", 12),
		("종목일련번호", 5),
		("누적체결수량", 12),
		("호가_OCCURS_10", 0),
		("매도호가1", 9),
		("매수호가1", 9),
		("매도호가_잔량1", 12),
		("매수호가_잔량1", 12),
		("매도호가2", 9),
		("매수호가2", 9),
		("매도호가_잔량2", 12),
		("매수호가_잔량2", 12),
		("매도호가3", 9),
		("매수호가3", 9),
		("매도호가_잔량3", 12),
		("매수호가_잔량3", 12),
		("매도호가4", 9),
		("매수호가4", 9),
		("매도호가_잔량4", 12),
		("매수호가_잔량4", 12),
		("매도호가5", 9),
		("매수호가5", 9),
		("매도호가_잔량5", 12),
		("매수호가_잔량5", 12),
		("매도호가6", 9),
		("매수호가6", 9),
		("매도호가_잔량6", 12),
		("매수호가_잔량6", 12),
		("매도호가7", 9),
		("매수호가7", 9),
		("매도호가_잔량7", 12),
		("매수호가_잔량7", 12),
		("매도호가8", 9),
		("매수호가8", 9),
		("매도호가_잔량8", 12),
		("매수호가_잔량8", 12),
		("매도호가9", 9),
		("매수호가9", 9),
		("매도호가_잔량9", 12),
		("매수호가_잔량9", 12),
		("매도호가10", 9),
		("매수호가10", 9),
		("매도호가_잔량10", 12),
		("매수호가_잔량10", 12),
		("10단계호가매도총잔량", 12),
		("10단계호가매수총잔량", 12),
		("FILLER", 12),
		("FILLER", 12),
		("장종료후시간외_매도총호가잔량", 12),
		("장종료후시간외_매수총호가잔량", 12),
		("세션ID", 2),
		("보드ID", 2),
		("예상체결가격", 9),
		("예상체결수량", 12),
		("경쟁대량_방향구분", 1),
		("FILLER", 7),
		("FF", 1)
	] #560
	sum = 0
	result = {}
	for i in category:
		if test:
			print(i[0],data[sum:sum+i[1]])
		result[i[0].strip()] = data[sum:sum+i[1]].strip()
		sum += i[1]

	return result

# 실시간 체결 A3011
def realTimeTightening(data, test=False):
	category = [
		("DATA구분", 2),
		("정보구분", 2),
		("시장구분", 1),
		("종목코드", 12),
		("종목일련번호", 5),
		("보드ID", 2),
		("전일대비(기준가대비)구분", 1),
		("전일대비", 9),
		("체결가격", 9),
		("체결수량", 10),
		("세션ID", 2),
		("시가", 9),
		("고가", 9),
		("저가", 9),
		("누적체결수량", 12),
		("누적거래대금", 18),
		("최종매도매수구분코드", 1),
		("체결가와1호가일치여부", 1),
		("체결시각", 6),
		("LP보유수량", 15),
		("매도1호가", 9),
		("매수1호가", 9),
		("FILLER", 6),
		("FF", 1)
	] #160

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
	print("실시간 체결")
	print("============================================")
	T21testdata = "A3011KR707197000800731G2300000000000000635000000001104000000000000000635000000635000000000011000000000000069850022073000000000000000000000000000000006350      "
	realTimeTightening(T21testdata, True)

	print()
	print("============================================")
	print("실시간 호가")
	print("============================================")
	T31testdata = "B6011KR571901A58600004000000000000000001020000000000000000003000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000                        00000000000000000000000010G10000000000000000000000       "
	realTimeQuote(T31testdata, True)

	print()
	print("============================================")
	print("배치")
	print("============================================")
	#35
	batchtestdata = "A0011KR57010177A400000001F7010177A도쿄오피스1                             Tokyo Office 1                          2018021300004BCN0000N00N1N00NNNNN                      N  03NNN             000001000300000100000000000000000000000000000000000000130000000070000000066000000100000000000100020171024000000066001012N+000000000+000000 +000000000+000000 N00000000 00000002017090620220906                000000000000000000066001012000000N0000700000000000000000000000N0000000000000000000000000000000100000                      KRW410NNNNNYY   +00000000000        NN000070000000    N         0  NN                                                           NNNN                                                                                                                                                     "
	#26
	batchtestdata2 = "A0011KR574201767000000012F74201767하나대체티마크그랜드부동산1호 A         Hana Alternative Tmark Real Estate 1-A  2018021300004BCN0000N00N1N00NNNNN                      N  03NNN             000000939300000093900000000000000000000000000000000000122000000065800000072000000100000000000100020160831000000060555978N+000000000+000000 +000000000+000000 N00000000 00000002016072620210726                000000000000000000060555978000000N0000700000000000000000000000N0000000000000000000000000000000100000                      KRW410NNNNNYY   +00000000000        NN000072000000    N         0  NN                                                           NNNN                                                                                                                                                     "
	batch(batchtestdata2, True)

def interval(sec = 0.01):
	time.sleep(sec)

# 배치 마지막: 349437줄
def generateByBatch():
	f = open("./data/20180213.KSC","rb")
	lineNum = 0
	while True:
		lineNum += 1
		line = f.readline()[:]
		code = line[:5]

		if code == b"A0011": # 배치
			line = line[:-2].decode('euc-kr')
			r = batch(line)
			if r["종목코드"] == "999999999999" and lineNum > 340000:
				break

			jdata = json.dumps(r, ensure_ascii=False)
			batchMap[r["종목코드"]] = jdata
			securities[r["종목한글약명"]] = r["종목코드"]
			securitiesNum[r["종목코드"]] = r["종목한글약명"]


	f.close()

async def listenClient(websocket, path):
	print("connected listen")
	global tighteningMap
	global quoteMap
	async for message in websocket:
		if len(message) > 5:
			if message not in mylist:
				mylist.append(message)
				print("registered : ",message)
				if message in tighteningMap:
					tdata = json.dumps(tighteningMap[message], ensure_ascii=False)
					await websocket.send(tdata)
				if message in quoteMap:
					qdata = json.dumps(quoteMap[message], ensure_ascii=False)
					await websocket.send(qdata)

async def sendData(websocket):
	global tighteningMap
	global quoteMap

	isSimultaneousCall = True
	print("sending Batch...")
	for info in batchMap:
		temp = {}
		temp["batch"] = batchMap[info]
		sdata = json.dumps(temp, ensure_ascii=False)
		await websocket.send(sdata)
		await asyncio.sleep(0.0001)

		# for testing
		#break

	f = open("./data/20180213.KSC","rb")

	print("sending StockInfo...")
	# end of batch

	lineNum = 0
	while True:
		stockCode = ""
		lineNum += 1
		line = f.readline()
		code = line[:5]

		temp = {}

		if code == b"A0011": # 배치
			continue
			pass
		elif code == b"A3011": # 실시간 채결

			line = line[:-2].decode('euc-kr')
			r = realTimeTightening(line)
			jdata = json.dumps(r, ensure_ascii=False)
			tighteningMap[r["종목코드"]] = jdata

			temp["tightening"] = jdata
			stockCode = r["종목코드"]
			pass
		elif code == b"B6011": # 실시간 호가
			line = line[:-2].decode('euc-kr')
			r = realTimeQuote(line)

			jdata = json.dumps(r, ensure_ascii=False)
			quoteMap[r["종목코드"]] = jdata

			temp["quote"] = jdata
			stockCode = r["종목코드"]

			if int(r["매수호가5"]) > 0:
				isSimultaneousCall = False
			pass
		else:
			continue
			pass

		if len(mylist) > 0:
			if stockCode in mylist:
				sdata = json.dumps(temp, ensure_ascii=False)
				await websocket.send(sdata)
				if isSimultaneousCall:
					await asyncio.sleep(0.0001)
				else:
					await asyncio.sleep(0.1)

	f.close()

async def runServer(websocket, path):

	print("connected")

	# t = threading.Thread(target=sendData, args=(websocket,))
	# t.start()

	await sendData(websocket)

    # while True:
    #     now = datetime.datetime.utcnow().isoformat() + 'Z'
    #     await websocket.send(now)
    #     await asyncio.sleep(random.random() * 3)





def readFromFile():

	f = open("./data/20180213.KSC","rb")
	lineNum = 0
	while True:
		lineNum += 1
		line = f.readline()[:]
		code = line[:5]

		temp = {}

		if code == b"A0011": # 배치
			line = line[:-2].decode('euc-kr')
			r = batch(line)
			jdata = json.dumps(r, ensure_ascii=False)
			batchMap[r["종목코드"]] = jdata
			securities[r["종목한글약명"]] = r["종목코드"]
			securitiesNum[r["종목코드"]] = r["종목한글약명"]
			pass
		elif code == b"A3011": # 실시간 채결

			line = line[:-2].decode('euc-kr')
			r = realTimeTightening(line)
			jdata = json.dumps(r, ensure_ascii=False)
			tighteningMap[r["종목코드"]] = jdata

			temp["tightening"] = jdata
			pass
		elif code == b"B6011": # 실시간 호가
			line = line[:-2].decode('euc-kr')
			r = realTimeQuote(line)

			jdata = json.dumps(r, ensure_ascii=False)
			quoteMap[r["종목코드"]] = jdata

			temp["quote"] = jdata
			pass
		else:
			continue
			pass

	f.close()

print("========= STS =========")
print("generating Batch...")
generateByBatch() # total 2968

mylist.append("KR7005930003")

start_server = websockets.serve(runServer, '127.0.0.1', 5678)
start_server_listen = websockets.serve(listenClient, '127.0.0.1', 6789)
print("socket server is running!")
asyncio.get_event_loop().run_until_complete(start_server_listen)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
