import matplotlib.pyplot as plt

figure, axes = plt.subplots()
draw_circle = plt.Circle((0, 0), 8, lw=50, fill=False, color=(0.8,0.4,0.4))

axes.set_aspect(1)
axes.add_artist(draw_circle)
plt.title('Circle')
plt.xlim(-10,10)
plt.ylim(-10,10)
plt.show()