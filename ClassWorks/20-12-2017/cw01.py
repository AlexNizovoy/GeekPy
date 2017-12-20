import pickle


data1 = {'a': [1, 2, 3.2, 4+6j],
    'b': ('string', "another string"),
    'c': None
    }

selfref_list = [1, 2, 3]
selfref_list.append(selfref_list)

outp = open('data.pkl', 'wb')

pickle.dump(data1, outp)
outp.close()
