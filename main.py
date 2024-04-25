import random

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
    print(address)
    print(address[-12:-6], 2)
    return int(address[0:6], 2)


def l1byteoffset(address):
    return int(address[-6:], 2)


def l1write(address):
    line = int(address, 2) >> 6
    l1[line % 128] = memory[line]


def l1read(address):
    line = int(addr, 2) >> 6
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
    changed = 0
    for i in range(4):
        if l2[line + i] != [0] * 64:
            l2[line + i] = data
            changed = 1
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


a = input("HIT ENTER TO START......")
while True:
    addr = processor()
    line = int(addr, 2) >> 6
    print("ADDRESS ISSUED BY PROCESSOR:", addr, end=" ")
    l1cachehit = l1check(addr)
    if l1cachehit:
        print("L1 CACHE HIT", end=" ")
        data = l1read(addr)
        print("DATA:", data, end=" ")

    else:
        print("L1 CACHE MISS", end=" ")
        # l1write(addr,memory[line])
        l1write(addr)
        vcachehit = victimcachecheck(addr)
        if vcachehit:
            print("VICTIM CACHE HIT", end=" ")
            data = victimcacheread(addr)
            print("DATA:", data, end=" ")

        else:
            print("VICTIM CACHE MISS", end=" ")
            victimcachewrite(addr)
            print(addr)
            l2cachehit = l2check(addr)
            if l2cachehit:
                print("L2 CACHE HIT", end=" ")
                data = l2read(addr)
                print("DATA:", data, end=" ")
            else:
                print("L2 CACHE MISS")
                l2write(addr)
    print()
    print()

    for i in range(256):
        for j in range(64):
            if i < 128:
                print(l1[i][j], end="")
            else:
                print(" ", end="")
        print(end=" ")
        for j in range(64):
            if i < 4:
                print(victimcache[i][j], end="")
            else:
                print(" ", end="")

        print(end=" ")
        for j in range(64):
            print(l2[i][j], end="")
        print()

    input()
