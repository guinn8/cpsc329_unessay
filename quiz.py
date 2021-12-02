import curses
import enum
import json
 
class quiz_state(enum.Enum):
    TITLE = 1
    QUESTION = 2
    END = 3

QUESTIONS_TO_ASK = 7
ENTER = 10

# Boiler plate from:
# https://gist.github.com/claymcleod/b670285f334acd56ad1c
def main(stdscr):
    global height
    global width
    global question_counter

    f = open("questions.json", "r")
    q_list = json.loads(f.read())

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    k = 0
    question_counter = 0
    state = quiz_state.TITLE
    while (k != ord('q')):
        height, width = stdscr.getmaxyx()
        stdscr.clear()

        if(state == quiz_state.TITLE):
            if(k == ENTER):
                state = quiz_state.QUESTION
                continue
            draw_title(stdscr)

        elif(state == quiz_state.QUESTION):
            draw_question(stdscr, q_list[0])
            question_counter += 1
            if(question_counter > QUESTIONS_TO_ASK):
                state = quiz_state.END
                continue

        elif(state == quiz_state.END):
            draw_end(stdscr)
        
        draw_status(stdscr)
        stdscr.refresh()
        k = stdscr.getch()

def draw_status(stdscr):
    statusbarstr = "Press 'q' to exit"
    quiz_sts_string = ""
    if(question_counter > 0 and question_counter <= QUESTIONS_TO_ASK):
        quiz_sts_string = " | {} /  {}  Questions in quiz".format(question_counter, QUESTIONS_TO_ASK)

    statusbarstr += quiz_sts_string
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
    start_y = int((height // 2) - 2)
    start_x_title = calc_center_text(title)

    stdscr.addstr(start_y, start_x_title, title, curses.color_pair(2) | curses.A_BOLD)

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
    