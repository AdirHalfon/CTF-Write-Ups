import socket, time


# This function returns the missing letters among the 2 words it gets as parameters.
def find_missing_letters(word1, word2):
    letters_in_pair = set(word1 + word2)
    return [letter for letter in 'abcdefghijklmnopqrstuvwxyz' if letter not in letters_in_pair]

    ####################################################
    # Another way to do it, without list comprehension #
    ####################################################
    # letters_in_pair = set(word1 + word2)             #
    # unique = []                                      #
    # for letter in "abcdefghijklmnopqrstuvwxyz":      #
    #     if letter not in letters_in_pair:            #
    #         unique.append(letter)                    #
    # return unique                                    #
    ####################################################


# This function gets a list of 2 words whose letters are unique - there is not a single common letter among them.
# These words are being sent to the server
def send_sample(pair) -> None:
    first_grade = int(send_message(pair[0]))
    second_grade = int(send_message(pair[1]))

    total_grade = first_grade + second_grade
    missing_letters = find_missing_letters(pair[0], pair[1])
    if total_grade == 12:
        black_list.extend(missing_letters)
    elif total_grade == 10:
        white_list.extend(missing_letters)


# This function gets invoked each time a sample is sent. It receives a dictionary of the 2 words of the sample
# and their grades, attempting to extend the white and black list of letters.


# In this function the white and black lists are implemented - this function returns a list of legitimate words.
def find_possible_answers() -> list(str):
    filtered_list = words_list.copy()
    filtered_list2 = words_list.copy()
    for word in words_list:
        for white_char in white_list:
            if white_char not in word:
                filtered_list.remove(word)
                break

    for word in words_list:
        for black_char in black_list:
            if word in filtered_list and black_char in word:
                filtered_list.remove(word)
                break

    return filtered_list


def send_message(message) -> str:
    message_bytes = str.encode(message)
    s.sendall(message_bytes)
    return s.recv(256).decode()


with open("words.txt", "r") as file_handler:
    words_list = file_handler.read().split()

unique_pairs = (['alkxwzqbymts', 'ejucongfhvir'], ['gylarwzxspbe', 'ckdqnfmhoivu'], ['lovkfupcgqax', 'wsjybeztrimd'],
                ['zanyxhuqspfm', 'orwikcejtgdv'], ['ezawprkoynth', 'bvxudfcsmjli'], ['mwozxsqilnkp', 'vhrfjyegtdbc'],
                ['hlexacvwzuig', 'ybjsrfpqntod'], ['sobqkijugdhy', 'mnawpevcxztl'], ['mzrtyljkifcd', 'auqnohpwbxsg'],
                ['umeapvcqothx', 'dbljgkrfwnsz'], ['uaybqfkdhgoz', 'nxjvltcrmipe'], ['lfhinpcdwsza', 'tkbejgmuyqvr'],
                ['xkldjegsthri', 'mwnpvbyufqoa'])
flag = ''
while 'csa' not in flag:
    black_list = []
    white_list = []
    print("Connecting to checkpoint's server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("tricky-guess.csa-challenge.com", 2222))
    # Sleeps for 5 seconds and receives all data to clean the buffer from instructions and anti-brute force.
    time.sleep(5)
    s.recv(2048)
    print("Connected! Starting to send samples.")

    for i in range(7):
        send_sample(unique_pairs[i])

    print("black list: {}".format(black_list))
    print("white list: {}".format(white_list))

    possible_answers = find_possible_answers()
    print("\nPossible answers: %d" % len(possible_answers))
    flag = send_message(possible_answers[0])
    if 'csa' in flag:
        print(flag)
    else:
        print("Didn't manage to get the flag. Trying again...\n\n")
    s.close()
