import csv
from collections import Counter

import itchat
from matplotlib import pyplot


def analyse_friends(friends):
    """ 好友性别 """
    sex = list(map(lambda x: x['Sex'], friends[1:]))
    counts = dict(Counter(sex).items())
    counts = [counts[0], counts[1], counts[2]]
    labels = ['Unknown', 'Male', 'Female']
    colors = ['green', 'blue', 'pink']
    pyplot.figure(figsize=(7, 5), dpi=80)
    pyplot.axes(aspect=1)
    pyplot.pie(
        counts,
        labels=labels,
        colors=colors,
        labeldistance=1.1,
        autopct='%3.2f%%',
        shadow=False,
        startangle=90,
        pctdistance=0.6,
    )
    pyplot.legend(loc='upper right')
    pyplot.title('wechat friends sex')
    pyplot.savefig('sex.png')
    pyplot.show()


def analyse_location(friends):
    """ 好友坐标 """
    headers = ['NickName', 'Province', 'City']
    with open('location.csv', 'w', encoding='utf-8', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, headers)
        writer.writeheader()
        for friend in friends[1:]:
            row = dict()
            row['NickName'] = friend['NickName']
            row['Province'] = friend['Province']
            row['City'] = friend['City']
            writer.writerow(row)


if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    friend_data = itchat.get_friends(update=True)
    analyse_friends(friend_data)
    analyse_location(friend_data)
    itchat.run(debug=True)
