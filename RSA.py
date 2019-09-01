import random
#import gmpy2
#from gmpy import f_mod
from math import floor

#Taqrim Sayed

#works
#Psuedocode from text book for miller rabbins
#p is the prime and s is the accuracy of the test
def MRT(p, s):
    #checks for 0-4
    if (p == 2 or p == 3 or p==0 or p==1):
        return "N/A"
    #lightens load
    if (p%2 == 0 or p%3 == 0):
        return "comp"
    u=0
    r = p-1
    #creates p-1 = (2**u)*r
    while r %2==0:
        u +=1
        r //= 2
    for i in range(1, s):
        a = random.randint(2, p-2)
        #z = f_mod(a**r, p)
        z = (a**r) % p
        if z != 1 and z != p-1:
            for j in range(0, u-1):
                #z = f_mod(z**2, p)
                z = z**2 % p
                if z == 1:
                    #p is composite
                    return "comp"
            if z != p-1:
                # p is composite
                return "comp"
    #p is prime
    return "prime"


#works
#checks for inverse using Euclidean algo
def EA(num1, num2):
    c=2
    if(num1>num2):
        a = num1
        b = num2
    elif(num2>num1):
        a = num2
        b = num1
    while c!=1 and c!=0:
        #c = f_mod(a,b)
        c = a%b
        a = b
        b = c
    if b == 1:
        return True
    elif b == 0:
        return False


#works
def genPQ(keySize, accuracy):
    p=random.getrandbits(keySize)
    q=random.getrandbits(keySize)
    satisfied = False
    while(not satisfied):
        if(MRT(q, accuracy) != "prime"):
            q = random.getrandbits(keySize)
        elif(MRT(p, accuracy)!="prime"):
            p = random.getrandbits(keySize)
        else:
            satisfied = True

    if p == q:
        return genPQ(keySize, accuracy)
    else:
        return [p , q]

##Extended Euclidean Finds inverse
def EEA(x, y):
    a = 0
    b = 1
    mod  = y
    while x != 0:
        temp = x
        q = y // x
        x = y % x
        y = temp
        temp = a
        a = b
        b = temp - q * b
    return a

#calculates phi
def phi(p,q):
    return ((p-1)*(q-1))


#x is plain/cipher, y is exp, n is modular
def powmod_sm(x, y, n):
    exp = bin(y)
    value = x
    for i in range(3, len(exp)):
        #value = f_mod(value*value, n)
        value = (value*value)%n
        if(exp[i:i+1] == '1'):
            #FMOD here value = f_mod(value*x, n)
            value = (value*x)%n
    return value

#primes to use for now [26021, 16693] -> 15bits 1000 accuracy
#print(EuclideanAlgo(26021,16693))

def RSAEnc(pubKey, plain, mod):
    #return (plain**pubKey)%mod
    return plain**powmod_sm(plain, pubKey, mod)%mod

def RSADec(privKey, cipher, mod):
    #return (cipher ** privKey) % mod
    return cipher**powmod_sm(cipher, privKey, mod)%mod

def main():
    keySize = int(input("How many bits should p and q be? "))
    accuracy = int(input("How accurate do you want it to test for primes? "))
    primes = genPQ(keySize, accuracy)
    p = primes[0]
    q = primes[1]
    n = p * q
    phi = (p - 1) * (q - 1)
    print("The two primes are {} and {} so n is {} and phi is {}".format(p, q, n, phi))
    plainText = int(input("Input plaintext:"))



    privKey = 1
    while(not EA(privKey, phi)):
        privKey = int(input("Please pick a new private key: "))
        pubKey = EEA(privKey, phi)
        if((pubKey*privKey)%phi != 1):
            privKey = 1

    print("Public Key: {}".format(pubKey))
    cipherText = RSAEnc(plainText, pubKey,  n)
    decryptedCipher = RSADec(cipherText, privKey,  n)
    print("CipherText: {} \nPlainText: {}".format(cipherText, decryptedCipher))

main()

#Generate keys with random.getrandbits(keySize) and check with MillerRabinTest(p, s)
#Determine private key with EuclideanAlgo(num1, num2)
