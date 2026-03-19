import file_handler
import helper
import time

BASE_REQ_TEXT_DIVIDER   = "---------BaseRequirements---------"
BASE_TEXT_DIVIDER       = "----------------------------------"

SLOTH                       = range(0,6)
SNAIL                       = range(6,16)
MANATEE                     = range(16, 31)
HUMAN                       = range(31, 41)
GAZELLE                     = range(41, 51)
OSTRICH                     = range(51, 61)
CHEETAH                     = range(61, 71)
SWORDFISH                   = range(71, 81)
SPUR_WINGED_GOOSE           = range(81, 91)
WHITE_THROATED_NEEDLETAIL   = range(91, 101)
GOLDEN_EAGLE                = range(101, 121)

WRITIER_CATEGORIES = [(SLOTH, "Sloth"), (SNAIL,"Snail")
                    , (MANATEE,"Manatee"), (HUMAN,"Human")
                    , (GAZELLE, "Gazelle"), (OSTRICH, "Ostrich")
                    , (CHEETAH, "Cheetah"), (SWORDFISH, "Swordfish")
                    , (SPUR_WINGED_GOOSE, "Spur-winged goose")
                    , (WHITE_THROATED_NEEDLETAIL, "White-throated needletail")
                    , (GOLDEN_EAGLE, "Golden eagle")]

PEREGRINE_FALCON = 121

DIFFICULTY_LIST = ["easy","medium","hard"]

def word_precision(words, correct_words):
    correct_words = correct_words.split()

    total_words_in_text = len(correct_words)
    written_words = len(words)

    extra_words = max((written_words - total_words_in_text), 0)
    nr_correct_words = 0
    misspelled_words = 0

    for i in range(total_words_in_text):
        try:
            if correct_words[i] == words[i]:
                nr_correct_words += 1
            else:
                misspelled_words += 1
        except IndexError:
            misspelled_words += 1

    score_word_precision = helper.calculate_precision(nr_correct_words, extra_words
                                                    ,total_words_in_text)
    # ((nr_correct_words - extra_words) / total_words_in_text ) * 100
    score_word_precision = round(score_word_precision, 1)

    print(f"Word-precision: {score_word_precision}%")

    return_tuple = (score_word_precision, nr_correct_words, misspelled_words, extra_words)
    return return_tuple

def make_histogram(user_list, correct_list):
    histogram_dict = {}
    iterator = -1
    for item in correct_list:
        iterator += 1
        try:
            if histogram_dict.get(item) is None and item != user_list[iterator]:
                histogram_dict[item] = "#"
            elif item != user_list[iterator]:
                histogram_dict[item] += "#"
        except IndexError:
            if histogram_dict.get(item) is None:
                histogram_dict[item] = "#"
            else:
                histogram_dict[item] += "#"

    histogram_list = []
    histogram_keys = histogram_dict.keys()
    for key in histogram_keys:
        histogram_list.append( (key, histogram_dict[key]) )
    histogram_list.sort(reverse=True)
    return histogram_list

def print_histogram_from_words(user_string, correct_string):
    line_as_list = correct_string.split()
    in_string_as_list = user_string#.split()

    histogram_list = make_histogram(in_string_as_list, line_as_list)

    print("Misspelled words:")
    for item in histogram_list:
        print(item[0],item[1])

def words_per_minute(nr_misspelled_words, nr_extra_words, nr_written_words, time_minutes):
    time_minutes = max(time_minutes, 1)
    # nr_misspelled_words = 0
    # nr_extra_words = 0

    gross_wpm   = None
    net_wpm     = None
    accuracy    = None

    # for result in list_of_results:
    #     nr_misspelled_words += result[2]
    #     nr_extra_words += result[3]
    try:
        gross_wpm = nr_written_words / time_minutes
        net_wpm = gross_wpm - ((nr_misspelled_words + nr_extra_words) / time_minutes)
        accuracy = (net_wpm / gross_wpm) * 100
    except ZeroDivisionError:
        gross_wpm   = 0
        net_wpm     = 0
        accuracy    = 0

    print(f"Gross wpm: {round(gross_wpm, 2)}")
    print(f"Net wpm: {round(net_wpm, 2)}")
    print(f"Accuracy: {round(accuracy, 2)}%")

    return (gross_wpm, net_wpm, accuracy)

def writer_category(net_wpm):
    net_wpm = round(net_wpm)
    msg = "You write like a "
    if net_wpm > PEREGRINE_FALCON:
        msg += "Peregrine falcon"
    else:
        for category in WRITIER_CATEGORIES:
            if net_wpm in category[0]:
                msg += category[1]
                break
    print(msg)

def save_results(total_word_precision, difficulty):
    user_result = input("Write your name to save results: ")
    user_result += f" {total_word_precision} {difficulty}\n"
    file_handler.write_to_file("scores.txt",user_result)

def train_typing_words_from_file(filename, difficulty):
    lines = file_handler.read_lines_from_file(filename)
    all_correct_words = " ".join(lines).split()
    start_time = time.time()
    all_written_words = []

    nr_correct_words    = 0
    nr_extra_words      = 0
    nr_misspelled_words = 0

    for line in lines:
        print(line)
        written_words = input().split()

        print(BASE_TEXT_DIVIDER)
        result = word_precision(written_words, line)
        nr_correct_words    += result[1]
        nr_misspelled_words += result[2]
        nr_extra_words      += result[3]

        print_histogram_from_words(written_words, line)
        all_written_words.extend(written_words)

        print(BASE_TEXT_DIVIDER)

    # get the finish-time
    finish_time_s = time.time() - start_time

    input("Congrats! The training is done\nPress Enter to see your stats...")
    finish_time_m = round(finish_time_s / 60)
    nr_written_words = len(all_written_words)
    total_words_in_text = len(all_correct_words)

    print(BASE_REQ_TEXT_DIVIDER)

    # total word precision
    total_word_precision = helper.calculate_precision(nr_correct_words, nr_extra_words
                                                        , total_words_in_text)
    total_word_precision = round(total_word_precision, 2)


    # total word precision
    print(f"Word precision: {total_word_precision}%")

    # final histogram of all words
    print_histogram_from_words(all_written_words, " ".join(all_correct_words))

    # Finish time
    print( f"Your time was: {round(finish_time_m)} minutes and {finish_time_s} seconds")

    # get wpm results
    wpm_results = words_per_minute(nr_misspelled_words ,nr_extra_words, nr_written_words
                            , finish_time_m)

    # how well did the player write?
    writer_category(wpm_results[1])
    finish_time_s =  finish_time_s % 60
    print(BASE_TEXT_DIVIDER)

    # Save players results
    save_results(total_word_precision, difficulty)



def read_scores(filename):
    scores = file_handler.read_lines_from_file(filename)
    score_list = []
    easy_list = []
    medium_list = []
    hard_list = []
    for i in range(len(scores)):
        try:
            temp_score = scores[i]
            temp_score = temp_score.split(" ")
            temp_score[1] = float(temp_score[1])
            temp_score.insert(0, temp_score[1])
            temp_score.pop(2)

            if temp_score[2] == "easy":
                easy_list.append( temp_score )
            elif temp_score[2] == "medium":
                medium_list.append( temp_score )
            else:
                hard_list.append( temp_score )

        except IndexError:
            print("Error! file is formated wrong!")
            return

    easy_list.sort(reverse=True)
    medium_list.sort(reverse=True)
    hard_list.sort(reverse=True)

    score_list.append(easy_list)
    score_list.append(medium_list)
    score_list.append(hard_list)

    for item in score_list:
        for score in item:
            print(f"{score[1]} {score[0]}% {score[2]}")


