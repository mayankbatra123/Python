# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 11:26:36 2019

@author: mayankbatra
"""
import hashlib
import datetime as date
import json

class MB_GENERIC:
    
    def __init__(self,index,timestamp,data,previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash= self.hash_block()
        
    def hash_block(self):
        #sha = hashlib.sha256()
        block_serialized = json.dumps(self, sort_keys=True).encode('utf-8')
        block_hash=hashlib.sha256(block_serialized).hexdigest()
        return block_hash
        

class MB_CREATE_BLOCK(MB_GENERIC):
    
   # MB_GENERIC.__init__(index,timestamp,data,previous_hash)
    
    def create_first_block():
        block = {index:0,'timestamp': date.datetime.now(),'data':'This is block 1','previous_hash':0}
        
    def add_new_block(self,previous):
        new_index=previous.index + 1
        new_data="This is block "+str(new_index)
        new_hash=previous.hash
        block={'index':new_index,'timestamp': date.datetime.now(),'data':new_data,'previous_hash': new_hash }
        
    
start=MB_CREATE_BLOCK()                     ##object created to initialize

blockchain = [start.create_first_block()]       ## blockchain with single block added to list

last=blockchain[0]                          ## seeting value of last blockchain to pass as paaram

for  i in range(1, 10):
    added_block=start.add_new_block(last)
    blockchain.append(added_block)
    last=added_block
    
    print ("Block #",i," created with hash",last.hash)




