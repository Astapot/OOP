from datetime import date

d1 = date.today()
d0 = date(1996, 10, 21)
delta = d1 - d0
print(delta.days // 365)