import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Create a figure
fig = plt.figure(figsize=(8, 6))
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1])

# First plot (smaller)
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_title("Plot 1")
ax1.plot([1, 2, 3], [1, 4, 9])

# Second plot (smaller)
ax2 = fig.add_subplot(gs[1, 0])
ax2.set_title("Plot 2")
ax2.plot([1, 2, 3], [1, 2, 3])

# Third plot (double the size, spanning two columns)
ax3 = fig.add_subplot(gs[:, 1])
ax3.set_title("Occupancy")
integer_value = 5
ax3.text(0.5, 0.5, str(integer_value), fontsize=200, ha="center", va="center")
ax3.axis("off")

# Adjust layout
plt.tight_layout()
plt.show()
