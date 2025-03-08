import random
import matplotlib.pyplot as plt

class agent:
    def __init__(self,levelNum):
        self.levelNum = levelNum
        self.currentLevel = 1
        self.probLevel = 0
        ##prob level: open probability
        ## level 0 means 33.75
        ## level 1 means 67.5
        ## level 2 means 100
        self.totalEvilNum = 0
    def showMeWhatYouGot(self):
        print("当前agent已结束")
        print("总共开启恶魔房次数为：",self.totalEvilNum)

    def aTry(self):
        if self.probLevel == 2:
            self.totalEvilNum += 1
            openres[self.currentLevel-1] += 1
            self.probLevel = 0
            return
        if self.probLevel == 1:
            if random.randint(1,100) < 67:
                self.totalEvilNum += 1
                openres[self.currentLevel-1] += 1
                self.probLevel = 0
            else:
                self.probLevel = 2
        if self.probLevel == 0:
            if random.randint(1,100) < 33:
                self.totalEvilNum += 1
                openres[self.currentLevel-1] += 1
                self.probLevel = 0
            else:
                self.probLevel = 1
    def forward(self):
        if self.currentLevel == 1:
            self.currentLevel += 1
            return
        if self.currentLevel == 2:
            self.totalEvilNum += 1
            openres[self.currentLevel-1] += 1
            self.currentLevel += 1
            return
        if self.currentLevel == 8:
            self.aTry()
            #self.showMeWhatYouGot()
            return
        else:
            self.aTry()
            self.currentLevel += 1
            return

res = []
openres = []
for i in range(8):
    openres.append(0)

epoch = 1000000
avg = 0

for i in range(epoch):
    issac = agent(8)
    for i in range(8):
        issac.forward()
    res.append(issac.totalEvilNum)

for i in range(epoch):
    avg += res[i]

print(avg / 1000000)

for i in range(8):
    print(openres[i])

plt.plot(list(range(1,9)),openres,marker='o')
plt.title("每层开启情况")
plt.xlabel("层")
plt.ylabel("开启次数")

plt.grid(True)
plt.show()



