import python_bitbankcc
import MySQLdb
from datetime import datetime,timedelta
import numpy as np
import time
##MYSQLサーバーへの接続
connection = MySQLdb.connect(db='bitbank_xrp_jpy',user='',passwd='',charset='utf8mb4')

cursor = connection.cursor()
#APIでの価格等々の取得
pub = python_bitbankcc.public()
value = pub.get_ticker(
	'xrp_jpy'
)
#移動平均を取る幅
timeWidth1 = 60
timeWidth2 = 15
#平均値、標準偏差、ボリンジャーバンド

print(value)
last_value = value['last']
#60分間の最終取引価格の配列
LastPrices60min = float(last_value)*np.ones(timeWidth1)
print(datetime.now().strftime('%S'))

while True:
	# 60秒毎に稼働
	if datetime.now().strftime('%S')=='00':
		value = pub.get_ticker('xrp_jpy')
		#各種値の取得
		timestamp = value['timestamp']
		last_value = value['last']
		sell_value = value['sell']
		buy_value = value['buy']
		high_value = value['high']
		low_value = value['low']
		vol_value = value['vol']

		print(value)
		#timestampのJST変換と文字列変換
		unixTime = str(value['timestamp'])[0:10]
		unixTimeint = int(unixTime)
		unixTimestamp = datetime.fromtimestamp(unixTimeint)		

		jstTime = unixTimestamp + timedelta(hours=+9)
		strJSTTime = jstTime.strftime("%Y/%m/%d %H:%M:%S")
		#最終取引価格の更新
		LastPrices60min = np.hstack((LastPrices60min[1:timeWidth1],float(value['last'])))
		LastPrices15min = LastPrices60min[timeWidth1-timeWidth2:timeWidth1]
		#平均値の計算
		Mean60min =LastPrices60min.mean()
		Mean15min =LastPrices15min.mean()
		#標準偏差の計算
		StdDev60 = LastPrices60min.std()
		StdDev15 = LastPrices15min.std()
		#ボリンジャーバンドの計算
		bandHigh60 = Mean60min + 2 * StdDev60
		bandLow60  = Mean60min - 2 * StdDev60
		bandHigh15 = Mean15min + 2 * StdDev15
		bandLow15  = Mean15min - 2 * StdDev15
			
		#DBへの格納
		cursor.execute('INSERT INTO trades VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)',(strJSTTime , sell_value, buy_value,last_value, high_value,low_value,vol_value,Mean60min,StdDev60,bandHigh60,bandLow60,Mean15min,StdDev15,bandHigh15,bandLow15))
		connection.commit()
		cursor.execute('SELECT * FROM trades')
		time.sleep(57)	
	







