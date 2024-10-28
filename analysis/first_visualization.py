import ezc3d
import pprint
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Load the C3D file
c3d_path = r'D:\GitHub\openbiomechanics\baseball_pitching\data\c3d\000002\000002_003034_73_207_002_FF_809.c3d'
c3d = ezc3d.c3d(c3d_path)

# Get the data points
data_points_xyz = c3d['data']['points']

# Get the labels for the points
labels = c3d['parameters']['POINT']['LABELS']['value']

# Print the labels and descriptions for the analog signals
analog_labels = c3d['parameters']['ANALOG']['LABELS']['value']
analog_ratio = c3d['parameters']['ANALOG']['USED']['value']

print("Analog Signal Labels:")
pprint.pprint(analog_labels)
print(len(analog_labels))

print(c3d['data']['analogs'].shape)

plt.plot(c3d['data']['analogs'][0, 3, :])
plt.show()
""" # Make 3D plot of all the points at time 0
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initial plot
sc = ax.scatter(data_points_xyz[0, :, 0], data_points_xyz[1, :, 0], data_points_xyz[2, :, 0])

# Label the axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set axis limits larger than the limits of the points at time point 1
x_limits = (data_points_xyz[0, :, 1].min() - 0.5, data_points_xyz[0, :, 1].max() + 1.75)
y_limits = (data_points_xyz[1, :, 1].min() - 0, data_points_xyz[1, :, 1].max() + 0)
z_limits = (data_points_xyz[2, :, 1].min() - 0, data_points_xyz[2, :, 1].max() + 0)

ax.set_xlim(x_limits)
ax.set_ylim(y_limits)
ax.set_zlim(z_limits)

# Add a slider for time points
ax_slider = plt.axes([0.25, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Time', 0, data_points_xyz.shape[2] - 1, valinit=0, valstep=1)

# Update function
def update(val):
    time_point = int(slider.val)
    sc._offsets3d = (data_points_xyz[0, :, time_point], data_points_xyz[1, :, time_point], data_points_xyz[2, :, time_point])
    fig.canvas.draw_idle()

# Connect the slider to the update function
slider.on_changed(update)

# Show the plot
plt.show() """