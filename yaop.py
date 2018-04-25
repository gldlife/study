import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

#定义请求参数
name_drug='氟氯西林钠阿莫西林胶囊'
data={
	'act':'search',
	'typeid':1,
	'keyword':name_drug,
}

url='http://www.china-yao.com/'


#定义爬取单页数据函数
def get_price_query(url,ws):
	header={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
	r=requests.get(url,headers=header)#,params=data)
	r.encoding='utf-8' #设置网页编码格式
	html=r.text #获取网页源码
	soup=BeautifulSoup(html,'html.parser')
	prices=soup.find('table',class_='table')
	price_data=prices.find_all('tr')
	for item in price_data:
		all_data=item.find_all('td')
		i=1
		price=[]
        #print(all_data)

		for data in all_data:
			print(data.string)
			price.append(data.string)
			i=i+1
			if(i%6==1):
				ws.append(price)
				print()

#获取最大页数
def get_max_num(url,data):
	header={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
	r=requests.get(url,params=data,headers=header)
	r.encoding='utf-8' #设置网页编码格式
	html=r.text #获取网页源码
	soup=BeautifulSoup(html,'html.parser')
	pages=soup.find('ul',class_='pagination')
	pages=pages.find_all('li')
	nums=[]
	for item in pages:
		i=item.a.string
		try:
			nums.append(int(i))
		except:
			continue
	return nums[-1]

#打印每页的访问网址
def get_pages_url():
	urls=[]
	url='http://www.china-yao.com/'
	name_drug='氟氯西林钠阿莫西林胶囊'
	data={
		'act':'search',
		'typeid':1,
		'keyword':name_drug,
	}
	max_num=get_max_num(url,data)
	for i in range(1,max_num):
		data={
			'act':'search',
			'typeid':1,
			'keyword':name_drug,
			'page':i,
		}
		r=requests.get(url,params=data)
		print(r.url)
		urls.append(r.url)
		return urls

#get_pages_url()
#运行程序
wb=Workbook()
ws=wb.active
ws.append(['名称','剂型','规格','供货价','零售价','生产企业'])
for i in range(1,25):
	url='http://www.china-yao.com/?act=search&typeid=1&keyword=%E5%85%AD%E5%91%B3%E5%9C%B0%E9%BB%84%E4%B8%B8&page={}'.format(i)
	print(url)
	get_price_query(url,ws)
#print(price)
wb.save('d:/liuwei.xlsx')
