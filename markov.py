import random
from process import *

class Markov:
    def __init__(self, Rank: int = 1):
        self.dataset = []
        self.dic = {}
        self.rank = Rank

    def pushback(self, data: list):
        self.dataset.append(data + ['end'])

    def getTransferMatrix(self):
        # 输入中请不要包含+和start，end
        self.dic = {}
        for data in self.dataset:
            now = "+".join(["start" for i in range(self.rank)])
            for i in data:
                # print(now)
                if(now not in self.dic):
                    self.dic[now] = ([], [])
                if(i not in self.dic[now][0]):
                    self.dic[now][0].append(i)
                    self.dic[now][1].append(0)
                self.dic[now][1][self.dic[now][0].index(i)] += 1
                if(self.rank != 1):
                    # print(now,now.find('+'))
                    now = now[now.find('+')+1:]+'+'+i
                else:
                    now = i

    def showMatrix(self):
        for i in self.dic.keys():
            # print(i[0],'\n',i[1])
            print(i, self.dic[i])

    def getSequense(self):
        now = "+".join(['start' for i in range(self.rank)])
        ret = []
        while True:
            assert now in self.dic, 'Not found {} in dic!'.format(now)
            qwq = random.choices(self.dic[now][0], weights=self.dic[now][1])
            if(qwq[0] == 'end'):
                return ret
            ret += qwq
            if(self.rank != 1):
                now = now[now.find('+')+1:]+'+'+qwq[0]
            else:
                now = qwq[0]


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
