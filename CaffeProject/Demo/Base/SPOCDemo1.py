import pickle

f = open("E:\\sun2\\工作\\lab\\computer vision\\CNN\\Spoc-master\\pcaFlickr.dat", 'rb')
(avg, sing, pcamat) = pickle.load(f)

print(f)