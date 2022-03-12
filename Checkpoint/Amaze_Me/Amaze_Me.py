import socket, time, statistics, math

PRINT_INTERVAL = 15  # Determines the print interval of the current position.


# Send the given command to the server and updates current position if a move command was given.
# Arguments: command(a char) to send, and cooldown(boolean) to determine whether to skip second respond from server.
def send_command(command, cooldown=True):
    # Update location if the command is to move
    global current_position
    if command == 'l':
        current_position[0] -= 1
    elif command == 'r':
        current_position[0] += 1
    elif command == 'u':
        current_position[1] += 1
    elif command == 'd':
        current_position[1] -= 1

    command_bytes = str.encode(command)
    s.sendall(command_bytes)
    reply = (s.recv(256)).decode()

    # "cooldown" to avoid "what is your command?" in buffer.
    if cooldown:
        s.recv(256)
    return reply


# Gets 2 tuples of circles(x, y, r^2) and returns their 2 points of intersections.
def get_intersections(circle1, circle2):
    x0, y0, r0 = circle1[0], circle1[1], circle1[2]
    x1, y1, r1 = circle2[0], circle2[1], circle2[2]
    d = math.sqrt((x1-x0)**2 + (y1-y0)**2)
    a = (r0-r1+d**2)/(2*d)
    h = math.sqrt(r0-a**2)
    x2 = x0+a*(x1-x0)/d
    y2 = y0+a*(y1-y0)/d

    x3 = round(x2+h*(y1-y0)/d)
    y3 = round(y2-h*(x1-x0)/d)
    x4 = round(x2-h*(y1-y0)/d)
    y4 = round(y2+h*(x1-x0)/d)
    return (x3, y3), (x4, y4)


# Sends 'g' command (which checks for treasure), only if the current position hasn't been probed yet.
# Once the method finds 3 circles, it also finds the treasure and sends it to the server to get the flag.
def check_for_treasure():
    if current_position not in probed:
        reply = send_command('g')  # Checks for treasure
        probed.append(current_position.copy())
        if "far far away\n" != reply:
            curr_x = int(current_position[0])
            curr_y = int(current_position[1])
            global circles
            start_index = reply.find('√') + 1  # Square root index, to find the distance.
            distance = int(reply[start_index:])
            print(f"Found a circle at {curr_x},{curr_y}, only square root({distance}) tiles away from treasure!")
            circles.append((curr_x, curr_y, distance))

            if len(circles) >= 3:
                all_intersections = []
                for i in range(len(circles)):
                    for j in range(i+1, len(circles)):
                        all_intersections.extend(get_intersections(circles[i], circles[j]))
                try:
                    answer = statistics.mode(all_intersections)
                    print("{0} circles were used to find the treasure location: {1} ".format(len(circles), str(answer)))
                    send_command('s', False)  # Solution command sending
                    answer = str(answer[0]) + "," + str(answer[1])
                    flag = send_command(answer, False)  # Answer sending
                    print("\n\n" + str(flag))
                    exit(0)
                except statistics.StatisticsError:
                    print("Couldn't find the treasure using {0} circles, trying to find more circles".format(len(circles)))


# Sends 'i' command to server to update available moves.
def check_available_moves():
    # format returned from server: "l = 0, r = 1, u = 0, d = 1"
    reply = send_command('i')
    allowed_directions["left"] = int(reply[2])
    allowed_directions["right"] = int(reply[7])
    allowed_directions["up"] = int(reply[12])
    allowed_directions["down"] = int(reply[17])

    # Optional:
    # for char in 'lrud, =':  # Changes the format from "l = 0, r = 1, u = 0, d = 1" to "0101" for easier indexing(0-3)
    #     reply = reply.replace(char, '')


# Updates the location using the start message sent when connecting to the server.
def update_location(message):
    start_index = message.index("(") + 1
    end_index = message.index(")")
    x, y = message[start_index:end_index].split(",")
    current_position[0] = int(x)
    current_position[1] = int(y)


# This method sends automatically move command according to "wall follower" algorithm with "left hand rule".
def auto_move():
    global heading
    for i in range(-1, 3):
        abs_direction = (heading + 90 * i) % 360  # Starts with (relative) left by multipling -1(thus substracts by 90)
        next_move = directions[abs_direction]
        if allowed_directions[next_move]:
            heading = abs_direction
            send_command(next_move[0])
            break


directions = {
    0: "up",
    90: "right",
    180: "down",
    270: "left"
}
allowed_directions = dict(left=0, right=0, up=0, down=0)
current_position = [0, 0]
heading = 0
circles = []  # Circle = a known point with a known distance to flag.

print("Connecting to checkpoint's server...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("maze.csa-challenge.com", 80))
probed = []
try:
    time.sleep(6)  # Waiting for the server to finish sending the instructions...
    start_message = s.recv(4096).decode()
    print("Connected and ready! Starting to search for the treasure :D")
    update_location(start_message)
    print("Current position: ", current_position)

    iterations_counter = 1
    while 1:
        auto_move()
        check_available_moves()
        check_for_treasure()

        if iterations_counter % PRINT_INTERVAL == 0:
            print("Current position: ", current_position)
        iterations_counter += 1

finally:
    s.close()
