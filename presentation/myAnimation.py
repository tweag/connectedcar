import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import json
import matplotlib


filename = "data.json.1"
with open(filename, 'r') as f:
        data = json.load(f)

fig = plt.figure( figsize=(20,10) )
# sns.set_style("darkgrid")
fig.patch.set_facecolor('black')
plt.style.use('dark_background')
matplotlib.rc('axes',edgecolor='black')
plt.yticks([])
plt.xticks(range(5))
plt.tight_layout()

N = len (data)
M = 500
accX = [ data[i]['accX']  for i in range(N)]
accY = [ data[i]['accY'] - 40  for i in range(N)]
accZ = [ data[i]['accZ'] - 80  for i in range(N)]



ims = []
for i in range(N-M):
    myplot = plt.plot(range(M) , accX[i:i+M], range(M) , accY[i:i+M]  , range(M) , accZ[i:i+M]  , color = 'xkcd:mint green')
    # plt.xlim = (0,100)
    # plt.ylim = (-20,20)
    ims.append(myplot)

im_ani = animation.ArtistAnimation(fig, ims, interval=10 , repeat = False , blit = True)
# im_ani.save('im.mp4')
plt.show()
