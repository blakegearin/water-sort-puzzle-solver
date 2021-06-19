import copy
import itertools
import json
import os
import sys

def get_input(filename):
  f = open(filename)
  data = json.load(f)
  f.close()

  for (k, v) in data.items():
    if k == "height":
      height = v
    elif k == "flasks":
      flasks = v

  return [height, flasks]

def delete_output_files():
  i = 0
  while os.path.exists(f"output/{i}.json"):
    os.remove(f"output/{i}.json")
    i += 1

def log_output(data):
  for i, value in enumerate(data):
    f = open(f"output/{i}.json", "w")
    f.write(json.dumps(value))
    f.close()

def list_to_string(l):
  flatten_l = list(itertools.chain(*l))
  return "".join(map(str, flatten_l))

def count_continuous_colors(flask):
  count = 0
  last_color = ""
  # print(flask)
  for color in reversed(flask):
    if last_color == "":
      last_color = color
    elif color == last_color:
      count += 1
    else:
      count = 0
      last_color = 0

  return count

def pour(array, duplicate, move, height):
  # print(f"Start of pour: {array}")

  if duplicate:
    flasks = copy.deepcopy(array)
  else:
    flasks = array

  beg = move["flasks"][0]
  end = move["flasks"][1]

  print(f"beg {beg}")
  top_color = flasks[beg][-1]
  # print(flasks)
  while len(flasks[beg]) > 0 and top_color == flasks[beg][-1] and len(flasks[end]) < height:
    top_color = flasks[beg].pop()
    flasks[end].append(top_color)

  # print(f"End of pour: {flasks}")
  return flasks

def determine_moves(flasks):
  possible_moves = []
  for i, beg_flask in enumerate(flasks):
    if len(beg_flask) > 0:
      top_color = beg_flask[-1]
      for j, end_flask in enumerate(flasks):
        if i != j and (len(end_flask) == 0 or (len(end_flask) < height and top_color == end_flask[-1])):
          rank = 1

          if len(end_flask) != 0 and len(flasks[j])+1 == height:
            rank += count_continuous_colors(flasks[j])
            # print(i)

          move = {
            "rank": rank,
            "flasks": [i, j]
          }
          possible_moves.append(move)
  return possible_moves

def check_solved(flasks, height):
  solved = True

  for flask in flasks:
    flask_height = len(flask)
    # print(f"flask {flask} has height: {flask_height}")

    if flask_height == 0:
      next
    elif flask_height != height:
      solved = False
      break
    else:
      print(f"top_color: {top_color}")
      top_color = flask[-1]
      flask.reverse()
      for color in flask:
        # print(f"color: {color}")
        if color != top_color:
          solved = False
          break

  if solved:
    print(f"Solved: {flasks}")
  return solved

def search_moves(flasks, height, winning_moves):
  print()
  print(f"Winning moves: {winning_moves}")
  print(flasks)
  # print(str(len(moves_made)))
  if len(winning_moves) > 100:
    # print("states_seen")
    # print(states_seen)
    log_output(states_seen)
    return null

  # while not check_solved(flasks, height):
  print("In loop")
  # solved = check_solved(flasks, height)
  # if solved:
  #   return winning_moves
  # else:
  moves = determine_moves(flasks)
  if len(moves) == 0:
    print("Zero moves!")
    return ["stuck"]
  else:
    # print(f"winning_moves after else: {winning_moves}")
    current_winning_moves = copy.deepcopy(winning_moves)
    current_flasks = copy.deepcopy(flasks)
    # print("setting")
    # print(winning_moves_before_move)
    sorted_moves = sorted(moves, key = lambda i: i["rank"], reverse=True)
    # print(f"Moves: {sorted_moves}")

    for i, move in enumerate(sorted_moves):
      count.append(1)
      current_count = len(count)

      flasks = current_flasks
      winning_moves = current_winning_moves

      print(f"Starting move {current_count} with values {move} and winning_moves {winning_moves}")

      sorted_flasks = copy.deepcopy(flasks)
      sorted_flasks.sort()

      if len(states_seen) > 1 and sorted_flasks != [] and sorted_flasks != starting_flasks and sorted_flasks in states_seen:
        # print(f"Seen sorted_flasks: {sorted_flasks}")
        next
      else:
        # print(f"Not solved: {flasks}")

        # print(f"Pushing flasks to states")
        states_seen.append(sorted_flasks)
        # print(f"winning_moves: {winning_moves}")
        print(f"On move {i} of {len(sorted_moves)-1}, winning_moves: {winning_moves}")
        # if len(count) > 20:
        #   print(states_seen)
        #   return null

        moves_match = False
        tuples_match = False
        quad_match = False

        if len(winning_moves) >= 1:
          latest_move = copy.deepcopy(move["flasks"])
          latest_move.reverse()

          last_move = copy.deepcopy(winning_moves[-1])
          last_move.reverse()

          moves_match = \
            (move["flasks"] == winning_moves[-1]) or \
            (latest_move == winning_moves[-1])

          if len(winning_moves) >= 3:
            latest_tuple = [last_move, latest_move]
            last_tuple = [winning_moves[-3], winning_moves[-2]]

            tuples_match = latest_tuple == last_tuple

            second_last_move = copy.deepcopy(winning_moves[-2])
            second_last_move.reverse()

            if len(winning_moves) >= 5:
              if latest_move == winning_moves[-3] and last_move == winning_moves[-5] and second_last_move == winning_moves[-4]:
                quad_match = True

        if moves_match or tuples_match or quad_match:
          print(f"Stuck! moves_match: {moves_match} , tuples_match: {tuples_match}, quad_match: {quad_match}, winning_moves: {winning_moves}")
          return ["stuck"]
        else:
          winning_moves.append(move["flasks"])

          print(f"Count {count}, trying move: {move}")
          winning_moves = winning_moves + search_moves(pour(flasks, False, move, height), height, winning_moves)
          print(f"Returned to count {current_count} and move {move} with winning_moves {winning_moves}")
          if "stuck" in winning_moves:
            print("Nexting")
            next
          else:
            return winning_moves
    print(f"Count {current_count}")
    # if "stuck" in winning_moves:
    #   return ["stuck"]
    # else:
    return winning_moves


  return winning_moves


# print(sys.argv[0])
# input = get_input(sys.argv[0])
for i in sys.argv[1:]:
  input = get_input(i)

height = input[0]
starting_flasks = input[1]

states_seen = []
count = []


delete_output_files()
winning_moves = search_moves(copy.deepcopy(starting_flasks), height, [])

# print(check_solved(starting_flasks, height))

print()
print()
print(winning_moves)
if not 0 in winning_moves and not "stuck" in winning_moves and winning_moves != []:
  for m in winning_moves:
    move = {
      "flasks": m
    }
    pour(starting_flasks, False, move, height)
    print(f"flasks {starting_flasks}")
  print(starting_flasks)

print("Done")
