from __future__ import division
import os,sys;

def arg_max(T):
    Max_index=0;Max=T[0];
    for i in range(1,len(T)):
        if T[i]>Max:
            Max_index=i;
            Max=T[i];
    return [Max_index,Max];

class Sen_Pair():
    def __init__(self):
        self.german_h=[];
        self.english_h=[];
        self.match=[];
        self.assign={};
        self.P_match=[];

class IBM1():
    def __init__(self):
        self.german_hash={};self.english_hash={};self.All_Pair=[];
        self.P_match=[];
    def ReadData(self,num_line):
        A=open('data/dev-test-train.de-en');
        lines=A.readlines();
        corpus=lines[0:num_line];
        self.german_hash['null']=0;
        for line in corpus:
            line=line[0:len(line)-1];
            pair=Sen_Pair();
            A=line.split('|||');
            t1=A[0].split(' ');
            t2=A[1].split(' ');
            t1.append('null');
            for item in t1:
                if len(item)==0:continue;
                item=item.lower();
                if self.german_hash.has_key(item)is False:
                    self.german_hash[item]=len(self.german_hash);
                pair.german_h.append(self.german_hash[item]);
            for item in t2:
                if len(item)==0:continue;
                item=item.lower();
                if self.english_hash.has_key(item)is False:
                    self.english_hash[item]=len(self.english_hash);
                pair.english_h.append(self.english_hash[item]);
            for i in range(len(pair.english_h)):
                pair.P_match.append([0]*len(pair.german_h));
            self.All_Pair.append(pair)

    def Initial(self):
        for i in range(len(self.german_hash)):
            self.P_match.append([1/len(self.english_hash)]*len(self.english_hash));

    def EM(self):
        for Iter in range(0,100):
            print(Iter)
            P=[];total_ger=[0]*len(self.P_match);
            for i in range(len(self.german_hash)):
                P.append([0]*len(self.english_hash));

            for pair in self.All_Pair:
                s_total=[0]*len(pair.english_h);
                for i in range(len(pair.english_h)):
                    for j in range(len(pair.german_h)):
                        s_total[i]+=self.P_match[pair.german_h[j]][pair.english_h[i]];

                for i in range(len(pair.english_h)):
                    for j in range(len(pair.german_h)): 
                        value=self.P_match[pair.german_h[j]][pair.english_h[i]]/s_total[i];
                        pair.P_match[i][j]=value*self.P_match[pair.german_h[j]][pair.english_h[i]];
                        P[pair.german_h[j]][pair.english_h[i]]+=value;
                        total_ger[pair.german_h[j]]+=value;
                    if Iter==9:
                        assign=arg_max(pair.P_match[i])[0];
                        if pair.assign.has_key(assign)is False:
                            pair.assign[assign]=[];
                        pair.assign[assign].append(i);

            for i in range(0,len(self.german_hash)):
                for j in range(len(self.english_hash)):
                    self.P_match[i][j]=P[i][j]/total_ger[i];
    def Output(self):
        for pair in self.All_Pair:
            for item1 in pair.assign:
                for item2 in pair.assign[item1]:
                    print(str(item1)+'-'+str(item2)+' ');
            print('\n')
IBM=IBM1();
IBM.ReadData(10000);
IBM.Initial()
IBM.EM();
IBM.Output();
