from fastapi import FastAPI
import random

app = FastAPI()

memorylines = 2**10
l1cachelines = 128
l1victimcachelines = 4
l2cachelines = 256

adr = []
last = 0

memory = [[random.randint(1, 9)] * 64 for _ in range(memorylines)]

l1 = [[0] * 64 for _ in range(l1cachelines)]
l2 = [[0] * 64 for _ in range(l2cachelines)]
victimcache = [[0] * 64 for _ in range(l1victimcachelines)]


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
    address = int(address, 2)
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
    return int(address, 2) in adr


def l1check(address):
    line = int(address, 2) >> 6
    data = memory[line]
    return l1[line % 128] == data


def processor():
    address = random.randint(0, 65535)
    return bin(address)


def convert_to_binary_list(cache):
    binary_list = []
    for line in cache:
        binary_data = "".join(str(bit) for bit in line)
        binary_list.append(binary_data)
    return binary_list


@app.get("/")
async def get_cache_states():
    l1_cache_list = convert_to_binary_list(l1)
    victim_cache_list = convert_to_binary_list(victimcache)
    l2_cache_list = convert_to_binary_list(l2)
    return {
        "L1_cache": l1_cache_list,
        "L2_cache": l2_cache_list,
        "Victim_cache": victim_cache_list,
    }


@app.post("/")
async def simulate_one_iteration():
    addr = processor()
    result = {"address": addr}

    l1cachehit = l1check(addr)
    result["L1_cache_hit"] = str(l1cachehit)

    if not l1cachehit:
        l1write(addr)
        vcachehit = victimcachecheck(addr)
        result["Victim_cache_hit"] = str(vcachehit)

        if not vcachehit:
            victimcachewrite(addr)
            l2cachehit = l2check(addr)
            result["L2_cache_hit"] = str(l2cachehit)

            if not l2cachehit:
                l2write(addr)

    l1_cache_list = convert_to_binary_list(l1)
    victim_cache_list = convert_to_binary_list(victimcache)
    l2_cache_list = convert_to_binary_list(l2)

    result["L1_cache"] = l1_cache_list
    result["Victim_cache"] = victim_cache_list
    result["L2_cache"] = l2_cache_list

    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
