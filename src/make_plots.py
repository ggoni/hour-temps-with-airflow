import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data_folder = './data/'
images_folder = './images/'

# Read the temperature measurements data
data = pd.read_csv(data_folder + 'mediciones.csv')

# Create a strip plot
ax = sns.stripplot(data=data, x='lugar', y='temp_celsius',
                   hue='lugar', jitter=True, alpha=0.3)

# Set seaborn style
sns.set_theme(style='darkgrid')

# Set plot title, x-label, and y-label
plt.title("Hourly temperature measurements by location")
ax.set_xlabel("Place (Comuna)")
ax.set_ylabel("Temperature (ºC)")

# Calculate mean, standard deviation, 25th and 75th percentiles for each location
means = data.groupby('lugar')['temp_celsius'].mean()
stds = data.groupby('lugar')['temp_celsius'].std()
p25 = data.groupby('lugar')['temp_celsius'].quantile(0.25)
p75 = data.groupby('lugar')['temp_celsius'].quantile(0.75)

# Add text annotations for mean, standard deviation, and percentiles
for i, lugar in enumerate(data['lugar'].unique()):
    mean = means[lugar]
    std = stds[lugar]
    ax.text(i, mean, f"Mean: {mean:.2f}", ha='left', va='bottom')
    ax.text(i, mean + std, f"Std: {std:.2f}", ha='right', va='bottom')

    # Add markers for 25th and 75th percentiles
    # ax.plot(i, p25[lugar], marker='o', markersize=5, color='red')
    # ax.plot(i, p75[lugar], marker='o', markersize=5, color='blue')

# Save the plot as an image file
plt.savefig(images_folder + 'stripplot.png')
