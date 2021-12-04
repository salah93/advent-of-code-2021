# part 1
measurments = [int(m) for m in open('inputs.txt')]
initial = measurments[0]
increases = 0
for m in measurments[1:]:
    if m > initial:
        increases +=1
    initial = m
print(increases)


# part 2
initial = measurments[0:3]
increases = 0
for m in measurments[3:]:
    if sum([m] + initial[1:]) > sum(initial):
        increases += 1
    initial = initial[1:] + [m]
print(increases)
