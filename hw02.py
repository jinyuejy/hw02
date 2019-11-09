# coding=utf-8
# 只适合最新的身份证
# 包含多个扩展库，可能需要安装
import requests
from bs4 import BeautifulSoup
import re
import numpy as num
import xlwt
check = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8',
         5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}
province = {}
city = {}
county = {}
url = 'http://www.mca.gov.cn/article/sj/xzqh/1980/201903/201903011447.html'
response = requests.get(url)
text_need = response.text
# print(text_need)
result_c = re.findall(r'<td class=xl723852>(\d{6})</td>', text_need)
result_z = re.findall(r'<td class=xl723852>.*?([\u4E00-\u9FA5]+).*?</td>', text_need)
# for i in range(len(result_c)):
#   print(f'{result_c[i]}:{result_z[i]}')
# 省市一级代码
accurate_c = re.findall(r'<td class=xl733852>(\d{6})</td>', text_need)
accurate_z = re.findall(r'<td class=xl733852>.*?([\u4E00-\u9FA5]+).*?</td>', text_need, re.S)
# for i in range(len(accurate_z)):
#   print(f'{accurate_c[i]}{accurate_z[i]}')

# 县一级代码
# 3
workbook=xlwt.Workbook()
worksheet1=workbook.add_sheet('省级')
worksheet2=workbook.add_sheet('市级')
worksheet3=workbook.add_sheet('县级')
n1=0
n2=0
for i in range(len(result_c)):
    str1 = ''.join(result_c[i])
    flag = int(str1[-4:6])
    if flag == 0:
        province[result_c[i]] = result_z[i]
        worksheet1.write(n1,0,result_c[i])
        worksheet1.write(n1,1,result_z[i])
        n1+=1
    else:
        city[result_c[i]] = result_z[i]
        worksheet2.write(n2,0,result_c[i])
        worksheet2.write(n2,1,result_z[i])
        n2+=1

for j in range(len(accurate_c)):
    county[accurate_c[j]] = accurate_z[j]
    worksheet3.write(j,0,accurate_c[j])
    worksheet3.write(j,1,accurate_z[j])


workbook.save("区号代码.xls")

print("区号代码.xls已保存至代码所在文件夹")



# 把省市县分开存为字典
# print(province.values())
ID = input('输入一个身份证号：\n')
ID_sex = ''.join(ID)
coe = (num.mat([7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2])).T
che = num.mat(list(map(int, list(ID_sex[0:17]))))
result = (che*coe) % 11
if check[int(result)] == ID[17] and len(ID_sex)==18:
    pa = 1
else:
    pa = 0

print(' ')
if pa == 1:
    ready = re.match(r'\d{6}', ID).group(0)
    jud = ''.join(ready)
    pro = str(jud[0:2])+'0000'
    cit = str(jud[0:4])+'00'
    n1 = ready in county.keys()
    n2 = cit in city.keys()
    n3 = pro in province.keys()
    print('籍贯：',end=' ')
    if n1 == True and n2 == True and n3 == True:
        print(f'{province[pro]} {city[cit]} {county[str(ready)]}')
    elif n1 == True and n3 == True and n2 == False:
        print(f'{province[pro]} {county[str(ready)]}')
    elif n3 == True and n1 == False and n2 == False:
        print(f'{province[pro]}')
    else:
        print('输入错误!')

# 地区识别

    print(' ')
    sex = int(ID_sex[16]) % 2
    print('性别：',end=' ')
    if sex == 0:
        print('女')
    else:
        print('男')

# 性别判定


    #birthday = re.findall(r'19|20\d{6}?', ID)
    #bir = ''.join(birthday)
    print(' ')
    print('出生年月：',end=' ')
    print(f'{ID_sex[6:10]}年{ID_sex[10:12]}月{ID_sex[12:14]}日')
# 出生日期判定
else:
    print('输入错误!!!\n\n\n')


print(' \n\n\n')



input("按任意键退出！")
