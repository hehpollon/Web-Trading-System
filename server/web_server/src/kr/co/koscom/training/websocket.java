package kr.co.koscom.training;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Random;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

import javax.websocket.OnClose;
import javax.websocket.OnError;
import javax.websocket.OnMessage;
import javax.websocket.OnOpen;
import javax.websocket.Session;
import javax.websocket.server.ServerEndpoint;

import org.json.JSONArray;
import org.json.JSONObject;


@ServerEndpoint("/websocket")
public class websocket {

	private List<Session> clients = Collections.synchronizedList(new ArrayList<Session>());

	private ConcurrentHashMap<String, String> A0011_HashMap = new ConcurrentHashMap<String, String>();
	private ConcurrentHashMap<String, String> A3011_HashMap = new ConcurrentHashMap<String, String>();
	private ConcurrentHashMap<String, String> B6011_HashMap = new ConcurrentHashMap<String, String>();

	private SimpleDateFormat dateFormat = new SimpleDateFormat("HH:mm:ss.SSS");
	private Random random = new Random();
	private int timeFlag = 0;
	private int onOpenFlag = 0;

	private int keyInterval = 100;
	private int orderkInterval = 100;
	private int tightInterval = 5 + random.nextInt(10);

	private int qCount = 0;
	private int tCount = 0;

	private int totalTraded = 0;
	private ArrayList<Thread> threads = new ArrayList<Thread>();
	
	private long start = 0;
	private long end = 0;

	@OnMessage
	public void onMessage(String message, Session session) throws Exception {

		//printlnWithTime("OnMessage is called.");
		//printlnWithTime("rcvMsg is : " + message);

		Thread t = new Thread() {
			public void run(){

				if(message.contains("key")) { // Ŭ���̾�Ʈ�κ��� �ü� ��û ���� ���

					Set<String> keySubsInfo = new HashSet<String>();
					//System.out.println("if-clause in onMessage is called.");

					// message ���� ���� �ڵ带 ����
					JSONObject jsonObj = new JSONObject(message);
					String compCode = jsonObj.getString("key");

					// ���� ������ ����ü�� �߰�
					if(!keySubsInfo.contains(compCode))
						keySubsInfo.add(compCode); 

					JSONObject tmpJsonObj;
					JSONObject finJsonObj;

					int prePrice = 0;
					int newPrice = 0;

					// �����ڵ忡 �ش��ϴ� A3011 �����Ϳ� B6011 �����͸� ���� 
					while(true) { 

						Iterator<String> iter = keySubsInfo.iterator();

						while(iter.hasNext()) {

							// A3011 �ʿ��� compCode�� ã��
							String str = iter.next();
							String sndString = A3011_HashMap.get(str);

							// ���� ü�ᰡ�ݰ� ���� ü�ᰡ���� ���ؼ�, �ٸ� ��쿡�� Ŭ���̾�Ʈ�� ����
							if (sndString.compareTo("") != 0) {

								tmpJsonObj = new JSONObject(sndString);
								finJsonObj = new JSONObject(tmpJsonObj.getString("tightening"));

								newPrice = finJsonObj.getInt("ü�ᰡ��");
							}

							try {
								if(newPrice != prePrice) {
									qCount++;
									sendQueue(sndString);
								}
							} catch (Exception e) {
								// TODO Auto-generated catch block
								System.exit(0);
								e.printStackTrace();
							}

							prePrice = newPrice;

							// B6011 ����ü���� compCode�� ã��
							sndString = B6011_HashMap.get(compCode);

							try {
								qCount++;
								sendQueue(sndString);
							} catch (Exception e) {
								// TODO Auto-generated catch block
								System.exit(0);
								e.printStackTrace();
							}

							// ������ �ð���ŭ ����
							try {
								Thread.sleep(keyInterval);
							} catch (InterruptedException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
							}
						}
					}
				}
				else if (message.contains("orderk")) {

					Set<String> orderkSubsInfo = new HashSet<String>();
					//System.out.println("else if-clause in onMessage is called.");

					// message ���� ���� �ڵ带 ����
					JSONObject jsonObj = new JSONObject(message);

					JSONArray orderk = jsonObj.getJSONArray("orderk");
					int len = orderk.length();

					String compCode = "";

					// ���� ������ ����ü�� �߰�
					for(int i = 0 ; i < len; i++) {
						compCode = orderk.get(i).toString();

						if(!orderkSubsInfo.contains(compCode))
							orderkSubsInfo.add(compCode); 
					}

					JSONObject tmpJsonObj;
					JSONObject finJsonObj;

					int prePrice = 0;
					int newPrice = 0;

					// �����ڵ忡 �ش��ϴ� A3011 �����Ϳ� B6011 �����͸� ���� 
					while(true) { 

						Iterator<String> iter = orderkSubsInfo.iterator();

						while(iter.hasNext()) {

							// A3011 �ʿ��� compCode�� ã��
							String str = iter.next();
							String sndString = A3011_HashMap.get(str);

							// ���� ü�ᰡ�ݰ� ���� ü�ᰡ���� ���ؼ�, �ٸ� ��쿡�� Ŭ���̾�Ʈ�� ����
							if (sndString.compareTo("") != 0) {

								tmpJsonObj = new JSONObject(sndString);
								finJsonObj = new JSONObject(tmpJsonObj.getString("tightening"));

								newPrice = finJsonObj.getInt("ü�ᰡ��");
							}

							try {
								if(newPrice != prePrice) {
									qCount++;									
									sendQueue(sndString);
								}
							} catch (Exception e) {
								// TODO Auto-generated catch block
								System.exit(0);
								e.printStackTrace();
							}

							prePrice = newPrice;

							// B6011 ����ü���� compCode�� ã��
							sndString = B6011_HashMap.get(compCode);

							// ȣ���� ��� ���ϹǷ�, Ŭ���̾�Ʈ�� ����
							try {
								qCount++;
								sendQueue(sndString);
							} catch (Exception e) {
								// TODO Auto-generated catch block
								System.exit(0);
								e.printStackTrace();
							}

							// ������ �ð���ŭ ����
							try {
								Thread.sleep(orderkInterval);
							} catch (InterruptedException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
							}
						}
					}
				}
				else { // Ŭ���̾�Ʈ�κ��� �ٽ��� ü�� ��û ���� ���

					//System.out.println("else-clause in OnMessage is called.");

					ConcurrentHashMap<String, Integer> orderMap = new ConcurrentHashMap<String, Integer>();

					boolean isCompleted = false;
					Object randKey;

					// message �� ������ orderMap �� ����
					JSONObject jsonObj = new JSONObject(message);

					String basketName = jsonObj.getString("basketName");
					JSONArray orderLists = jsonObj.getJSONArray("orderLists");
					int len = orderLists.length();

					String stock = "";
					int num = 0;

					for(int i = 0 ; i < len; i++) {

						stock = orderLists.getJSONObject(i).getString("stock");
						num = orderLists.getJSONObject(i).getInt("num");

						orderMap.put(stock, num);
					}

					if(timeFlag == 0) {
						start = System.currentTimeMillis();
						timeFlag++;
					}
						
					// ü���ϸ鼭 Ŭ���̾�Ʈ�� ü�� ���� �۽� (ü�� �Ϸ� �� break)
					while(!isCompleted) {

						// shuffle
						randKey = orderMap.keySet().toArray()[new Random().nextInt(orderMap.keySet().toArray().length)];

						if(orderMap.get(randKey) <= 0)
							continue;

						// �� ������ ���, ü�� ������ �����ϰ� ����
						int cur = orderMap.get(randKey);
						int traded = random.nextInt(cur) % 10 + 1;
						cur = cur - traded;

						// �� ������Ʈ
						orderMap.put(randKey.toString(), cur);

						// ü�� ������ �۽�
						JSONObject tmpJsonObj = new JSONObject();

						tmpJsonObj.put("basketName", basketName);
						tmpJsonObj.put("stock", randKey.toString());
						tmpJsonObj.put("num", Integer.toString(cur));

						JSONObject finJsonObj = new JSONObject();

						finJsonObj.put("result", tmpJsonObj.toString());

						try {
							tCount++;
							sendQueue(finJsonObj.toString());
						} catch (Exception e) {
							// TODO Auto-generated catch block
							System.exit(0);
							e.printStackTrace();
						}

						isCompleted = true;

						// ��� �ֹ��� ü��Ǿ����� Ȯ��
						for(String i : orderMap.keySet()){
							if(orderMap.get(i) != 0)
								isCompleted = false;
						}

						try {
							Thread.sleep(tightInterval);
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
						
						totalTraded += traded;
					}
					printlnWithTime("trade complete.");
				}
			}
		};

		//printlnWithTime("(" + this.toString() + ") # of additional thread is : " + threads.size());
		threads.add(t);
		t.start();
	}

	@OnOpen
	public void onOpen(Session session) throws Exception {

		//printlnWithTime("OnOpen is called.");
		//System.out.println(session);
		//printlnWithTime("(" + this.toString() + ") # of additional thread is : " + threads.size());

		clients.add(session);

		if (onOpenFlag == 0) {

			BufferedReader br = new BufferedReader(new FileReader(new File("C:/Users/������/workspace4/web_server/1_A0011.KSC")));
			BufferedReader br2 = new BufferedReader(new FileReader(new File("C:/Users/������/workspace4/web_server/2_A3011_B6011.KSC")));

			String data;

			// ��ġ ������ ���� �� �����ڵ� �� �� ���� 
			while((data = br.readLine()) != null){

				if(data.contains("9999999"))
					continue;

				String compCode = subString(data, 5, 12).trim();
				String hangul = subString(data, 34, 40).trim();
				String isKospi = subString(data, 174, 1).trim();
				String yesPrice = subString(data, 200, 9).trim();

				if(!A0011_HashMap.containsKey(compCode)) {

					JSONObject tmpJsonObj = new JSONObject();

					tmpJsonObj.put("�����ڵ�", compCode);
					tmpJsonObj.put("�����ѱ۾��", hangul);
					tmpJsonObj.put("(����)KOSPI����", isKospi);
					tmpJsonObj.put("��������", yesPrice);

					// ��� ���� ���ο� ������ �� ������Ʈ
					A0011_HashMap.put(compCode, tmpJsonObj.toString());
				}

				if(!A3011_HashMap.containsKey(compCode))
					A3011_HashMap.put(compCode, "");

				if(!B6011_HashMap.containsKey(compCode))
					B6011_HashMap.put(compCode, "");
			}			

			for(ConcurrentHashMap.Entry<String, String> entry : A0011_HashMap.entrySet()) {

				JSONObject finJsonObj = new JSONObject();
				finJsonObj.put("batch", entry.getValue().toString());

				//System.out.println(finJsonObj.toString());
				sendQueue(finJsonObj.toString());
				Thread.sleep(1);
			}

			br.close();
			printlnWithTime("batch data has been sent.");

			onOpenFlag++;

			Thread t = new Thread() {
				public void run(){

					// ���� raw data�� �����鼭 �޸� ������Ʈ
					while(true) {

						String data;
						String TR;

						try {
							while((data = br2.readLine()) != null) {

								TR = data.substring(0, 5);

								if(TR.compareTo("A3011") == 0) {

									String t_compCode = data.substring(5, 17);

									JSONObject tmpJsonObj = new JSONObject();
									tmpJsonObj.put("�����ڵ�", t_compCode);
									tmpJsonObj.put("���ϴ��(���ذ����)����", data.substring(24, 25));
									tmpJsonObj.put("���ϴ��", Integer.parseInt(data.substring(25, 34))).toString();
									tmpJsonObj.put("ü�ᰡ��", Integer.parseInt(data.substring(34, 43))).toString();
									tmpJsonObj.put("ü�����", Integer.parseInt(data.substring(43, 53))).toString();
									tmpJsonObj.put("�ð�", Integer.parseInt(data.substring(55, 64))).toString();
									tmpJsonObj.put("��", Integer.parseInt(data.substring(64, 73))).toString();
									tmpJsonObj.put("����", Integer.parseInt(data.substring(73, 82))).toString();
									tmpJsonObj.put("�����ŵ��ż������ڵ�", data.substring(112, 113));
									tmpJsonObj.put("ü��ð�", data.substring(114, 120));
									tmpJsonObj.put("�ŵ�1ȣ��", Integer.parseInt(data.substring(135, 144))).toString();
									tmpJsonObj.put("�ż�1ȣ��", Integer.parseInt(data.substring(144, 153))).toString();

									JSONObject finJsonObj = new JSONObject();
									finJsonObj.put("tightening", tmpJsonObj.toString());

									// ��� ���� ���ο� ������ �� ������Ʈ
									A3011_HashMap.put(t_compCode, finJsonObj.toString());
								}
								else {	// B6011

									String t_compCode = data.substring(5, 17);

									JSONObject tmpJsonObj = new JSONObject();
									tmpJsonObj.put("�����ڵ�", t_compCode);

									tmpJsonObj.put("�ŵ�ȣ��1", Integer.parseInt(data.substring(34, 43))).toString();
									tmpJsonObj.put("�ż�ȣ��1", Integer.parseInt(data.substring(43, 52))).toString();
									tmpJsonObj.put("�ŵ�ȣ��_�ܷ�1", Integer.parseInt(data.substring(52, 64))).toString();
									tmpJsonObj.put("�ż�ȣ��_�ܷ�1", Integer.parseInt(data.substring(64, 76))).toString();

									tmpJsonObj.put("�ŵ�ȣ��2", Integer.parseInt(data.substring(76, 85))).toString();
									tmpJsonObj.put("�ż�ȣ��2", Integer.parseInt(data.substring(85, 94))).toString();
									tmpJsonObj.put("�ŵ�ȣ��_�ܷ�2", Integer.parseInt(data.substring(94, 106))).toString();
									tmpJsonObj.put("�ż�ȣ��_�ܷ�2", Integer.parseInt(data.substring(106, 118))).toString();

									tmpJsonObj.put("�ŵ�ȣ��3", Integer.parseInt(data.substring(118, 127))).toString();
									tmpJsonObj.put("�ż�ȣ��3", Integer.parseInt(data.substring(127, 136))).toString();
									tmpJsonObj.put("�ŵ�ȣ��_�ܷ�3", Integer.parseInt(data.substring(136, 148))).toString();
									tmpJsonObj.put("�ż�ȣ��_�ܷ�3", Integer.parseInt(data.substring(148, 160))).toString();

									tmpJsonObj.put("�ŵ�ȣ��4", Integer.parseInt(data.substring(160, 169))).toString();
									tmpJsonObj.put("�ż�ȣ��4", Integer.parseInt(data.substring(169, 178))).toString();
									tmpJsonObj.put("�ŵ�ȣ��_�ܷ�4", Integer.parseInt(data.substring(178, 190))).toString();
									tmpJsonObj.put("�ż�ȣ��_�ܷ�4", Integer.parseInt(data.substring(190, 202))).toString();

									tmpJsonObj.put("�ŵ�ȣ��5", Integer.parseInt(data.substring(202, 211))).toString();
									tmpJsonObj.put("�ż�ȣ��5", Integer.parseInt(data.substring(211, 220))).toString();
									tmpJsonObj.put("�ŵ�ȣ��_�ܷ�5", Integer.parseInt(data.substring(220, 232))).toString();
									tmpJsonObj.put("�ż�ȣ��_�ܷ�5", Integer.parseInt(data.substring(232, 244))).toString();

									tmpJsonObj.put("�ŵ�ȣ��6", Integer.parseInt(data.substring(244, 253))).toString();
									tmpJsonObj.put("�ż�ȣ��6", Integer.parseInt(data.substring(253, 262))).toString();
									tmpJsonObj.put("�ŵ�ȣ��_�ܷ�6", Integer.parseInt(data.substring(262, 274))).toString();
									tmpJsonObj.put("�ż�ȣ��_�ܷ�6", Integer.parseInt(data.substring(274, 286))).toString();

									tmpJsonObj.put("�ŵ�ȣ��7", Integer.parseInt(data.substring(286, 295))).toString();
									tmpJsonObj.put("�ż�ȣ��7", Integer.parseInt(data.substring(295, 304))).toString();
									tmpJsonObj.put("�ŵ�ȣ��_�ܷ�7", Integer.parseInt(data.substring(304, 316))).toString();
									tmpJsonObj.put("�ż�ȣ��_�ܷ�7", Integer.parseInt(data.substring(316, 328))).toString();

									tmpJsonObj.put("�ŵ�ȣ��8", Integer.parseInt(data.substring(328, 337))).toString();
									tmpJsonObj.put("�ż�ȣ��8", Integer.parseInt(data.substring(337, 346))).toString();
									tmpJsonObj.put("�ŵ�ȣ��_�ܷ�8", Integer.parseInt(data.substring(346, 358))).toString();
									tmpJsonObj.put("�ż�ȣ��_�ܷ�8", Integer.parseInt(data.substring(358, 370))).toString();

									tmpJsonObj.put("�ŵ�ȣ��9", Integer.parseInt(data.substring(370, 379))).toString();
									tmpJsonObj.put("�ż�ȣ��9", Integer.parseInt(data.substring(379, 388))).toString();
									tmpJsonObj.put("�ŵ�ȣ��_�ܷ�9", Integer.parseInt(data.substring(388, 400))).toString();
									tmpJsonObj.put("�ż�ȣ��_�ܷ�9", Integer.parseInt(data.substring(400, 412))).toString();

									tmpJsonObj.put("�ŵ�ȣ��10", Integer.parseInt(data.substring(412, 421))).toString();
									tmpJsonObj.put("�ż�ȣ��10", Integer.parseInt(data.substring(421, 430))).toString();
									tmpJsonObj.put("�ŵ�ȣ��_�ܷ�10", Integer.parseInt(data.substring(430, 442))).toString();
									tmpJsonObj.put("�ż�ȣ��_�ܷ�10", Integer.parseInt(data.substring(442, 454))).toString();

									JSONObject finJsonObj = new JSONObject();
									finJsonObj.put("quote", tmpJsonObj.toString());

									// ��� ���� ���ο� ������ �� ������Ʈ
									B6011_HashMap.put(t_compCode, finJsonObj.toString());
								}
							}
						} catch (Exception e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}

						// ���� �� �ּ� ����
						//						try {
						//							Thread.sleep(interval);
						//						} catch (InterruptedException e) {
						//							// TODO Auto-generated catch block
						//							e.printStackTrace();
						//						}
					}
				}
			};
			
			//printlnWithTime("(" + this.toString() + ") # of additional thread is : " + threads.size());
			threads.add(t);
			t.start();

			//br2.close();
			//br3.close();
		}
	}

	@OnClose
	public void onClose(Session session) {

		//printlnWithTime("OnClose is called.");
		end = System.currentTimeMillis();
		
		double runningTime = (end - start) / 1000.0;
		
		DecimalFormat df = new DecimalFormat("#.##");
		df.format(123.435436);
		
		printlnWithTime("# of transmitted quote data is : " + qCount + " (" + df.format(qCount / runningTime) + " per second)");
		printlnWithTime("# of transmitted tightening data is : " + tCount + " (" + df.format(tCount / runningTime) + " per second)");
		printlnWithTime("# of traded stocks is : " + totalTraded + " (" + df.format(totalTraded / runningTime) + " per second)");
		
		printlnWithTime("program is terminated.");
	}

	@OnError
	public void onError(Session session, Throwable ex) {

		//printlnWithTime("OnError is called.");

		//printlnWithTime("\tsession is : " + session);
		//printlnWithTime("\tex is : " + ex);
	}

	private  String subString(String strData, int iStartPos, int iByteLength) {
		byte[] bytTemp = null;
		int iRealStart = 0;
		int iRealEnd = 0;
		int iLength = 0;
		int iChar = 0;

		try {
			// UTF-8�� ��ȯ�ϴ°�� �ѱ� 2Byte, ��Ÿ 1Byte�� ������
			bytTemp = strData.getBytes("EUC-KR");
			iLength = bytTemp.length;

			for(int iIndex = 0; iIndex < iLength; iIndex++) {
				if(iStartPos <= iIndex) {
					break;
				}
				iChar = (int)bytTemp[iIndex];
				if((iChar > 127)|| (iChar < 0)) {
					// �ѱ��� ���(2byte ���ó��)
					// �ѱ��� 2Byte�̱� ������ ���� ���ڴ� ���͵� ���� ��ŵ�Ѵ�
					iRealStart++;
					iIndex++;
				} else {
					// ��Ÿ �۾�(1Byte ���ó��)
					iRealStart++;
				}
			}

			iRealEnd = iRealStart;
			int iEndLength = iRealStart + iByteLength;
			for(int iIndex = iRealStart; iIndex < iEndLength; iIndex++)
			{
				iChar = (int)bytTemp[iIndex];
				if((iChar > 127)|| (iChar < 0)) {
					// �ѱ��� ���(2byte ���ó��)
					// �ѱ��� 2Byte�̱� ������ ���� ���ڴ� ���͵� ���� ��ŵ�Ѵ�
					iRealEnd++;
					iIndex++;
				} else {
					// ��Ÿ �۾�(1Byte ���ó��)
					iRealEnd++;
				}
			}
		} catch(Exception e) {
		}

		return strData.substring(iRealStart, iRealEnd);
	} 

	synchronized void sendQueue(String str) throws Exception {

		//System.out.println("session is : " + clients.get(0));
	
		//printlnWithTime("sndMsg is : " + str);
		clients.get(0).getBasicRemote().sendText(str);
	}
	
	synchronized void printlnWithTime(String str) {
		
		long date = System.currentTimeMillis();

		System.out.print("[" + dateFormat.format(date) + "] ");
		System.out.println(str);
	}
}