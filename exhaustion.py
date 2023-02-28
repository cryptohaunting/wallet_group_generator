from itertools import combinations, permutations
import numpy as np
from math import comb
import pickle
from tqdm import tqdm
import os

def select_wallet():
    res = []
    for ii_ip_list in ip_combinations:
        for ii in range(wallet_per_ip ** choose):
            temp1 = [0] * len(ii_ip_list)
            temp2 = ii
            jj = 0
            for ii_digital in range(len(ii_ip_list)):
                quotient = temp2 // wallet_per_ip
                remainer = temp2 % wallet_per_ip
                temp2 = quotient
                temp1[jj] = remainer
                jj += 1
            temp1.reverse()
            res.append([f'({i[0]}-{i[1]})' for i in list(zip(ii_ip_list, temp1))])
    return res

def check_Sybil(verified,tobechecked,wallet_group):
    num_common = len(set(verified) & set(tobechecked))
    flag = True
    if num_common >= wallet_group:
        flag = False
    return flag

ip_total = 10 #IP池子的个数
wallet_per_ip = 5 #每个IP池子的钱包数目
choose = 8 #选多少个池子
wallet_group = 4 #判定重复的钱包组合数目
wallet_max = 2  #允许的最大重复数量

ip_combinations = [i for i in combinations(range(ip_total), choose)]

print("正在生成判定前的密码本")
possible_wallets = select_wallet()
possible_wallets = [tuple(i) for i in possible_wallets]
print("判定前的密码本条目",possible_wallets)
print("判定前密码本条目的数量",len(possible_wallets))

print("正在生成判定后的密码本")
flag_list = [True]*len(possible_wallets)
for ii in tqdm(range(len(possible_wallets))):
    if flag_list[ii] == True:
        for jj in range(ii+1,len(possible_wallets)):
                if flag_list[jj] == True:
                    flag1 = check_Sybil(possible_wallets[ii],possible_wallets[jj],wallet_group)
                    # flag1 = True if the pair pass the test
                    # flag1 = False if the par fail the test
                    flag_list[jj] = flag1

print("判定后密码本条目数量",flag_list.count(True)*wallet_max)

verified_wallet = []
for ii in range(len(flag_list)):
    if flag_list[ii]:
        verified_wallet.append(possible_wallets[ii])
print(f"判定后的密码本条目(可重复使用{wallet_max}次)",verified_wallet)

with open("possible_wallets.txt","w") as file1:
    file1.write("判定前的密码本条目"+str(len(possible_wallets))+"\n")
    file1.write(str(possible_wallets))
with open("verified_wallet.txt","w") as file2:
    file2.write(f"判定后的密码本条目(可重复使用{wallet_max}次)"+str(len(verified_wallet))+"\n")
    file2.write(str(verified_wallet))
