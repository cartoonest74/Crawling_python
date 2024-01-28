import re
reg = re.compile(r'JPG|PNG|JPEG',re.IGNORECASE)
arr = ["xx:img/png;sss/ssss/"]
print(reg.search(arr[0]).group())
first_exten =arr[0].find("/")+1
last = arr[0].find(";")
print(arr[0][first_exten:last])
print(last)
test = 'aaaaaaabbbss'
test.replace("a","ggg")
print(test)