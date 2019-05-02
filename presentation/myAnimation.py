import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import json


filename = "data.json"
with open(filename, 'r') as f:
        data = json.load(f)

fig = plt.figure( figsize=(15,3) )
sns.set_style("darkgrid")

N = len (data)
M = 500
accY = [ data[i]['accY']  for i in range(N)]

ims = []
for i in range(N-M):
    myplot = plt.plot(range(M) ,accY[i:i+M] , color = 'b')
    # plt.xlim = (0,100)
    # plt.ylim = (0,100)
    ims.append(myplot)

im_ani = animation.ArtistAnimation(fig, ims, interval=10 , repeat = False , blit = True)
# im_ani.save('im.mp4')
plt.show()
