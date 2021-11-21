
# importing modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymysql

# https://www.whoishostingthis.com/tools/user-agent/

city = input('Enter your city name : ')
url = 'https://www.zomato.com/'+city+'/top-restaurants'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

response = requests.get(url,headers=header)
html = response.text

soup = BeautifulSoup(html,'html.parser')
print(soup.title.text,'\n')

# scraping raw data and stroing it in a array

top_rest = soup.find_all("div",attrs={"class": "sc-bke1zw-0 fIuLDK"})
#list_tr = top_rest[0].find_all("div",attrs={"class": "sc-bke1zw-1 ixpGXU"})

list_rest=[]
link_temp=[]
cnt=0
for tr in top_rest:
    if(cnt==0):
        #print(tr.text)
        print()
        print()
        #print(tr.text)
        #rsts = tr.find_all('div',class_="sc-bke1zw-1 ixpGXU",class_="sc-bke1zw-1 fuDxvO")
        rsts = tr.find_all('div',class_="sc-bke1zw-1")
        '''for i in rsts:
            print(i.text)
            print()
        print("---------------------------------------")'''
        print(rsts)
        print("-------------------------------------------")
        print() 
        for i in rsts:
            temp=[]
            name = i.select('a',class_='sc-ljNbsN sc-fLRKdW crFNUn')
            link = i.find(href=True)
            print(link['href'])
            print()
            link_temp.append(link['href'])
            for k in name:
                temp.append(k.text)
            list_rest.append(temp)
    cnt+=1

print("-------------------------------------------")
print()     
  
print("Displaying top restaurants in "+ city)
print("-------------------------------------------")
print()
    #dataframe['rest_name']=tr.find("a",attrs={"class": "sc-ljNbsN sc-fLRKdW crFNUn"}).text.replace('\n',' ')
    #print(tr.find("a",attrs={"class": "sc-ljNbsN sc-fLRKdW crFNUn"}))
    #print()
    #i+=1
    #dataframe['rest_add']=tr.find("div",attrs={"class": "sc-ljNbsN sc-hlzYAP fincoD"})
    #dataframe['rest_cuisine']=tr.find("div",attrs={"class": "sc-ljNbsN sc-fLRKdW crFNUn"})
    #dataframe['rest_rating']=tr.find("div",attrs={"class": "sc-1q7bklc-1 cILgox"})
    #list_rest.append(dataframe)
#print(list_rest)
name=[]
cuis=[]
address=[]
print()
for i in range(0,len(list_rest)):
    temp=[]
    name.append(list_rest[i][1])
    print("Restaurant  :  "+list_rest[i][1])
    address.append(list_rest[i][-1])
    print("Address  :  "+list_rest[i][-1])
    temp.append(list_rest[i][2:-2])
    str1 = ''.join(map(str,temp))
    cuis.append(str1)
    print("Cuisine  :  "+str1)
    print("Link  :  "+link_temp[i] )
    print()
    print()

df = pd.DataFrame(list(zip(name,cuis,address,link_temp)),
               columns =['Restaurant Name', 'Cuisine','Address','Link'])


print("Inserting data in database.....")
print()
print("Displaying data from database")
print("---------------------------------------")
print()
# Connect to the database
connection = pymysql.connect(host='localhost',
                         user='root',
                         password='',
                         db='webscraping')
# create cursor
cursor=connection.cursor()
# creating column list for insertion
cols = "`,`".join([str(i) for i in df.columns.tolist()])

# Insert DataFrame recrds one by one.
for i,row in df.iterrows():
    sql = "INSERT INTO `restaurants` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))

    # the connection is not autocommitted by default, so we must commit to save our changes
    connection.commit()

# Execute query
sql = "SELECT * FROM `restaurants`"
cursor.execute(sql)

# Fetch all the records
result = cursor.fetchall()
for i in result:
    print(i)

connection.close()


