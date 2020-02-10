import numpy as np
import matplotlib.pyplot as plt
import math
import random as rd
import statistics as st

import yaml


#(x-h)^2 + 2(y-k)^2.3=r^2

partymap = [
    ["Com","Com","Com","Com","Com","Fas","Fas","Fas","Fas","Fas"],
    ["Com","Com","Com","Com","Com","Fas","Fas","Fas","Fas","Fas"],
    ["Soc","Soc","Soc","Soc","Soc","Con","Con","Con","Con","Con"],
    ["Soc","Soc","Soc","Ctr","Ctr","Ctr","Ctr","Con","Con","Con"],
    ["Soc","Soc","Ctr","Ctr","Ctr","Ctr","Ctr","Ctr","Con","Con"],
    ["Lib","Lib","Ctr","Ctr","Ctr","Ctr","Ctr","Ctr","Lbt","Lbt"],
    ["Lib","Lib","Lib","Ctr","Ctr","Ctr","Ctr","Lbt","Lbt","Lbt"],
    ["Lib","Lib","Lib","Lib","Ctr","Ctr","Lbt","Lbt","Lbt","Lbt"],
    ["Lib","Lib","Lib","Lib","Lib","Lbt","Lbt","Lbt","Lbt","Lbt"],
    ["Lib","Lib","Lib","Lib","Lib","Lbt","Lbt","Lbt","Lbt","Lbt"]
    ]

match = {

    "Com" : "communist",
    "Fas" : "fascist",
    "Soc" : "socialist",
    "Con" : "conservative",
    "Ctr" : "centrist",
    "Lib" : "liberal",
    "Lbt" : "libertarian"
    }


class Seat():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.member = None
    def sit(self,member):
        if self.member:
            self.member.seat = None
        self.member = member
        member.seat = self

class Party():
    def __init__(self,econ=None,pol=None):
        global parties
        global ExistingParties
        self.colour = [rd.random(),rd.random(),rd.random()]
        self.econLean = econ if econ else rd.randint(0,9)
        self.polLean = pol if pol else rd.randint(0,9)
        parties.append(self)
        self.members = []
        self.candidates = []
        self.name = self.genName()
        ExistingParties.append(self.name)
        self.seats = []
        self.cohesion = 0
        self.guaranteedSeats = 0
    def join(self,member):
        self.candidates.append(member)
    def seat(self,member):
        self.members.append(member)
    def calcCohesion(self):
        for i in self.members:
            pass
    def genName(self):
        key = match[partymap[self.econLean][self.polLean]]
        self.key = key
        self.category = partymap[self.econLean][self.polLean]
        key = mDict["parties"][key]
        name = None
        while not name or name in ExistingParties:
            name = (rd.choice(key["prefix"]) + " " if not rd.randint(0,2) else "") + rd.choice(key["middle"]) + " " + rd.choice(key["suffix"])
            name = name.replace("CNAME",countryName)
        return name
    def merge(self,target):
        if self == target: return
        newParty = Party(round(st.mean([self.econLean,target.econLean])),round(st.mean([self.polLean,target.econLean])))
        newParty.members = self.members + target.members
        newParty.candidates = self.candidates + target.candidates
        for member in newParty.candidates:
            member.party = newParty
        if not rd.randint(0,3):
            newParty.name = self.name
        else:
            ExistingParties.remove(self.name)
        print("{}({}) merged with {}({}) to form {}({})!".format(self.name,len(self.members),target.name,len(target.members),newParty.name,len(newParty.members)))
        newParty.guaranteedSeats = len(self.members) + len(target.members)
        self.members = []
        target.members = []
        self.candidates = []
        target.candidates = []
        parties.remove(self)
        parties.remove(target)
        
    def splitUp(self):
        if len(self.candidates) < 20: return
        newEcon = self.econLean + rd.randint(-2,2)
        newPol = self.polLean + rd.randint(-2,2)
        if newEcon < 0: newEcon = 0
        if newEcon > 9: newEcon = 9
        if newPol < 0: newPol = 0
        if newPol > 9: newPol = 9
        newParty = Party(newEcon,newPol)
        newParty.candidates = rd.choices(population=self.candidates,k=rd.randint(1,round(len(self.candidates)/2)))
        newParty.guaranteedSeats = rd.randint(1,round(len(self.candidates)/2))
        for cand in newParty.candidates:
            try:
                self.candidates.remove(cand)
                self.members.remove(cand)
            except:
                pass
        print("{} split from {}!".format(newParty.name,self.name))       
    
        

class Member():
    def __init__(self,parties=None,thisParty=None):
        self.seat = None
        if thisParty:
            self.party = thisParty
            self.polLean = thisParty.polLean
            self.econLean = thisParty.econLean
        else:
            self.polLean = rd.randint(0,9)
            self.econLean = rd.randint(0,9)
            if not parties or not rd.randint(0,100):
                self.party = Party(self.econLean,self.polLean)
            else:
                self.party = rd.choices(population=parties,weights=[len(p.members)**0.1 for p in parties],k=1)[0]
        self.party.join(self)        

def arc(sides, radius=1, rotation=97, translation=None):
    one_segment = math.pi * 2 / sides

    points = [
        (math.sin(one_segment * i + rotation) * radius,
         math.cos(one_segment * i + rotation) * radius)
        for i in range(sides)]

    if translation:
        points = [[sum(pair) for pair in zip(point, translation)]
                  for point in points]

    points = [[p[0],p[1]] for p in points if p[1] >= 11]

    return points


def voteForGovernment(parties,points,fromExisting=False):
    global inPower
    global majority
    totalVotes = 50000
    for party in parties:
        if not rd.randint(0,10):
            party.splitUp()
        elif not rd.randint(0,10):
            party.merge(rd.choice([p for p in parties if p.category == party.category]))
    pVotes = {k:0 for k in parties}
    if fromExisting:
        for k,v in pVotes.items():
            pVotes[k] += (len(k.candidates) + rd.randint(round(-len(k.candidates)/1.3),0))
            totalVotes -= pVotes[k]
    else:
        for k,v in pVotes.items():
            pVotes[k] += rd.randint(1,1)
            totalVotes -= pVotes[k]
    for i in range(totalVotes):
        party = rd.choice(rd.choices(population=list(pVotes.keys()),weights=[vv ** 0.8 for vv in list(pVotes.values())],k=10))
        pVotes[party] += 1
    pSeats = {k:0 for k in parties}
    numSeats = len(points)
    #print("NUMBER OF SEATS",numSeats)
    for k,v in pVotes.items():
        pSeats[k] = k.guaranteedSeats + round((v/totalVotes) * numSeats)
        #print(k.name,"/ votes:",v, "/ seats:",(v/totalVotes)* numSeats)
        k.guaranteedSeats = 0
    for k,v in pSeats.items():
        #print(k.name,"/ seats:",v)
        if v >= 1:
            for i in range(v):
                try:
                    members.append(k.members[i])
                    k.seat(k.members[i])
                except:
                    nm = Member(parties,k)
                    members.append(nm)
                    k.seat(nm)
    memberSum = sum([len(k.members) for k in pSeats.keys()])
    print(memberSum,"/",numSeats)
    if memberSum > len(points):
        while memberSum > len(points):
            delm = members.pop()
            delm.party.members.pop()
            memberSum = sum([len(k.members) for k in pSeats.keys()])
    inPower = sorted(parties,key=lambda k:len(k.members))[-1]
    if len(inPower.members) > numSeats/2:
        majority = inPower
    else:
        majority = None
    for k in sorted(parties,key=lambda v: len(v.members), reverse=True):
        print(k.name,"|",len(k.members),"seats")
            

def clearParliament():
    for party in parties:
        party.members = []
    members = []
    

ptz = 1

if ptz == 1:
    with open ('polpoints.txt') as file:
        points = file.readlines()

    with open ('polnames.yaml') as STREAM:
        mDict = yaml.safe_load(STREAM)        
    ExistingParties = []
    points = [eval(i) for i in points]

if ptz == 0:
    points = arc(sides=40,radius=6,translation=(6,11))
    points += arc(sides=40,radius = 5,translation=(6,11))
    points += arc(sides=20,radius = 4,rotation=90,translation=(6,11))
    
seats = []
parties = []
members = []
candidates = []
inPower = None
majority = None
cGen = mDict["country"]
countryName = rd.choice(cGen["start"]) + rd.choice(cGen["middle"]) + rd.choice(cGen["end"])

for p in points:
    seats.append(Seat(p[0],p[1]))

for i in range(len(points)+rd.randint(0,1000)):
    candidates.append(Member(parties))

voteForGovernment(parties,points)
while True:
    

    leftWing = [pat for pat in parties if pat.polLean < 3]
    leftWing.sort(key= lambda x: len(x.members),reverse=True)

    center = [pat for pat in parties if pat.polLean >= 3 and pat.polLean <= 7]
    center.sort(key=lambda x: x.polLean)
    
    rightWing = [pat for pat in parties if pat.polLean > 7]
    rightWing.sort(key= lambda x: len(x.members),reverse=False)

    parties = leftWing + center + rightWing
        
    mindex = 0
    for party in parties:
        for i,member in enumerate(party.members):
            seats[mindex].sit(member)
            mindex += 1
        
    colors = [member.party.colour for party in parties for member in party.members]
    labels = [party.name for party in parties for member in party.members]
    area = np.pi*6

    # Plot
    for party in parties:
        if party.members:
            x = [member.seat.x for member in party.members]
            y = [member.seat.y for member in party.members]
            colors = [member.party.colour for member in party.members]
            plt.scatter(x, y, s=area, c=colors, alpha=1,label="[{}] {} ({})".format(party.category, party.name,len(party.members)))
    plt.ylim(-200, 500)
    if majority:
        pType = mDict["parties"][majority.key]["majority"]
    else:
        pType = "Parliament"
    plt.title("{} of {}".format(pType,countryName))
    #plt.title("Plot {}".format(inPower.category))
    plt.xlim(000, 1000)
    plt.axis('off')
    plt.legend()
    #for i,x in enumerate(points):
    #    plt.annotate(members[i].party.name,(x[0],x[1]))

    plt.show()
    clearParliament()
    if input(">") == "q":
        break
    else:
        voteForGovernment(parties,points,fromExisting=True)


