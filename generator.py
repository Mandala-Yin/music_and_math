import random
from markov import Markov

def mode_uncoupled(data_pitch, data_note, maxlen = 500, rank = None):
    random.seed(520)

    pitch_markov = Markov() 
    note_markov = Markov() 

    pitch_markov.pushback(data_pitch) #用pushback方法喂数据
    note_markov.pushback(data_note) 
    
    pitch_markov.getTransferMatrix() #喂完数据后用这个方法初始化转移矩阵
    note_markov.getTransferMatrix()
    pitch_markov.showMatrix((0,1)) #支持展示转移矩阵
    
    new_pitch = []
    new_note = []
    
    Len = maxlen
    while(len(new_pitch) < Len): 
        new_pitch += pitch_markov.getSequense(rank_=rank, pre_=new_pitch,alpha=0.2)
    while(len(new_note) < Len):
        new_note += note_markov.getSequense(rank_=rank)
    new_pitch = new_pitch[:Len]
    new_note = new_note[:Len]

    return (new_pitch, new_note)

def mode_full_coupled(data_pitch, data_note, maxlen = 500,  rank = None):
    l = [data_pitch[i] + '_' + data_note[i] for i in range(len(data_pitch))]
    # print(l)
    my_markov = Markov()
    my_markov.pushback(l)
    my_markov.getTransferMatrix()
    # my_markov.showMatrix([0]) 
    new_data = []
    
    Len = maxlen
    while(len(new_data) < Len): 
        new_data = my_markov.getSequense(rank_=rank, pre_ = new_data)
    new_data = new_data[:Len]
    
    new_pitch = [new_data[i][:new_data[i].find('_')] for i in range(Len)]
    new_note = [new_data[i][new_data[i].find('_')+1:] for i in range(Len)]

    return (new_pitch, new_note)
    

def mode_half_coupled(data_pitch, data_note, maxlen = 500, rank = None):

    pitch_markov = Markov() 
    pitch_markov.pushback(data_pitch) 
    
    dic = {}
    for i in range(len(data_pitch)): # 计算内外网连接
        pitch = data_pitch[i]
        note = data_note[i]
        if(pitch not in dic):
            dic[pitch]=([],[])
        if(note not in dic[pitch][0]):
            dic[pitch][0].append(note)
            dic[pitch][1].append(0)
        dic[pitch][1][dic[pitch][0].index(note)]+=1
    # print("**************") # 展示内外网连接。
    # for k in dic.keys():
    #     print(k,dic[k])
    # print("^^^^^^^^^^^^^^\n")
    pitch_markov.getTransferMatrix() 
    # pitch_markov.showMatrix((0,1))
    new_pitch = []
    new_note = []
    Len = maxlen
    while(len(new_pitch) < Len): 
        new_pitch += pitch_markov.getSequense(rank_=rank, pre_=new_pitch,alpha=0.2)
    new_pitch = new_pitch[:Len]
    
    for i in range(Len):
        new_note.append(random.choices(dic[new_pitch[i]][0],weights=dic[new_pitch[i]][1])[0]) # 连接内外网

    return (new_pitch, new_note)


