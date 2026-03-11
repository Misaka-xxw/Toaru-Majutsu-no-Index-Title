"""
File: measures.py
Description: 测量样例图的坐标，用于计算坐标的比例
Author: Misaka-xxw
Created: 2025-03-31
"""
print("横着的图")
xy = [(0, 4), (314, 461), (321, 144), (597, 453), (558, 106), (747, 319), (743, 0), (1233, 489), (1221, 98),
      (1582, 482), (1589, 126), (1933, 463), (144, 498), (584, 1013), (597, 501), (1008, 909), (1001, 487), (1383, 906),
      (1378, 464), (1827, 1019), (636, 937), (1371, 1019)
      ]  # 1937 x 1022超炮横图
w = 1937
h = 1022
font_size = []
middle_xy = []
for i in range(0, len(xy), 2):
    middle_xy.append((((xy[i + 1][0] + xy[i][0]) / 2 - w / 2) / w, ((xy[i + 1][1] + xy[i][1]) / 2 - h / 2) / h))
    font_size.append((xy[i + 1][1] - xy[i][1]) / h)
# print(middle_xy)
i = 6
print((xy[i + 1][0] - xy[i][0]) / w, (xy[i + 1][1] - xy[i][1]) / h)
# print(font_size)

print("竖着的图")
xy = [(482, 1), (757, 329), (605, 339), (804, 569), (463, 468), (631, 658), (447, 671), (818, 1009), (452, 1020),
      (816, 1361), (481, 1368), (786, 1617), (21, 427), (430, 835), (153, 857), (434, 1132), (94, 1144), (439, 1433),
      (4, 1441), (454, 1856), (2,417),(435, 851)
      ]  # 822x 1860超炮竖图
w = 822
h = 1860
font_size = []
middle_xy = []
for i in range(0, len(xy), 2):
    middle_xy.append((((xy[i + 1][0] + xy[i][0]) / 2 - w / 2) / w, ((xy[i + 1][1] + xy[i][1]) / 2 - h / 2) / h))
    font_size.append((xy[i + 1][1] - xy[i][1]) / h)
print(middle_xy)
i = len(xy)-2
print((xy[i + 1][0] - xy[i][0]) / w, (xy[i + 1][1] - xy[i][1]) / h)
print(font_size)

print("小字部分（横）")
xy = [(622,929),(1370,1021)]  # 1937 x 1022超炮横图
w = 1937
h = 1022
font_size = []
middle_xy = []
for i in range(0, len(xy), 2):
    middle_xy.append((((xy[i + 1][0] + xy[i][0]) / 2 - w / 2) / w, ((xy[i + 1][1] + xy[i][1]) / 2 - h / 2) / h))
    font_size.append((xy[i + 1][1] - xy[i][1]) / h)
print(middle_xy)
print(font_size)

print("小字部分（竖）")
xy = [(0,878),(68,1433)]  # 1937 x 1022超炮横图
w = 822
h = 1860
font_size = []
middle_xy = []
for i in range(0, len(xy), 2):
    middle_xy.append((((xy[i + 1][0] + xy[i][0]) / 2 - w / 2) / w, ((xy[i + 1][1] + xy[i][1]) / 2 - h / 2) / h))
    font_size.append((xy[i + 1][1] - xy[i][1]) / h)
print(middle_xy)
print(font_size)

