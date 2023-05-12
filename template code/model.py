import pulp

# Define the activities and time slots
activities = ['A', 'B', 'C', 'D']
time_slots = ['T1', 'T2', 'T3', 'T4', 'T5']

# Define the duration and resource requirement for each activity
duration = {'A': 2, 'B': 3, 'C': 1, 'D': 2}
resource = {'A': 1, 'B': 2, 'C': 1, 'D': 1}

# Create a linear programming problem
prob = pulp.LpProblem('Scheduling', pulp.LpMinimize)

# Define the start time and completion time variables for each activity
start_time = pulp.LpVariable.dicts('Start', activities, lowBound=0, cat='Integer')
end_time = pulp.LpVariable.dicts('End', activities, lowBound=0, cat='Integer')

# Define the objective function to minimize the total time
prob += pulp.lpSum([end_time[i] for i in activities])

# Define the time constraints
for i in activities:
    for j in activities:
        if i != j:
            prob += end_time[i] <= start_time[j]
            prob += start_time[i] >= end_time[j] - duration[j]

# Define the resource constraints
for t in time_slots:
    prob += pulp.lpSum([resource[i] * (start_time[i] <= t) * (end_time[i] > t)
                        for i in activities]) <= 2

# Solve the problem
prob.solve()

# Print the solution
print('Total time:', pulp.value(prob.objective))
for i in activities:
    print('Activity', i, ': Start time =', pulp.value(start_time[i]), ', End time =',
          pulp.value(end_time[i]))
