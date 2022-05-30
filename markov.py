import random
from process import *


class Markov:
    def __init__(self):
        self.dataset = []
        self.dics = []
        self.maxRank=100  #只计算前100阶马尔可夫
    def pushback(self,data:list):
        self.dataset.append(data+['end'])
    def getTransferMatrix(self):
        #输入中请不要包含+和start，end
        for rank in range(self.maxRank+1): 
            dic = {}
            for data in self.dataset:
                now = "+".join(["start" for i in range(rank)])
                for i in data:
                    # print(now)
                    if(now not in dic):
                        dic[now]=([],[])
                    if(i not in dic[now][0]):
                        dic[now][0].append(i)
                        dic[now][1].append(0)
                    dic[now][1][dic[now][0].index(i)]+=1
                    if(rank==0):
                        now = ''
                    elif(rank==1):
                        now = i                       
                    else:
                        now = now[now.find('+')+1:]+'+'+i
            self.dics.append(dic)
                
    def showMatrix(self,ranklist=range(2)):
        for rank in ranklist:
            print(f"*********Rank {rank}***********")
            for i in self.dics[rank].keys():
                # print(i[0],'\n',i[1])
                print(i,self.dics[rank][i])
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^\n");
            
            
    def getSequense(self,rank_=None,pre_=None,alpha=0.5):
        p=1
        seq = []
        for i in range(self.maxRank+1):
            seq.append(p*alpha)
            p = p*(1-alpha)
        pre = ['start'] * self.maxRank
        ret = []
        fail_cnt = 0
        if pre_ is not None:
            pre += pre_
        # print(pre) 
        while True:
            if(rank_ is not None):
                rank = rank_
            else :
                rank = random.choices(range(1,self.maxRank+1),weights=seq[1:])[0]
            if(rank==0):
                now = ''
            elif(rank==1):
                now = pre[-1]                       
            else:
                now = '+'.join(pre[-rank:])
            # print(rank,now) #取消注释这一行可以观察选择的阶数，理解alpha的效果。
            if(now in self.dics[rank]):
                qwq = random.choices(self.dics[rank][now][0],weights=self.dics[rank][now][1])
                if(qwq[0] == 'end'): return ret
                ret += qwq
                pre += qwq
            else:
                fail_cnt+=1
                if(fail_cnt>1000):
                    print("Warning: Failed many times.")
                    return ret
                     


if __name__ == '__main__':
    random.seed(520)

    pitch_markov = Markov(3)  # 这里传矩阵阶数
    note_markov = Markov(3)

    # configs
    input_path = './input.txt'
    output_txt_path = './out.txt'
    output_mid_path = './out.mid'

    # example
    with open(input_path) as f:
        data_pitch = f.readline().split()
        pitch_markov.pushback(data_pitch)  # 用 pushback 方法喂数据
        data_note = f.readline().split()
        note_markov.pushback(data_note)

        pitch_markov.getTransferMatrix()  # 喂完数据后用这个方法初始化转移矩阵
        note_markov.getTransferMatrix()
        # pitch_markov.showMatrix() # 支持展示转移矩阵

        new_pitch = []
        new_note = []

        Len = 500
        while(len(new_pitch) < Len):  # 暴力拼接，不太妙
            new_pitch += pitch_markov.getSequense()
        while(len(new_note) < Len):
            new_note += note_markov.getSequense()
        new_pitch = new_pitch[:Len]
        new_note = new_note[:Len]
        out = open(output_txt_path, 'w')
        out.write(' '.join(new_pitch)+'\n')
        out.write(' '.join(new_note)+'\n')
        out.close()
        array_to_midi(output_txt_path, output_mid_path, format='name', bpm=80)
        print('Done.')
