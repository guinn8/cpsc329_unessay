import curses
import enum
import json
import random
import textwrap
import sys
 
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

art = """
                 __                              _________ 
..-'''-.    ...-'  |`. ..-'''-.   ..-'''-.      /         |
\.-'''\ \   |      |  |\.-'''\ \  \.-'''\ \    '-----.   .'
       | |  ....   |  |       | |        | |       .'  .'  
    __/ /     -|   |  |    __/ /      __/ /      .'  .'    
   |_  '.      |   |  |   |_  '.     |_  '.    .'  .'      
      `.  \ ...'   `--'      `.  \      `.  \ '---'        
        \ '.|         |`.      \ '.       \ '.             
         , |` --------\ |       , |        , |             
         | | `---------'        | |        | |             
        / ,'                   / ,'       / ,'             
-....--'  /            -....--'  /-....--'  /              
`.. __..-'             `.. __..-' `.. __..-'               
"""

# Boiler plate from:
# https://gist.github.com/claymcleod/b670285f334acd56ad1c
def main(stdscr):
    global height
    global width
    global question_counter
    question_counter = 0

    f = open("questions.json", "r")
    all_quest_list = json.loads(f.read())
    q_list = random.sample(all_quest_list, 7)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.curs_set(0)

    ans = -1
    k = 0
    score = 0
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
                if (ans == q_list[question_counter]["correct"]):
                    score += 1
                question_counter += 1

                if(question_counter == QUESTIONS_TO_ASK):
                    state = quiz_state.END
                else:
                    state = quiz_state.QUESTION
                continue
            else:
                draw_question_followup(stdscr, q_list[question_counter], ans)

        elif(state == quiz_state.END):
            draw_end(stdscr, score)
        
        draw_status(stdscr, state)
       
        k = stdscr.getch()
        stdscr.refresh()

def draw_status(stdscr, state):
    statusbarstr = " Press 'q' to exit"
    quiz_sts_string = ""
    usage_str = ""
    if(state == quiz_state.QUESTION):
        quiz_sts_string = " | {} / {} Questions in quiz".format(question_counter + 1, QUESTIONS_TO_ASK)
        usage_str = " | Use keys '1' - '4' to select an answer"
    elif(state == quiz_state.QUESTION_ANS or state == quiz_state.TITLE):
        usage_str = " | Press 'Enter' to continue"

    statusbarstr += quiz_sts_string + usage_str
    status_bar_pad = " " * (width - len(statusbarstr) - 1)
    
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height-1, 0, statusbarstr)
    stdscr.addstr(height-1, len(statusbarstr), status_bar_pad)
    stdscr.attroff(curses.color_pair(3))

def draw_end(stdscr, score):
    title = "FIN"
    start_y = int((height // 2) - 2)
    start_x_title = calc_center_text(len(title))

    stdscr.addstr(start_y, start_x_title, title, curses.color_pair(1) | curses.A_BOLD)

    insult = ""
    if(score <= 2):
        insult = "U have b33n pwned scrub"
    elif(score <= 4):
        insult = "Wat are some sorta scr1pt k1ddy"
    elif(score <= 6):
        insult = "Ok you are almost 31337"
    elif(score == 7):
        insult = "We have a U8B3R 31337 H4XX0R"
    score_str = " {}, your score is {} / {} ".format(insult, score, QUESTIONS_TO_ASK)
    score_str_x = calc_center_text(len(score_str))
    stdscr.addstr(start_y + 2, score_str_x, score_str, curses.color_pair(5) | curses.A_BOLD)


def draw_question(stdscr, q):
    title = q["ask"]
    start_y = 1
    start_x_title = calc_center_text(len(title))
    stdscr.addstr(start_y, start_x_title, title, curses.color_pair(2) | curses.A_BOLD)

    start_x_choice = calc_center_text(len(q["choices"][0]))
    for i in range(0, 4):
        choice = "{}) {}".format(i+1, q["choices"][i])
        stdscr.addstr(start_y + (2 * (i + 1)), start_x_choice, choice)

def draw_question_followup(stdscr, q, ans):
    title =  q["ask"]
    start_y = 1
    start_x_title = calc_center_text(len(title))
    stdscr.addstr(start_y, start_x_title, title, curses.color_pair(2) | curses.A_BOLD)

    start_x_choice = calc_center_text(len(q["choices"][0]))
    for i in range(0, 4):
        highlight = 0
        highlight_string = ""
        if(i == ans):
            highlight = curses.color_pair(5) # red
            highlight_string = " <-- Your response"
        if(i == q["correct"]):
            highlight = curses.color_pair(4) # green
            highlight_string = " <-- Correct"
        choice = "{}) {}{}".format(i+1, q["choices"][i], highlight_string)
        stdscr.addstr(start_y + 2 * (i + 1), start_x_choice, choice, highlight)

    box1_cols = 110
    box1_rows = 8
    box1_y = start_y + 2 * (4 + 1)
    box1_x = calc_center_text(box1_cols)
    box1 = stdscr.subwin(box1_rows, box1_cols, box1_y, box1_x)
    box1.addstr(0, 0, textwrap.fill(q["explain"], box1_cols - 1)) #  box1_wid - 1 fixes some weird line breaking
    box1.immedok(True)


def draw_title(stdscr):
    title_str = "So you think you're..."
    title_str_y = 5
    title_str_x = calc_center_text(len(art.splitlines()[1]))
    stdscr.addstr(title_str_y, title_str_x, title_str, curses.A_BOLD)
    rainbow_magic = curses.COLOR_RED

    art_lines = title_str_y
    for y, line in enumerate(art.splitlines(), 0):
        start_x_title = calc_center_text(len(line))
        curses.init_pair(10 + rainbow_magic, rainbow_magic, curses.COLOR_BLACK)
        stdscr.addstr(title_str_y + y, start_x_title, line, curses.color_pair(10 + rainbow_magic))
        rainbow_magic += 1
        if (rainbow_magic > curses.COLOR_WHITE):
            rainbow_magic = curses.COLOR_RED
        art_lines += 1

    subtitle = "A quiz game designed to test your privacy and security skills!"
    start_x_subtitle = calc_center_text(len(subtitle))
    stdscr.addstr(art_lines + 1, start_x_subtitle, subtitle, curses.A_BOLD)

def calc_center_text(strlen):
    return int((width // 2) - (strlen // 2) - strlen % 2)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except curses.error:
        print("Curses threw an error, try increasing your terminal size.") 

    