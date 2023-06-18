# import random
from random import *

# define path and file names
path = '<enter file directory path>'
game_data_file = '<enter name for game data file>'
high_score_file = '<enter name for high scores file>'

# functions

# function to get file
def get_file(file_name, mode):
    try:
        file = open(path + file_name, mode)
        return file
    except FileNotFoundError:
        # create file if does not exist
        open(path + file_name, 'w')
        return get_file(file_name, mode)


# function to create new game (empty map - only outlines)
def empty_map():
    # dictionary with empty fields for A1:D4
    building_rows = {
        'row_1': {
            'col_1': '1|',
            'A1': '     |',
            'B1': '     |',
            'C1': '     |',
            'D1': '     |'
        },
        'row_2': {
            'col_2': '2|',
            'A2': '     |',
            'B2': '     |',
            'C2': '     |',
            'D2': '     |'
        },
        'row_3': {
            'col_3': '3|',
            'A3': '     |',
            'B3': '     |',
            'C3': '     |',
            'D3': '     |'
        },
        'row_4': {
            'col_4': '4|',
            'A4': '     |',
            'B4': '     |',
            'C4': '     |',
            'D4': '     |'
        }
    }

    return building_rows


# function to write the map into the file
def create_map(row_dict):
    # get file
    file = get_file(game_data_file, 'w')

    # dictionary with empty strings assigned to row{num} to combine entire row values later
    combined_rows_dict = {
        'row_1': '',
        'row_2': '',
        'row_3': '',
        'row_4': ''
    }

    # combine all values per building row and update combined_rows_dict dictionary
    for row_number in row_dict:
        string = ''
        row = row_dict[row_number]

        for key in row:
            val = row[key]
            string += val

        combined_rows_dict[row_number] = string

    # put all row values in map list
    header = '    A     B     C     D   '
    divider = ' +-----+-----+-----+-----+'
    map = [header, divider]

    # loop through the rows in combined_rows_dict to add each row value into map list
    for row in combined_rows_dict:
        map.append(combined_rows_dict[row])
        map.append(divider)

    # loop through the map list to write all rows to file
    for line in map:
        file.write(line + '\n')

    # close file
    file.close()


# function to read file to print the map without the remaining buildings
def read_map_only():
    # get file
    file = get_file(game_data_file, 'r')

    # print each line from file
    for line in file:
        print(line, end='')

    # close file
    file.close()


# function to read file to print the map with remaining buildings
def read_map_buildings(buildings_dict):
    # get file
    file = get_file(game_data_file, 'r')

    # empty list to put lines from file
    map = []

    # add each line to map list
    for line in file:
        # remove \n in the line
        line = line.replace('\n', '')
        map.append(line)

    # close file
    file.close()

    # list to put headers, buildings and building count
    show_buildings = [['Building', 'Remaining'], ['--------', '---------']]

    # get the count for each building from buildings_dict
    # update show_buildings with the building and count for each type of building
    types = ['BCH', 'FAC', 'HSE', 'SHP', 'HWY']
    for building in types:
        count = buildings_dict[building]
        show_buildings.append([building, count])

    # print the map with remaining buildings on the right
    for index in range(len(map)):
        row = map[index]
        if index < len(show_buildings):
            build_1 = show_buildings[index][0]
            build_2 = show_buildings[index][1]
            print('{}{:15}{:15}{:<10}'.format(row, ' ', build_1, build_2))
        else:
            print(row)


# function to generate 2 random buildings to build
def buildings_gen(buildings_list):
    # get the buildings available - has remaining copies (not yet placed 8)
    available = []
    for pair in buildings_list:
        building = pair[0]
        count = pair[1]
        if count != 0:
            available.append(building)

    # generate 2 random buildings
    n1 = randint(0, len(available) - 1)
    building_1 = available[n1]

    # prevent duplicate building options
    while True:
        n2 = randint(0, len(available) - 1)
        if n2 != n1:
            break
    building_2 = available[n2]

    return building_1, building_2


# function to build buildings (add buildings into the map)
def build(building, location, row_dict, buildings_list):
    # get row number
    num = location[1]

    # update the map with new building in correct location
    row = row_dict['row_{}'.format(num)]
    row[location] = ' {} |'.format(building)

    # minus one for building count when the building is placed
    types = ['BCH', 'FAC', 'HSE', 'SHP', 'HWY']
    index = types.index(building)
    buildings_list[index][1] -= 1

    return row_dict, buildings_list


# function to generate boxes to check (up, down, left and right of the specified location)
def get_check_boxes(location):
    # get location's row and column
    column_let = location[0]
    column_num = ord(column_let)
    row_num = location[1]

    # get +-1 of column/row
    column_minus = chr(column_num - 1)
    column_plus = chr(column_num + 1)
    row_minus = str(int(row_num) - 1)
    row_plus = str(int(row_num) + 1)

    # combine the locations to check and add in list
    up = column_let + row_minus
    down = column_let + row_plus
    left = column_minus + row_num
    right = column_plus + row_num

    check_boxes = [up, down, left, right]

    return check_boxes


# function to check for illegal placement - not next to existing building
def validity(location, row_dict):
    # value of empty box
    empty = '     |'

    # valid columns and rows to use for checking later
    val_col = 'ABCD'
    val_row = '1234'

    col = location[0]
    row = location[1]

    # check if the specified location exists within the map
    if col not in val_col or row not in val_row:
        valid = False

        return valid

    # check if the location specified is empty and
    # return invalid if location is not empty (means that there is already a building in that location)
    elif row_dict['row_{}'.format(row)][location] != empty:
        valid = False

        return valid

    else:
        # assume placement is invalid
        valid = False

        # get the boxes to check if location 1. exists in the map 2. is not empty
        check_boxes = get_check_boxes(location)

        # check for non-empty boxes in the locations
        # non-empty means it is next to an existing building therefore valid
        for box in check_boxes:
            col = box[0]
            row = box[1]

            # skip invalid locations (out of range)
            if col not in val_col or row not in val_row:
                continue
            # check if location is empty and change validity to true if non-empty
            else:
                row_num = row_dict['row_{}'.format(row)]
                check = row_num[box]
                if check != empty:
                    valid = True
                    break

        return valid


# function to convert buildings list to dictionary
def b_list_to_dict(buildings_list):
    # create empty dictionary
    buildings_dict = {}

    # add building(key) and count(value) pairs into dictionary
    for pair in buildings_list:
        building = pair[0]
        count = pair[1]
        buildings_dict[building] = count

    return buildings_dict


# function to check if saved file is empty
def check_saved():
    # get file
    file = get_file(game_data_file, 'r')

    # file.read() to get all characters into string chars
    # if len(chars) is 0 means the file is empty hence invalid
    chars = file.read()
    if len(chars) == 0:
        valid = False
    else:
        valid = True

    return valid


# function to load saved game and update box values into dictionary
def get_saved():
    # get file
    file = get_file(game_data_file, 'r')

    # dictionary to get and update A1:D4 values
    building_rows = {
        'row_1': {
            'col_1': '',
            'A1': '',
            'B1': '',
            'C1': '',
            'D1': ''
        },
        'row_2': {
            'col_2': '',
            'A2': '',
            'B2': '',
            'C2': '',
            'D2': ''
        },
        'row_3': {
            'col_3': '',
            'A3': '',
            'B3': '',
            'C3': '',
            'D3': ''
        },
        'row_4': {
            'col_4': '',
            'A4': '',
            'B4': '',
            'C4': '',
            'D4': ''
        }
    }

    # number of line from file
    line_num = 1
    # list of line numbers of lines with building row value (eg 1|     |...|)
    valid_rows = [3, 5, 7, 9]
    # row number to access dictionary
    row_val = 1

    for line in file:
        # lines with building row values
        if line_num in valid_rows:
            # split line by '|' to get list containing values like
            # ['1', '     ', ' BCH ', ..., '\n']
            line_split = line.split('|')

            # remove \n from end of line
            new_line = line_split[-1]
            line_split.remove(new_line)

            # integer value of column letter - start with A
            column_num = 65

            # add box value into dictionary
            for index in range(len(line_split)):
                string = line_split[index] + '|'
                correct_row = building_rows['row_{}'.format(row_val)]
                column_let = chr(column_num)

                # first value is column number (eg 1|)
                if index == 0:
                    correct_row['col_{}'.format(row_val)] = string
                # other values is buildings or empty space (eg:' BCH |' or '     |')
                else:
                    correct_row[column_let + str(row_val)] = string

                    # increase column_num by 1 to get next letter
                    column_num += 1

            # increase row_val by 1 to access next row
            row_val += 1

        # increase line_num to get the line numbers
        line_num += 1

    # close file
    file.close()

    return building_rows


# function to determine which turn the saved game is at
def get_turn(row_dict):
    # value of empty box
    empty = '     |'

    # number of non-empty boxes
    filled = 0

    for row_num in row_dict:
        row = row_dict[row_num]
        for key in row:
            # skip column boxes (eg 1|, 2|)
            if 'col' in key:
                continue
            # add one to filled for each non-empty box
            else:
                value = row[key]
                if value != empty:
                    filled += 1

    # turn number is the number of built buildings + 1
    turn = filled + 1

    return turn


# function to get buildings and count from saved game - update saved_buildings list
def get_buildings(row_dict):
    # value of empty box
    empty = '     |'

    # list of rows to access dictionary
    rows = ['row_1', 'row_2', 'row_3', 'row_4']
    # list of building types
    types = ['BCH', 'FAC', 'HSE', 'SHP', 'HWY']
    # empty list to fill in building type and count from saved map
    buildings = []
    # empty list to fill in existing building types from saved map
    existing_buildings = []

    for row_num in rows:
        row = row_dict[row_num]
        for key in row:
            val = row[key]
            # skip column boxes
            if 'col' in val:
                continue
            # add building name into existing_buildings if it exists
            else:
                if val != empty:
                    # replace space and | with empty string to leave behind building name only
                    # eg ' BCH |' --> 'BCH'
                    val = val.replace(' ', '')
                    val = val.replace('|', '')
                    existing_buildings.append(val)

    # get the number of buildings per building type in existing_buildings list
    # add building type and count to buildings list
    for building in types:
        count = existing_buildings.count(building)
        buildings.append([building, count])

    # subtract the existing buildings' count from saved_buildings list to get the actual amount of remaining buildings
    # remove the default value (8) and add the actual value
    for index in range(len(buildings)):
        existing = buildings[index][1]
        initial = saved_buildings[index].pop()
        new = initial - existing
        saved_buildings[index].append(new)

    return saved_buildings


# function to clear file content
def clear_file():
    # get file
    file = get_file(game_data_file, 'w')

    # close file
    file.close()


# function to get non-empty boxes - to get buildings scores later
def non_empty(row_dict):
    # value of empty box
    empty = '     |'

    # put non-empty box location and values into lists (box_key & box_val respectively)
    box_key = []
    box_val = []

    for row_num in row_dict:
        row = row_dict[row_num]
        for key in row:
            val = row[key]
            if 'col' in key:
                continue
            else:
                # add location and building into box_key and box_val if the box is not empty
                if val != empty:
                    # replace space and | with empty string to leave behind building name only
                    # eg ' BCH |' --> 'BCH'
                    val = val.replace(' ', '')
                    val = val.replace('|', '')
                    box_key.append(key)
                    box_val.append(val)

    return box_key, box_val


# function to calculate BCH score
def bch_score(box_key, box_val):
    # empty list to store individual BCH values
    score_bch = []
    # total value of BCH
    total_bch = 0

    for index in range(len(box_key)):
        key = box_key[index]
        val = box_val[index]

        # add score for each BCH into list based on conditions
        if 'BCH' in val:
            col = key[0]
            if col == 'A' or col == 'D':
                score = 3
            else:
                score = 1

            score_bch.append(score)

    # calculate total BCH score
    if len(score_bch) > 0:
        for pt in score_bch:
            total_bch += pt

    return score_bch, total_bch


# function to calculate FAC score
def fac_score(box_val):
    # empty list to store individual FAC values
    score_fac = []
    # total number of FAC to calculate scores later
    fac_num = 0
    # total value of FAC
    total_fac = 0

    # get number of FAC in map
    for box in box_val:
        if 'FAC' in box:
            fac_num += 1

    # add score to list based on conditions
    if fac_num <= 4:
        score = fac_num
        for index in range(fac_num):
            score_fac.append(score)
    else:
        # first 4 FAC
        score = 4
        for index in range(4):
            score_fac.append(score)

        # remaining FAC
        score2 = 1
        num = fac_num - 4
        for index2 in range(num):
            score_fac.append(score2)

    # calculate total FAC score
    if len(score_fac) > 0:
        for pt in score_fac:
            total_fac += pt

    return score_fac, total_fac


# function to calculate HSE score
def hse_score(row_dict, box_key, box_val):
    # empty list to store individual HSE values
    score_hse = []
    # total value of HSE
    total_hse = 0

    for index in range(len(box_key)):
        key = box_key[index]
        val = box_val[index]

        if 'HSE' in val:
            # get box locations to check for adjacent buildings
            check_boxes = get_check_boxes(key)

            # valid rows and columns
            valid_col = 'ABCD'
            valid_row = '1234'

            # number of points
            score = 0

            # check for invalid boxes
            for box in check_boxes:
                col = box[0]
                row = box[1]

                # skip invalid boxes (out of range)
                if col not in valid_col or row not in valid_row:
                    continue

                # check for FAC, HSE, SHP or BCH in box
                # determine points based on conditions
                else:
                    correct_row = row_dict['row_{}'.format(row)]
                    check_val = correct_row[box]

                    if 'HSE' in check_val or 'SHP' in check_val:
                        score += 1

                    elif 'BCH' in check_val:
                        score += 2

                    elif 'FAC' in check_val:
                        score = 1

                        break

            # add score to list
            score_hse.append(score)

    # calculate total HSE score
    if len(score_hse) > 0:
        for pt in score_hse:
            total_hse += pt

    return score_hse, total_hse


# function to calculate SHP score
def shp_score(row_dict, box_key, box_val):
    # empty list to store individual SHP values
    score_shp = []
    # total value of SHP
    total_shp = 0
    # list containing the valid building types
    valid_types = ['BCH', 'FAC', 'HSE', 'SHP', 'HWY']

    for index in range(len(box_key)):
        key = box_key[index]
        val = box_val[index]

        # empty list to store the adjacent buildings
        types = []

        if 'SHP' in val:
            # get box locations to check for adjacent buildings
            check_boxes = get_check_boxes(key)

            # valid rows and columns
            valid_col = 'ABCD'
            valid_row = '1234'

            # check for different buildings in boxes
            for box in check_boxes:
                col = box[0]
                row = box[1]

                # skip invalid boxes (out of range)
                if col not in valid_col or row not in valid_row:
                    continue
                # check for different types of buildings in box
                else:
                    correct_row = row_dict['row_{}'.format(row)]
                    check_val = correct_row[box]

                    # add building into list if building does not exist in list - unique buildings in list
                    for building in valid_types:
                        if building in check_val:
                            if building in types:
                                break
                            else:
                                types.append(building)
                                break

            # determine score based on conditions
            # add scores into list
            score = len(types)
            score_shp.append(score)

    if len(score_shp) > 0:
        # calculate total SHP score
        for pt in score_shp:
            total_shp += pt

    return score_shp, total_shp


# function to calculate HWY score
def hwy_score(row_dict):
    # empty list to store individual HWY values
    score_hwy = []
    # total value of HWY
    total_hwy = 0
    # list containing rows to access dictionary
    rows = ['row_1', 'row_2', 'row_3', 'row_4']

    for row_num in rows:
        # empty string to add box values
        values = ''
        row = row_dict[row_num]

        # add HWY to values if HWY exists
        # add space to values if HWY does not exist
        for key in row:
            val = row[key]

            if 'HWY' in val:
                values += 'HWY'
            else:
                values += ' '

        # split values to get only two kinds of values - 'HWY' * n, and empty string ''
        # where n represents the number of HWY connected in a row
        # remove empty strings to leave behind only HWY values
        val_list = values.split(' ')

        for index in range(len(val_list)):
            if '' in val_list:
                val_list.remove('')
            else:
                break

        if len(val_list) > 0:
            # calculate number of connected HWY and add to list
            # take the length of the HWY value and divide by 3 to get the number of connected HWY
            # eg len('HWYHWY') // 3 = 2 means two connected HWY
            for hwy in val_list:
                score = len(hwy) // 3
                for times in range(score):
                    score_hwy.append(score)

    if len(score_hwy) > 0:
        # calculate total HWY score
        for pt in score_hwy:
            total_hwy += pt

    return score_hwy, total_hwy


# function to compile scores for each building and print
def print_score(row_dict):
    # get box_key and box_val variables for functions that need them
    box_key, box_val = non_empty(row_dict)

    # lists for score lists, total scores and building types respectively
    buildings_score = []
    buildings_total = []
    buildings = []

    # get the score for each building type if there are non-empty boxes (len(box_key))
    # add {building}_list to buildings_score
    # add {building}_pt to buildings_total
    # add building name to buildings
    if len(box_key) > 0:
        if 'BCH' in box_val:
            bch_list, bch_pt = bch_score(box_key, box_val)
            buildings_score.append(bch_list)
            buildings_total.append(bch_pt)
            buildings.append('BCH')

        if 'FAC' in box_val:
            fac_list, fac_pt = fac_score(box_val)
            buildings_score.append(fac_list)
            buildings_total.append(fac_pt)
            buildings.append('FAC')

        if 'HSE' in box_val:
            hse_list, hse_pt = hse_score(row_dict, box_key, box_val)
            buildings_score.append(hse_list)
            buildings_total.append(hse_pt)
            buildings.append('HSE')

        if 'SHP' in box_val:
            shp_list, shp_pt = shp_score(row_dict, box_key, box_val)
            buildings_score.append(shp_list)
            buildings_total.append(shp_pt)
            buildings.append('SHP')

        if 'HWY' in box_val:
            hwy_list, hwy_pt = hwy_score(row_dict)
            buildings_score.append(hwy_list)
            buildings_total.append(hwy_pt)
            buildings.append('HWY')

        # get building name, building scores and total scores to format string and print
        for index in range(len(buildings)):
            type = buildings[index]
            scores = buildings_score[index]
            total = buildings_total[index]

            # string to add numbers to print equation
            # assign the first value to the string and add '+' and next value later
            eqn = str(scores[0])

            # get the full equation (add all individual scores per building type)
            for index2 in range(len(scores)):
                # skip first value
                if index2 == 0:
                    continue
                else:
                    # add scores for each building type to equation
                    num = str(scores[index2])
                    eqn = eqn + ' + ' + num

            print('{}: {} = {}'.format(type, eqn, total))

        # calculate total score for all buildings
        pt_sum = 0
        for score in buildings_total:
            pt_sum += score

    else:
        # if there are no non-empty boxes then total score is 0
        pt_sum = 0

    print('Total score: {}'.format(pt_sum))


# function to calculate total score to use to check for high score
def cal_total(row_dict):
    # get box_key and box_val variables for functions that need them
    box_key, box_val = non_empty(row_dict)

    # list for total points per building type
    scores = []
    # total score for all buildings
    total = 0

    # get the score for each building type if there are non-empty boxes (len(box_key))
    # add total score per building to scores list
    if len(box_key) > 0:
        if 'BCH' in box_val:
            bch_list, bch_pt = bch_score(box_key, box_val)
            scores.append(bch_pt)

        if 'FAC' in box_val:
            fac_list, fac_pt = fac_score(box_val)
            scores.append(fac_pt)

        if 'HSE' in box_val:
            hse_list, hse_pt = hse_score(row_dict, box_key, box_val)
            scores.append(hse_pt)

        if 'SHP' in box_val:
            shp_list, shp_pt = shp_score(row_dict, box_key, box_val)
            scores.append(shp_pt)

        if 'HWY' in box_val:
            hwy_list, hwy_pt = hwy_score(row_dict)
            scores.append(hwy_pt)

        # calculate total score for all buildings
        for score in scores:
            total += score

    return total


# function to check if score is in top 10
def check_score(score, check_score_list):
    # get the number of scores that are the same as the current score in high scores
    count = check_score_list.count(score)
    check_score_list.append(score)
    check_score_list.sort()
    check_score_list.reverse()
    # get index of the current score and add count - puts it at last position for the same scores
    index = check_score_list.index(score) + count

    # if the index <= 9 means the score is in top 10
    # else it means it is ranked 11 - not in high score
    if index < 10:
        valid = True
    else:
        valid = False

    # remove the last score if the length of the list is greater than 10
    if len(check_score_list) > 10:
        check_score_list.remove(check_score_list[-1])

    return valid, index, check_score_list


# function to add name and score to high_scores_list
def add_score_list(score, name, index):
    # add name and score to high_scores_list at the found index in check_score
    high_scores_list.insert(index, [score, name])
    # remove the last nested list if the length of the list is greater than 10
    if len(high_scores_list) > 10:
        high_scores_list.remove(high_scores_list[-1])

    return high_scores_list


# function to add name and score to high_scores_dict
def add_score_dict(high_scores_list):
    # get score and name from high_scores_list
    # get dict_no ({number}.) - to access dictionary
    # update dictionary[dict_no] with list containing score and name
    for index in range(len(high_scores_list)):
        score = high_scores_list[index][0]
        name = high_scores_list[index][1]
        score_name = [score, name]
        dict_no = str(index + 1) + '.'
        high_scores_dict[dict_no] = score_name

    return high_scores_dict


# function to show high scores
def show_high(high_scores_dict):
    # headers for high scores section
    headings = [['-' * 9, ' HIGH SCORES ', '-' * 9],
                ['Pos ', '{:22}'.format('Player'), 'Score'],
                ['--- ', '{:22}'.format('------'), '-----']]
    # last line for high scores section (---...)
    end = '-' * 31
    print()

    # put the different parts of the header into one string and print headers
    for header_list in headings:
        val = ''
        for part in header_list:
            val += part

        print(val)

    for key in high_scores_dict:
        # get score and name list from dictionary
        score_name = high_scores_dict[key]
        # get the list for position 1
        first = high_scores_dict['1.']
        # if the list is empty list means there is no high scores yet
        # print none and break
        if first == []:
            print('{:-^31s}'.format(' None '))
            break
        # else print position, name and score
        # break when the position is empty list - end of high scores recorded
        else:
            if score_name == []:
                break
            else:
                name = score_name[1]
                score = score_name[0]

                print('{:>3s} {:22s}{:>5d}'.format(key, name, score))

    print(end)


# function to get high scores and names from file
def get_high_score():
    # get file
    file = get_file(high_score_file, 'r')

    # list to get score and name pair from file
    score_name = []
    # list to get only scores - to update check_scores_list to check for high scores later
    scores = []

    # remove \n from line
    # split the line to get a list containing score and name
    # add score and name list into score_name
    for line in file:
        line = line.replace('\n', '')
        split_line = line.split(',')
        score_name.append(split_line)

    # add score into scores list
    for index in range(len(score_name)):
        score_name[index][0] = int(score_name[index][0])
        score = score_name[index][0]
        scores.append(score)

    return score_name, scores


# function to write high scores and names into file
def high_scores_file(high_scores_dict):
    # get file
    file = get_file(high_score_file, 'w')

    # get the list containing score and name from dictionary
    for pos in high_scores_dict:
        pair = high_scores_dict[pos]
        # write score and name into file
        # break when the list is empty list - end of high scores recorded
        if pair == []:
            break
        else:
            score = pair[0]
            name = pair[1]
            file.write('{},{}\n'.format(score, name))

    # close file
    file.close()


# function to check score and update high_scores_dict
def update_high(row_dict, check_score_list, high_scores_list):
    # get total score
    # check if score is in high score
    # if yes ask for name and update list/dictionary then write the new dictionary into file
    # show the high scores
    total = cal_total(row_dict)
    high, index, check_score_list = check_score(total, check_score_list)
    if high == True:
        print('\nCongratulations! You made the high score board at \nposition {}!'.format(index + 1))
        while True:
            name = input('Please enter your name (max 20 chars): ')
            if len(name) <= 20:
                break
            else:
                print('Name cannot be more than 20 characters!')

        high_scores_list = add_score_list(total, name, index)
        high_scores_dict = add_score_dict(high_scores_list)
        high_scores_file(high_scores_dict)

        # show high scores
        show_high(high_scores_dict)

    # if no print message
    else:
        print('\nUnfortunately, you did not make it into the high score board. Try again!')


# program code

# introduction sentence
intro = ['Welcome, mayor of Simp City!', '-' * 28]

for sentence in intro:
    print(sentence)

# main menu options
main_menu = ['\n1. Start new game', '2. Load saved game', '3. Show high scores', '\n0. Exit']
# valid main menu choices
valid_choices = ['0', '1', '2', '3']
# valid in game options
valid_options = ['0', '1', '2', '3', '4']

while True:

    # list of buildings and building count for empty map (new map)
    new_buildings = [['BCH', 8], ['FAC', 8], ['HSE', 8], ['SHP', 8], ['HWY', 8]]
    # list of buildings for saved game - modify later to get correct building counts
    saved_buildings = [['BCH', 8], ['FAC', 8], ['HSE', 8], ['SHP', 8], ['HWY', 8]]
    # dictionary for username and high score
    high_scores_dict = {
        '1.': [],
        '2.': [],
        '3.': [],
        '4.': [],
        '5.': [],
        '6.': [],
        '7.': [],
        '8.': [],
        '9.': [],
        '10.': []
    }

    # list to update high_scores_dict
    high_scores_list = []
    # list to check if score is in high scores
    check_score_list = []

    # print main menu options
    for opt in main_menu:
        print(opt)

    # get input for main menu options
    choice = input('Your choice? ')

    # check if choice is in valid choices
    # if yes then get integer value of choice and carry on to play
    # else show message and continue
    if choice in valid_choices:
        choice_check = int(choice)
    else:
        print('Enter a valid option!')
        continue

    # print message and quit if main menu choice is 0
    if choice_check == 0:
        print('You quit!')
        break

    elif choice_check == 1 or choice_check == 2:
        # create empty map if choice is 1
        if choice_check == 1:
            turn = 1

            # row dictionary is empty map
            row_dict = empty_map()
            # write the map into file
            create_map(row_dict)
            # buildings_list is new_buildings list
            buildings_list = new_buildings

        # get saved game rows and turn if choice is 2
        elif choice_check == 2:
            # check if saved file is empty and go back to main menu if file is empty
            valid_saved = check_saved()
            if valid_saved == False:
                print('No saved game found.')
                continue
            else:
                # row dictionary is updated with existing buildings from saved game
                row_dict = get_saved()
                # get turn number from saved game
                turn = get_turn(row_dict)
                # get the actual remaining building counts from saved game and update saved_buildings list
                saved_buildings = get_buildings(row_dict)
                # buildings_list is the new saved_buildings list
                buildings_list = saved_buildings

        while True:

            # print turn number
            print('\nTurn {}'.format(turn))

            # get buildings dictionary to print remaining buildings
            buildings_dict = b_list_to_dict(buildings_list)
            # print map with remaining buildings
            read_map_buildings(buildings_dict)
            # clear file contents - no auto save
            # otherwise it defeats the purpose of having option 4 - save game
            clear_file()

            # generate 2 buildings
            b1, b2 = buildings_gen(buildings_list)

            # options description
            des = ['\n1. Build a {}'.format(b1), '2. Build a {}'.format(b2),
                   '3. See current score', '\n4. Save game', '0. Exit to main menu']

            # print the options available
            for line in des:
                print(line)

            # get input in game
            option = input('Your choice? ')

            # check if option is in valid options
            # if yes then get integer value of options and carry on to play
            # else show message and continue
            if option in valid_options:
                option_check = int(option)
            else:
                print('Enter a valid option!')
                # write map into file so that read_map_buildings() will show the current map
                create_map(row_dict)
                continue

            # clear file contents
            # end game and go back to main menu if option is 0
            if option_check == 0:
                clear_file()
                break

            # get location if option is 1 or 2
            elif option_check == 1 or option_check == 2:
                location = input('Build where? ').upper()

                # check if length of location is 2 (letter + number is 2 characters)
                # if no then show message and continue
                # else carry on to do further checking
                if len(location) != 2:
                    print('Enter a valid location!')
                    # write map into file so that read_map_buildings() will show the current map
                    create_map(row_dict)
                    continue

                else:
                    # valid columns and rows that exist in the map
                    valid_cols = 'ABCD'
                    valid_rows = '1234'
                    col = location[0]
                    row = location[1]

                # check if the location exists in the map
                # if no then show message and continue
                # else carry on to do further checking/build building
                if col not in valid_cols or row not in valid_rows:
                    print('Enter a valid location!')
                    # write map into file so that read_map_buildings() will show the current map
                    create_map(row_dict)
                    continue
                else:
                    # check turn number and validate location if turn is not 1 - must be next to existing building
                    # if location is valid, build building
                    if turn >= 2:
                        valid = validity(location, row_dict)
                        # build building and write the new map into file if location is valid
                        # else show message and continue
                        if valid == True:
                            turn += 1
                            if option_check == 1:
                                building = b1
                            else:
                                building = b2
                            row_dict, buildings_list = build(building, location, row_dict, buildings_list)
                            create_map(row_dict)
                        else:
                            print('You must build next to an existing building.')
                            # write map into file so that read_map_buildings() will show the current map
                            create_map(row_dict)
                            continue
                    # if turn is 1 then no need to check if location is next to existing building
                    # build building and write the new map into file
                    else:
                        turn += 1
                        if option_check == 1:
                            building = b1
                        else:
                            building = b2
                        row_dict, buildings_list = build(building, location, row_dict, buildings_list)
                        create_map(row_dict)

            # show total score if option is 3
            elif option_check == 3:
                print()
                # show the scores for each building and total score
                print_score(row_dict)
                # write map into file so that read_map_buildings() will show the current map
                create_map(row_dict)

            # save game and exit to main menu if option is 4
            elif option_check == 4:
                # write the map into file to save progress then show message and break
                create_map(row_dict)
                print('\nGame saved!')
                break

            # show final layout and total score if turn is 17 (end of game)
            # return to main menu
            if turn == 17:
                print('\nFinal layout of Simp City: ')

                # print map without remaining buildings
                read_map_only()
                # show the scores for each building and total score
                print_score(row_dict)
                # remove file contents - game finished and cannot be continued anymore
                clear_file()

                # get high_scores_list and check_score_list from file
                high_scores_list, check_score_list = get_high_score()

                # get total score
                # check if score is in high score
                # if yes ask for name and update list/dictionary then write the new dictionary into file
                # show the high scores
                # if no print message
                update_high(row_dict, check_score_list, high_scores_list)

                break

    # show high scores if choice is 3
    elif choice_check == 3:
        high_scores_list, check_score_list = get_high_score()
        high_scores_dict = add_score_dict(high_scores_list)
        show_high(high_scores_dict)
