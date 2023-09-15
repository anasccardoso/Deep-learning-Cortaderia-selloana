import sys
import pickle
from photos import photo_instance
pk1_path = sys.argv[1]
with open(pk1_path,'rb') as inp:
    data = pickle.load(inp)

photos = [photo_instance(x) for x in data]

photos_ids = [x.id for x in photos]

a = set(photos_ids)
print(len(a))
