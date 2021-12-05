## part 1
#forward = 0
#down = 0
#for line in open('data/depth.txt'):
#    command, value = line.split()
#    if command == 'forward':
#        forward += int(value)
#    elif command == 'down':
#        down += int(value)
#    else:
#        down -= int(value)
#print(f'forward = {forward}')
#print(f'down = {down}')
#print(f'product = {forward * down}')
#
# part 2
forward = 0
depth = 0
aim = 0
for line in open('data/depth.txt'):
    command, value = line.split()
    if command == 'forward':
        forward += int(value)
        depth += (aim * int(value))
    elif command == 'down':
        aim += int(value)
    elif command == 'up':
        aim -= int(value)
print(f'aim = {aim}')
print(f'depth = {depth}')
print(f'forward = {forward}')
print(f'product = {forward * depth}')
