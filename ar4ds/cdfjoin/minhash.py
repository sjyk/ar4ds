#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Creates a hash table over a relation using the min_hash trick
"""
import binascii
import random

# maximum integer value
MAXINT = 2**32-1

# We need the next largest prime number above MAXINT
NEXTPRIME = 4294967311


def _generate_hash_fns(num=1):

    def kwisehash(st, a=1, k=1):
        val = binascii.crc32(bytes(st.encode("utf-8"))) & 0xffffffff
        return (a * val + k) % NEXTPRIME

    family = []

    for i in range(num):
        a = random.randint(0, MAXINT)
        b = random.randint(0, MAXINT)

        family.append(lambda r, s=a, t=b: kwisehash(r,s,t))

    return family



def _min_hash(attrs, data, hashfn):
    output = {}

    for i, d in enumerate(data):
        
        mh = None

        for a in attrs:

            if a not in d:
                continue

            hv = hashfn(a + str(d[a]))

            if mh == None:
                mh = hv
            else:
                mh = min(mh, hv)

        if mh not in output:
            output[mh] = []

        output[mh].append(i)

    return output


# In[2]:


data = [{"a": 1, "b":0}, {"a": 2, "b":100}, {"a": 1, "b":4}]
data2 = [{"a": 1, "c":0}, {"a": 2, "c":100}, {"a": 1, "c":4}]

hashfn = _generate_hash_fns(1)[0]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




