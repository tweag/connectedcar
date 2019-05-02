import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

# def update_line(num, data, line):
#     line.set_data(data[..., :num])
#     return line,
# fig1 = plt.figure()
#
# # Fixing random state for reproducibility
# np.random.seed(19680801)
#
# data = np.random.rand(2, 25)
# l, = plt.plot([], [], 'r-')
# plt.xlim(0, 1)''
# plt.ylim(0, 1)
# plt.xlabel('x')
# plt.title('test')
# line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
#                                    interval=50, blit=True)
#
# line_ani.save('lines.mp4')

fig = plt.figure( figsize=(15,3) )

N = 5000
M = 500
x = np.zeros(N)

x[0] = 0
for i in range(N-1) :
    x[i+1] = x[i] + 0.01*(2*np.random.rand() - 1)

sns.set_style("darkgrid")

ims = []
for i in range(N-M):
    myplot = plt.plot(range(M) ,x[i:i+M] , color = 'b')
    # plt.xlim = (0,100)
    # plt.ylim = (0,100)
    ims.append(myplot)

im_ani = animation.ArtistAnimation(fig, ims, interval=10 , repeat = False , blit = True)
im_ani.save('im.mp4')
# plt.show()
