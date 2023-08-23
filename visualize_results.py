file_path = "/content/results_5_marine.txt"  # Replace with the actual file path
with open(file_path, 'r') as file:
    text = file.read()

data = {}
input_text=text
lines = input_text.strip().split('\n')
for line in lines:
    parts = line.split(',')
    step = int(parts[0].split(':')[1].strip())
    win_percentage = float(parts[1].split(':')[1].strip())
    reward = float(parts[4].split(':')[1].strip())

    data[step] = {'wins': win_percentage, 'reward': reward}

print(data)
sorted_data = dict(sorted(data.items()))

# Print the sorted dictionary
print(sorted_data)
data=sorted_data
import matplotlib.pyplot as plt

# Extract data for plotting
steps = list(data.keys())
wins = [entry['wins'] for entry in data.values()]
rewards = [entry['reward'] for entry in data.values()]
formatted_steps = []
for step in steps:
    if step >= 1000 and step % 1000 == 0:
        formatted_steps.append(f"{int(step/1000)}k")
    else:
        formatted_steps.append(str(step))
steps=formatted_steps
# Create a figure with two y-axes
fig, ax1 = plt.subplots()

# Plot win percentage on the first y-axis (left)
color = 'tab:blue'
ax1.set_xlabel('Steps (in Thousands(K))')
ax1.set_ylabel('Avg. Reward', color=color)
ax1.plot(steps, rewards, color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Create a second y-axis that shares the same x-axis
ax2 = ax1.twinx()

# Plot average reward on the second y-axis (right)
color = 'tab:red'
ax2.set_ylabel('Win Percentage', color=color)
ax2.plot(steps, wins, color=color)
ax2.tick_params(axis='y', labelcolor=color)

n = 10  # Display every 2nd label
plt.xticks(range(0, len(formatted_steps), n), formatted_steps[::n], rotation=45)

# plt.tight_layout()

# Show the plot
plt.title('PySC2 Single-Agent-Movement')
plt.tight_layout()
plt.show()

