import curses
import enum
import json
import random
 
class quiz_state(enum.Enum):
    TITLE = 1
    QUESTION = 2
    END = 3
    QUESTION_ANS = 4

QUESTIONS_TO_ASK = 7
ASCII_ENTER = 10
ASCII_1 = 49
ASCII_2 = 50
ASCII_3 = 51
ASCII_4 = 52

# Boiler plate from:
# https://gist.github.com/claymcleod/b670285f334acd56ad1c
def main(stdscr):
    global height
    global width
    global question_counter

    f = open("questions.json", "r")
    all_quest_list = json.loads(f.read())
    q_list = random.sample(all_quest_list, 7)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    ans = -1
    k = 0
    question_counter = 0
    state = quiz_state.TITLE
    while (k != ord('q')):
        height, width = stdscr.getmaxyx()
        stdscr.clear()

        if(state == quiz_state.TITLE):
            if(k == ASCII_ENTER):
                state = quiz_state.QUESTION
                continue
            else:
                draw_title(stdscr)

        elif(state == quiz_state.QUESTION):
            if (ASCII_1 <= k <= ASCII_4):
                state = quiz_state.QUESTION_ANS
                ans = k - ASCII_1
                continue
            else:
                draw_question(stdscr, q_list[question_counter])

        elif(state == quiz_state.QUESTION_ANS):
            assert(ans != -1)
            if(k == ASCII_ENTER): 
                question_counter += 1
                if(question_counter == QUESTIONS_TO_ASK):
                    state = quiz_state.END
                else:
                    state = quiz_state.QUESTION
                continue
            else:
                draw_question_followup(stdscr, q_list[question_counter], ans)

        elif(state == quiz_state.END):
            draw_end(stdscr)
        
        draw_status(stdscr)
        stdscr.refresh()
        k = stdscr.getch()

def draw_status(stdscr):
    statusbarstr = "Press 'q' to exit"
    quiz_sts_string = ""
    if(question_counter > 0 and question_counter <= QUESTIONS_TO_ASK):
        quiz_sts_string = " | {} / {} Questions in quiz".format(question_counter, QUESTIONS_TO_ASK)

    statusbarstr += quiz_sts_string + " | Use keys '1' - '4' to select an answer"
    status_bar_pad = " " * (width - len(statusbarstr) - 1)
    
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height-1, 0, statusbarstr)
    stdscr.addstr(height-1, len(statusbarstr), status_bar_pad)
    stdscr.attroff(curses.color_pair(3))

def draw_end(stdscr):
    title = "FIN"
    start_y = int((height // 2) - 2)
    start_x_title = calc_center_text(title)

    stdscr.addstr(start_y, start_x_title, title, curses.color_pair(1) | curses.A_BOLD)

def draw_question(stdscr, q):
    title = q["ask"]
    start_y = 1
    start_x_title = calc_center_text(title)
    stdscr.addstr(start_y, start_x_title, title, curses.color_pair(2) | curses.A_BOLD)

    for i in range(0, 4):
        choice = "{}) {}".format(i+1, q["choices"][i])
        start_x_choice = calc_center_text(choice)
        stdscr.addstr(start_y + (2 * (i + 1)), start_x_choice, choice)

def draw_question_followup(stdscr, q, ans):
    title = "followup" + str(ans) #q["ask"]
    start_y = 1
    start_x_title = calc_center_text(title)
    stdscr.addstr(start_y, start_x_title, title, curses.color_pair(2) | curses.A_BOLD)

    for i in range(0, 4):
        choice = "{}) {}".format(i+1, q["choices"][i])
        start_x_choice = calc_center_text(choice)
        stdscr.addstr(start_y + (2 * (i + 1)), start_x_choice, choice)

def draw_title(stdscr):
    title = "Curses example"[:width-1]
    subtitle = "Written by Clay McLeod"[:width-1]

    start_x_title = calc_center_text(title)
    start_y = int((height // 2) - 2)

    stdscr.addstr(start_y, start_x_title, title, curses.color_pair(2) | curses.A_UNDERLINE)

    start_x_subtitle = calc_center_text(subtitle)
    stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
    stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)

def calc_center_text(str):
    return int((width // 2) - (len(str) // 2) - len(str) % 2)

if __name__ == "__main__":
    curses.wrapper(main)
    