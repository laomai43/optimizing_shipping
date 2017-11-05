# -- coding: utf-8 --
f= open('in.txt')
s_temp= 'temp.txt'
temp= open(s_temp, 'w')
temp.writelines(f.readlines()[1:])
f.close()
temp.close()
import numpy
a= numpy.loadtxt(s_temp)
import os
os.remove(s_temp)
b= numpy.arange(len(a))

print b

print a
print len(a)

veryExpensive= 999999;

# for numPackages in range(4,5):
numPackages= 6
minPrice= veryExpensive
resString=''
def work():

    print "numPackages"
    print numPackages

    def dhlPrice(w, t):
        #如果价格超过1000元，那么DHL会收30%税，所以超过1000元不走DHL
        #小于1000元DHL不收税
        assert t<1000
        #空包裹，不算钱
        if w<0.001 and t<0.001:
            return 0
        prices= [203.2, 216, 240, 252.8, 276, 299.2, 323.2, 346.4, 369.6, 393.6, 416.8, 440, 464, 487.2]
        i= int(w)
        #11/30前8折
        return prices[i]*0.8

    def sunnyPrice(w, t):
        #税费是包裹商品总价的11.9%
        #空包裹，不算钱
        if w<0.001 and t<0.001:
            return 0
        total=t*0.119
        prices= [45.5, 76.5, 108.8, 139.4, 171.7, 203.15, 235.45, 266.9, 298.35, 314.5, 330.65, 346.8, 362.95, 379.1]
        i= int(w)
        #11/30前85折
        total+= prices[i]*0.85
        return total


    def calTotal(b, l):
        w= numpy.zeros(numPackages)
        t= numpy.zeros(numPackages)
        p= numpy.zeros(numPackages)
        for i in range(min(l,len(b))):
            v= b[i]
            w[v]+= a[i][0]
            t[v]+= a[i][2]

            #单个包裹总价大于2000元的方案，去掉。
            if t[v]>2000:
                return veryExpensive
        if l!=len(b):
            return -1
        total=0
        for i in range(numPackages):
            sp= sunnyPrice(w[i], t[i])
            #总价大于1000元的包裹，直接走阳光清关。
            if t[i]>=1000:
                total+= sp
            else:
                #总价小于1000元的包裹，比较DHL和阳光清关哪个更便宜
                dp= dhlPrice(w[i], t[i])
                if (sp<dp):
                    total+= sp
                else:
                    total+= dp
                    p[i]= 1

        global minPrice
        global resString
        if minPrice>total:
            minPrice= total
            resString= "{} {} {} {} {}".format(b, w, t, p, total)
        print b,w,t,p,total
        return total




    def dfs(k):
        r= calTotal(b, k)
        if r==veryExpensive:
            return
        if k>len(a)-1:
            return
        for i in range(numPackages):
            b[k]= i
            dfs(k+1)
    pass

    b[0]=0
    b[1]=1
    b[2]=2
    dfs(3)
    print "best solution:"
    print resString, minPrice
work()
