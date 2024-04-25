from fastapi import FastAPI, HTTPException
from typing import List
import random

app = FastAPI()

memorylines = 2**10
l1cachelines = 128
l1victimcachelines = 4
l2cachelines = 256

adr = []
last = 0

memory = [[random.randint(1, 9)] * 64 for _ in range(memorylines)]

l1 = [[0] * 64] * l1cachelines
l2 = [[0] * 64] * l2cachelines
victimcache = [[0] * 64] * l1victimcachelines


def l2byteoffset(address):
    return int(address[-6:], 2)


def setno(address):
    return int(address[0:6], 2)


def l1byteoffset(address):
    return int(address[-6:], 2)


def l1write(address):
    line = int(address, 2) >> 6
    l1[line % 128] = memory[line]


def l1read(address):
    line = int(address, 2) >> 6
    return l1[line % 128][int(l1byteoffset(address))]


def l2check(address):
    line = setno(address) * 4
    data = memory[int(address, 2) >> 6]
    for i in range(4):
        if l2[line + i] == data:
            return True
    return False


def l2read(address):
    line = setno(address) * 4
    for i in range(4):
        if l2[line + i] == memory[int(address, 2) >> 6]:
            return l2[line + i][l2byteoffset(address)]


def l2write(address):
    line = setno(address) * 4
    data = memory[int(address, 2) >> 6]
    changed = False
    for i in range(4):
        if l2[line + i] != [0] * 64:
            l2[line + i] = data
            changed = True
    if not changed:
        l2.pop(line)
        l2.insert(line + 3, data)


def victimcacheread(address):
    address = int(address)
    return victimcache[adr.index(address)][l1byteoffset(address)]


def victimcachewrite(address):
    line = int(address, 2) >> 6
    global last
    address = int(address, 2)
    if last < 4:
        last += 1
        adr.append(address)
        victimcache[adr.index(address)] = memory[line]
    else:
        adr.pop(0)
        victimcache.pop(0)
        adr.append(address)
        victimcache.append(memory[line])


def victimcachecheck(address):
    if int(address, 2) in adr:
        return True
    else:
        return False


def l1check(address):
    line = int(address, 2) >> 6
    data = memory[line]
    if l1[line % 128] == data:
        return True
    else:
        return False


def processor():
    address = random.randint(0, 65535)
    return bin(address)


@app.get("/")
async def get_cache_states():
    return {"L1": l1, "Victim Cache": victimcache, "L2": l2}


@app.post("/")
async def simulate_cache_access():
    addr = processor()
    line = int(addr, 2) >> 6
    response = {"address": addr}
    l1cachehit = l1check(addr)
    if l1cachehit:
        response["l1_cache_hit"] = True
        response["data"] = l1read(addr)
    else:
        response["l1_cache_hit"] = False
        l1write(addr)
        vcachehit = victimcachecheck(addr)
        if vcachehit:
            response["victim_cache_hit"] = True
            response["data"] = victimcacheread(addr)
        else:
            response["victim_cache_hit"] = False
            victimcachewrite(addr)
            l2cachehit = l2check(addr)
            if l2cachehit:
                response["l2_cache_hit"] = True
                response["data"] = l2read(addr)
            else:
                response["l2_cache_hit"] = False
                l2write(addr)
    return response
