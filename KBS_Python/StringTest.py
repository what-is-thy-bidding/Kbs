String = ("T1.B=>T2.B AND T2.B!=T3.B OR T4.B=T5.B AND T1.B=+4").split(" ")

joinCondition=""

for i in String:
    if (i.__contains__("=") and i.count(".")==2) and (not i.__contains__("!")) and (not i.__contains__("<")) and (not i.__contains__(">")):
        joinCondition=i
        break
