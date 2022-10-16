def solution(n):
    nn = n
    d = [0] * 30
    l = 0
    while (n > 0):
        d[l] = n % 2
        n //= 2
        l += 1
    #for p in range(1, l//2+1):
    for p in range(1, 1 + l):
        ok = True
        for i in range(l - p):
            #print(l, p, i, d[:l], l-i, l-(i+p), d[l-1-i], d[l-1-(i+p)])
            if d[i] != d[(i + p)]:
            #if d[l - 1 - i] != d[l - 1 - (i + p)]:
                #print('break')
                ok = False
                break
        if ok:
            print(nn, l, ''.join(f'{i}' for i in reversed(d[:l])), p)
            return p
    print(nn, l, ''.join(f'{i}' for i in reversed(d[:l])), -1)
    return -1

#for i in range(1000000000):
for i in range(173803):
   (solution(i))

