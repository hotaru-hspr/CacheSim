from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import random
from collections import defaultdict

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Define the Line Size
lineSize = 32

# Define the Main Memory
mainMemoryLines = 2**10
mainMemory = [[random.choice([i for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"]) for _ in range(lineSize)] for _ in range(mainMemoryLines)]

# Define the L1 Cache
l1CacheLines = 128
l1Cache = [[0] * lineSize for _ in range(l1CacheLines)]

# Define the L2 Cache
l2CacheLines = 256
l2Cache = [[0] * lineSize for _ in range(l2CacheLines)]

# Define the victim cache
l1VictimLines = 4
victimAddress = []
victimCacheCount = 0
victimCacheCounter = defaultdict(int)
victimcache = [[0] * lineSize for _ in range(l1VictimLines)]

# Get the ByteOffset for L1 and L2 Cache
def ByteOffset(addr):
    return int(addr[-6:], 2)

# Get the SetNo for L1 and L2 Cache
def SetNo(addr):
    return int(addr[0:6], 2)

# Write to L1 cache
def l1Write(addr):
    line = int(addr, 2) >> 6
    data = mainMemory[line]
    evicted_line = l1Cache[line % 128]
    l1Cache[line % L1CacheLines] = data
    if evicted_line != [0] * lineSize:
        victimCacheWrite(addr)

# Read from L1 cache
def l1Read(addr):
    line = int(addr, 2) >> 6
    return l1Cache[line % 128][int(ByteOffset(addr))]

# Check if line is present in L2 cache
def l2Check(addr):
    line = SetNo(addr) * 4
    data = mainMemory[int(addr, 2) >> 6]
    for i in range(4):
        if l2Cache[line + i] == data:
            return True
    return False

# Read from L2 cache
def l2Read(addr):
    line = SetNo(addr) * 4
    for i in range(4):
        if l2Cache[line + i] == mainMemory[int(addr, 2) >> 6]:
            return l2Cache[line + i][ByteOffset(addr)]

# Write to L2 cache
def l2Write(addr):
    line = SetNo(addr) * 4
    data = mainMemory[int(addr, 2) >> 6]
    changed = 0
    for i in range(4):
        if l2Cache[line + i] != [0] * 64:
            l2Cache[line + i] = data
            changed = 1
    if not changed:
        l2Cache.pop(line)
        l2Cache.insert(line + 3, data)

# Read from victim cache
def victimCacheRead(addr):
    addr = int(addr, 2)
    victimCacheCounter[addr] += 1
    if addr in victimAddress:
        victimAddress.remove(addr)
        victimAddress.append(addr)
        victimCacheCounter[addr] += 1
        return victimcache[victimAddress.index(addr)][ByteOffset(addr)]
    return None

# Write to victim cache
def victimCacheWrite(addr):
    line = int(addr, 2) >> 6
    global victimCacheCount
    addr = int(addr, 2)

    if addr in victimAddress:
        victimAddress.remove(addr)
        victimAddress.append(addr)
    else:
        if len(victimAddress) < l1VictimLines:
            victimAddress.append(addr)
        else:
            victimAddress.pop(0)
            victimAddress.append(addr)

    victimcache[victimAddress.index(addr)] = mainMemory[line]

# Check if line is present in victim cache
def victimcachecheck(addr):
    return int(addr, 2) in victimAddress

# Check if line is present in L1 cache
def l1check(addr):
    line = int(addr, 2) >> 6
    data = mainMemory[line]
    return l1Cache[line % 128] == data

# Generate a random address from the processor
def processor():
    address = random.randint(0, 65535)
    return bin(address)

# Convert cache to base64 list
def convertToBinaryList(cache):
    base64List = []
    for line in cache:
        binaryData = "".join(str(bit) for bit in line)
        base64List.append(binaryData)
    return base64List


@app.get("/")
async def getCacheStates():
    l1CacheList = convertToBinaryList(l1Cache)
    victimCacheList = convertToBinaryList(victimcache)
    l2CacheList = convertToBinaryList(l2Cache)

    return {
        "L1_cache": l1CacheList,
        "L2_cache": l2CacheList,
        "Victim_cache": victimCacheList,
    }


@app.post("/")
async def simulateOneIteration():
    addr = processor()
    result = {"address": addr}

    l1cachehit = l1check(addr)

    if l1cachehit:
        result["L1_cache_hit"] = "Hit"
    else:
        result["L1_cache_hit"] = "Miss"

        vcachehit = victimcachecheck(addr)
        if vcachehit:
            result["Victim_cache_hit"] = "Hit"
        else:
            result["Victim_cache_hit"] = "Miss"

            l2cachehit = l2Check(addr)

            if l2cachehit:
                result["L2_cache_hit"] = "Hit"
            else:
                result["L2_cache_hit"] = "Miss"
                l2Write(addr)

        l1Write(addr)

    l1_cache_list = convertToBinaryList(l1Cache)
    victim_cache_list = convertToBinaryList(victimcache)
    l2_cache_list = convertToBinaryList(l2Cache)

    result["L1_cache"] = l1_cache_list
    result["Victim_cache"] = victim_cache_list
    result["L2_cache"] = l2_cache_list

    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
