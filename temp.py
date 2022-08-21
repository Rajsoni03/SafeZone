# Hours Plot Data 
hours_data = {'data': [1, 2, 2, 1, 1], 'cate': [11, 12, 20, 21, 22]}

# 'hoursData': [{"x" : j, "y" : str(i)} 
hoursData = []

IthEle = 0
EleLen = len(hours_data['cate'])
for i in range(24):
	if (IthEle < EleLen and i == hours_data['cate'][IthEle]):
		print(i, hours_data['data'][IthEle])
		hoursData.append({"x" : i, "y" : hours_data['data'][IthEle]})
		IthEle+=1
	else:
		print(i, 0)
		hoursData.append({"x" : i, "y" : 0})

print(hoursData)