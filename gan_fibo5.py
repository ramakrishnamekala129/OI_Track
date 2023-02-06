# -*- coding: utf-8 -*-
"""
Created on Tue May 31 11:13:46 2022
@author: ramak
"""

import streamlit as st
import math
import pandas as pd
from datetime import datetime, timedelta,date
import numpy as np
from streamlit_autorefresh import st_autorefresh

m=st.sidebar.text_input('Option Range',value=10)


def check_strength(lvl,direction='buy'):
    if direction=='buy':
        if (lvl['PE']/ lvl['CE']) > 1.9:
            return 'Strong Support'
        elif 1 < (lvl['PE']/ lvl['CE']) < 1.9:
            return 'Weak Support'
        elif (lvl['PE']/ lvl['CE']) <0.6:
            return 'Strong Resistance'
        elif ((lvl['PE']/ lvl['CE']) < 1):
            return 'Weak Resistance'
        else:
            return 'Wait time'
    else:
        if (lvl['CE']/ lvl['PE']) > 1.9:
            return 'Strong Resistance'
        elif (lvl['CE']/ lvl['PE']) < 1.9:
            return 'Weak Resistance'
        elif (lvl['CE']/ lvl['PE']) <0.6:
            return 'Strong Support'
        elif ((lvl['CE']/ lvl['PE']) < 1):
            return 'Weak Support'
        else:
            return 'Wait time'



def check_strengthdaily(lvl,direction='buy'):
    if direction=='buy':
        if (lvl['PE_change']/ lvl['CE_change']) > 1.9:
            return 'Strong Support'
        elif 1 < (lvl['PE_change']/ lvl['CE_change']) < 1.9:
            return 'Weak Support'
        elif (lvl['PE_change']/ lvl['CE_change']) <0.6:
            return 'Strong Resistance'
        elif ((lvl['PE_change']/ lvl['CE_change']) < 1):
            return 'Weak Resistance'
        else:
            return 'Wait time'
    else:
        if (lvl['CE_change']/ lvl['PE_change']) > 1.9:
            return 'Strong Resistance'
        elif 1<(lvl['CE_change']/ lvl['PE_change']) < 1.9:
            return 'Weak Resistance'
        elif (lvl['CE_change']/ lvl['PE_change']) <0.6:
            return 'Strong Support'
        elif ((lvl['CE_change']/ lvl['PE_change']) < 1):
            return 'Weak Support'
        else:
            return 'Wait time'



def movers(lvl):
    for i,g in lvl.items():
        print(i,g)




def analysis(symbol,ltp,nextlvl):
    indexltp=ltp
    if symbol=='Nifty':
    	key=50
    else:
    	key=100
    mod=int(indexltp)%key
    if mod <25:
        atmstrike = int(math.floor(indexltp/key))*key
    else:
        atmstrike = int(math.ceil(indexltp/key))*key

    b1=0
    s1=0
    store=[]
    for i in range(0,int(m)-1):
        a=atm-(key*i)
        #print(k)
        buy=nextlvl[(str(float(a)))]
        if a <= indexltp:
            if b1==0:
                r=int(buy['PE']/buy['CE'])
                if buy['PE_change']>buy['CE_change'] and (buy['PE']/buy['CE'])>1.9:
                    store.append(f'buy level {a} Strong Movers')
                    b1=1
                elif 1.3< buy['PE_change']<buy['CE_change'] and (buy['PE']/buy['CE'])>1.9:
                    store.append(f'buy level {a} Weak Movers')
                elif buy['PE_change']>buy['CE_change'] and (buy['PE']/buy['CE'])>1.3:
                    store.append(f'buy level undecicive {a} Strong Movers')
                    #b1=1
                elif buy['PE_change']<buy['CE_change'] and (buy['PE']>buy['CE']):
                    store.append(f'buy level undecicive {a} Weak Movers')
        b=atm+(key*i)
        sell=nextlvl[(str(float(b)))]
        if b >= indexltp:
            if s1==0:
                r=int(sell['CE']/sell['PE'])
                if sell['CE_change']>sell['PE_change'] and (sell['CE']/sell['PE'])>1.9:
                    store.append(f'sell level {b} Strong Movers')
                    s1=1
                elif 1.3<sell['CE_change']<sell['PE_change'] and (sell['CE']/sell['PE'])>1.9:
                    store.append(f'sell level {b} Weak Movers')
                elif sell['CE_change']<sell['PE_change'] and (sell['CE']/sell['PE'])>1.3:
                    store.append(f'sell level undecicive {b} Weak Movers')
                elif sell['CE_change']>sell['PE_change'] and sell['CE']>sell['PE']:
                    store.append(f'sell level undecicive {b} Strong Movers')
    
    
    finalmovers=0
    finalmove=[]
    
    for i in range(0,int(m)):
        a=atm-(key*i)
        #k1=k
        buy=nextlvl[(str(float(a)))]
        j=check_strength(buy,'buy')
        k=check_strengthdaily(buy,'buy')
        finalmovers+=buy['PE_change']-buy['CE_change']
        finalmove.append(f'strike lvl {a} Buy ' + j+' todays ' +k)
        b=atm+(key*i)
        sell=nextlvl[(str(float(b)))]
        finalmovers+=sell['PE_change']-sell['CE_change']
        j=check_strength(sell,'sell')
        k=check_strengthdaily(sell,'sell')
        finalmove.append(f'strike lvl {b} Sell ' + j+' todays ' +k)
    
    move='Buyers are dominating the Market' if finalmovers >0 else 'Sellers are dominating the Market'
    return pd.DataFrame(store),pd.DataFrame(finalmove),move









def optionchainbnf(symbol,expiry):
	import requests

	headers = {
	    'authority': 'api.stocksrin.com',
	    'accept': 'application/json, text/plain, */*',
	    'accept-language': 'en-US,en;q=0.9',
	    'origin': 'https://www.stocksrin.com',
	    'referer': 'https://www.stocksrin.com/',
	    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104", "Opera GX";v="90"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-site',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100',
	}

	params = (
	    ('symbol', symbol),
	    ('expiry', expiry),
	    ('lastTimeStamp', ''),
	    ('forcedDataLoad', 'true'),
	)

	response = requests.get('https://api.stocksrin.com/srOptionChain/chain', headers=headers, params=params)
	return response.json()
def expirybnf(symbol):
	import requests

	headers = {
	    'authority': 'api.stocksrin.com',
	    'accept': 'application/json, text/plain, */*',
	    'accept-language': 'en-US,en;q=0.9',
	    'origin': 'https://www.stocksrin.com',
	    'referer': 'https://www.stocksrin.com/',
	    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104", "Opera GX";v="90"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-site',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100',
	}

	params = (
	    ('symbol', symbol),
	)

	r = requests.get('https://api.stocksrin.com/srOptionChain/expiry', headers=headers, params=params)

	#NB. Original query string below. It seems impossible to parse and
	#reproduce query strings 100% accurately so the one below is given
	#in case the reproduced version is not "correct".
	# response = requests.get('https://api.stocksrin.com/srOptionChain/expiry?symbol=BankNifty', headers=headers)



	r=r.json()
	return r



#usdinr epiry
def usdinr(m):
    import requests
    
    headers = {
        'authority': 'api.stocksrin.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.stocksrin.com',
        'referer': 'https://www.stocksrin.com/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Opera GX";v="91", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.72',
    }
    
    response = requests.get('https://api.stocksrin.com/currency/liveData/expiry', headers=headers)
    k=response.json()
    allof=[]
    
    for i in k:
        import requests
        
        headers = {
            'authority': 'api.stocksrin.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://www.stocksrin.com',
            'referer': 'https://www.stocksrin.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104", "Opera GX";v="90"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100',
        }
        
        params = {
            'symbol': 'USDINR',
            'expiry': i,
        }
        
        response = requests.get('https://api.stocksrin.com/currency/liveData/optionModel', params=params, headers=headers)
        #print(i)
        for j in response.json()['datums']:
            #print(j['strikePrice'])
            allof.append(j['strikePrice'])
        #print(i)
    allof=list(set(allof))
    allr={}
    for a in allof:
        allr[str(a)]={
            'CE':0,
            'PE':0,
            'CE_Change':0,
            'PE_Change':0
            
            }
    
    for i in k:
        import requests
        
        headers = {
            'authority': 'api.stocksrin.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://www.stocksrin.com',
            'referer': 'https://www.stocksrin.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104", "Opera GX";v="90"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100',
        }
        
        params = {
            'symbol': 'USDINR',
            'expiry': i,
        }
        
        response = requests.get('https://api.stocksrin.com/currency/liveData/optionModel', params=params, headers=headers)
        #print(i)
        for j in response.json()['datums']:
            if j['strikePrice'] in allof:
                #print(j.keys())
                if 'CE' in list(j.keys()):
                    #print(j['CE']['openInterest'])
                    #print(j['CE']['changeinOpenInterest'])
                    allr['{}'.format(j['strikePrice'])]['CE']=(allr['{}'.format(j['strikePrice'])]['CE']) +j['CE']['openInterest']
                    allr['{}'.format(j['strikePrice'])]['CE_Change']=(allr['{}'.format(j['strikePrice'])]['CE_Change']) +j['CE']['changeinOpenInterest']
                if 'PE' in list(j.keys()):
                    #print(j['PE']['openInterest'])
                    #print(j['PE']['changeinOpenInterest'])
                    allr['{}'.format(j['strikePrice'])]['PE']=(allr['{}'.format(j['strikePrice'])]['PE']) +j['PE']['openInterest']
                    allr['{}'.format(j['strikePrice'])]['CE_Change']=(allr['{}'.format(j['strikePrice'])]['PE_Change']) +j['PE']['changeinOpenInterest']
        
        #print()
        #break
        import math
        indexltp=(response.json()['underlyingValue'])*1000           
        mod=int(indexltp*100)%250
        #print(mod)
        if mod <25:
            atmstrike = int(math.floor(indexltp/250))*250/1000
        else:
            atmstrike = int(math.ceil(indexltp/250))*250/1000
        #print(atmstrike)
        allrl={}
        alk=[]
        for i in range(0,int(m)):
            alk.append(atmstrike+(i*.25))
            alk.append(atmstrike-(i*.25))
            #allrl[str(atmstrike+(i*.25))]=allr[str(atmstrike+(i*.25))]
            #allrl[str(atmstrike-(i*.25))]=allr[str(atmstrike-(i*.25))]]
        alk.sort()
        for i in alk:
            allrl[str(i)]=allr[str(i)]
        return allrl


def chaindata(symbol,expiry):
	import requests

	headers = {
	    'authority': 'api.stocksrin.com',
	    'accept': 'application/json, text/plain, */*',
	    'accept-language': 'en-US,en;q=0.9',
	    'origin': 'https://www.stocksrin.com',
	    'referer': 'https://www.stocksrin.com/',
	    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104", "Opera GX";v="90"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-site',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100',
	}

	params = (
	    ('symbol', symbol),
	    ('expiry', expiry),
	    #('lastTimeStamp', '07-Oct-22 15:31:39'),
	    ('forcedDataLoad', 'true'),
	)

	response = requests.get('https://api.stocksrin.com/srOptionChain/chain', headers=headers, params=params)

	#NB. Original query string below. It seems impossible to parse and
	#reproduce query strings 100% accurately so the one below is given
	#in case the reproduced version is not "correct".
	# response = requests.get('https://api.stocksrin.com/srOptionChain/chain?symbol=BankNifty&expiry=2022-10-27&lastTimeStamp=07-Oct-22%2015:31:39&forcedDataLoad=true', headers=headers)
	k=response
	return k

def totaloi_bnf(symbol,r):
	global m
	#r=expirybnf(symbol)
	k=(optionchainbnf(symbol,r[0]))#.json()
	indexltp,ltp=k['srIndexQuote']['openValue'],k['srIndexQuote']['spotPrice']
	mod=int(indexltp)%50
	if mod <25:
	    atmstrike = int(math.floor(indexltp/100))*100
	else:
	    atmstrike = int(math.ceil(indexltp/100))*100
	#print(math.floor(k['srIndexQuote']['openValue']))
	#print(atmstrike)
	strikelvl=[]
	nextlvl={}
	for i in range(0,int(m)):
		if symbol=='Nifty':		
		    strikelvl.append(atmstrike + (i*50))
		    strikelvl.append(atmstrike - (i*50))
		else:
                        strikelvl.append(atmstrike + (i*100))
                        strikelvl.append(atmstrike - (i*100))
	strikelvl.append(atmstrike)
	print('strikelvl')
	print(strikelvl)

	for i in k['strikeDataModel']['strikes']:
	    #print(i)
	    if i['strikePrice'] in strikelvl:
	        nextlvl[str(i['strikePrice'])]={'CE':0,
	        'PE':0,
	        'CE_change':0,'PE_change':0}
	    #print(nextlvl)


	for expiry1 in r:

		k=chaindata(symbol,expiry1)
		#print(expiry)
		if k.status_code==200:
			#print(k)
			k=k.json()
			#print(k)
			for i in k['strikeDataModel']['strikes']:
				#print()
				if i['strikePrice'] in strikelvl:
					#print(i['strikePrice'])
					#print(nextlvl[str(i['strikePrice'])])
					#print(i)
					if str(i['strikePrice']) in list(nextlvl.keys()):
						if i['CE']==None:
							i['CE']={'oi':0
							,'oic':0
							}


						if (i['PE'])==None:
							i['PE']={'oi':0
							,'oic':0
							}
						nextlvl[str(i['strikePrice'])]={'CE': (nextlvl[str(i['strikePrice'])]['CE']+i['CE']['oi']),
						'PE':(nextlvl[str(i['strikePrice'])]['PE']+i['PE']['oi']),
						'CE_change':(nextlvl[str(i['strikePrice'])]['CE_change']+i['CE']['oic']),'PE_change':(nextlvl[str(i['strikePrice'])]['PE_change']+i['PE']['oic'])}
		return nextlvl,atmstrike,ltp



st_autorefresh(interval=45*1000, key="dataframerefresh")

st.sidebar.title("Fibo Level Maker")
#st.markdown("This application is a Share Price dashboard for Top 5 Gainers and Losers:")
st.sidebar.markdown("This application is a which gives Fibo entry levels")
def CurrencyDivider(select):
    if 'JPY' in select:
       return 1000
    elif 'XAU/USD' in select:
    	return 100
    elif 'USD' in select:
        return 100000
    elif 'INR' in select:
        return 10000
    else:
    	return 1

select=1
#st.sidebar.title("Pairs")
#select = st.sidebar.selectbox('Select a Pair', pairs, key='1')
#currency = st.sidebar.checkbox('Currency')
#st.json(response.json())


import plotly.express as px 


niftyoi = st.sidebar.checkbox('Nifty OI')
bankniftyoi = st.sidebar.checkbox('BankNifty OI')
usdinroi = st.sidebar.checkbox('USDINR OI')

if niftyoi:
	r=expirybnf('Nifty')
	nextlvl,atm,ltp=totaloi_bnf('Nifty',r)
	a,b,c=analysis('Nifty',ltp,nextlvl)
	#print(pd.DataFrame(nextlvl).T)
	allexp=st.multiselect('Select Nifty Expirys',r)
	print(allexp)
	if allexp:
		st.write("Custom NIFTY OI")
		nextlvl1, a1,v1=totaloi_bnf('Nifty',allexp)
		#fig1=px.bar(pd.DataFrame(nextlvl1).T, orientation='h' ,text_auto=True,barmode='group')
		fig1=px.bar(pd.DataFrame(nextlvl1).T, orientation='h' ,text_auto=True,barmode='group',color_discrete_map={'CE':'#FF2B2B','CE_change':'#FFABAB','PE':'#0068C9','PE_change':'#83C9FF'})


		st.write(fig1)
	st.write("NIFTY TOTAL OI")
	st.write(c)
	#fig=px.bar(pd.DataFrame(nextlvl).T, orientation='h' ,text_auto=True,barmode='group')
	fig=px.bar(pd.DataFrame(nextlvl).T, orientation='h' ,text_auto=True,barmode='group',color_discrete_map={'CE':'#FF2B2B','CE_change':'#FFABAB','PE':'#0068C9','PE_change':'#83C9FF'})

	st.table(a)
	st.write(fig)
	
	st.table(b)


if bankniftyoi:
	r=expirybnf('BankNifty')
	nextlvl,atm,ltp=totaloi_bnf('BankNifty',r)
	a,b,c=analysis('BankNifty',ltp,nextlvl)
	#print(pd.DataFrame(nextlvl).T)
	#st.bar_chart(pd.DataFrame(nextlvl).T)
	allexp=st.multiselect('Select BankNifty Expirys',r)
	print(allexp)
	if allexp:
		st.write("Custom BANKNIFTY OI")
		nextlvl1, a1,v1=totaloi_bnf('BankNifty',allexp)
		print(nextlvl1)
		#fig1=px.bar(pd.DataFrame(nextlvl1).T, orientation='h' ,text_auto=True,barmode='group')
		fig1=px.bar(pd.DataFrame(nextlvl1).T, orientation='h' ,text_auto=True,barmode='group',color_discrete_map={'CE':'#FF2B2B','CE_change':'#FFABAB','PE':'#0068C9','PE_change':'#83C9FF'})
		st.write(fig1)
	st.write("BANKNIFTY TOTAL OI")
	st.write(c)

	st.table(a)
	#fig=px.bar(pd.DataFrame(nextlvl).T, orientation='h' ,text_auto=True,barmode='group')
	fig=px.bar(pd.DataFrame(nextlvl).T, orientation='h' ,text_auto=True,barmode='group',color_discrete_map={'CE':'#FF2B2B','CE_change':'#FFABAB','PE':'#0068C9','PE_change':'#83C9FF'})

	st.write(fig)
	st.table(b)
	

if usdinroi:
	nextlvl=usdinr(m)
	#print(pd.DataFrame(nextlvl).T)
	#st.bar_chart(pd.DataFrame(nextlvl).T)
	fig=px.bar(pd.DataFrame(nextlvl).T, orientation='h' ,text_auto=True,barmode='group')
	st.write(fig)









