import time

FIND_ME_IN = "Log In"
FIND_ME_OUT = "Log Out"
USR_NAME_STRING = "usrName"

HTML_FILE_NAME = "index.html"

CURRENT_LOGGED_USERS = []
NR_LOGGED_USERS = 0


def follow(thefile):
    # The actual function that simulates "tail -f"
    # in unix. Returns the last written line

    thefile.seek(0, 2)

    while True:
        in_line = thefile.readline()
        if not in_line:
            time.sleep(0.1)
            continue
        yield in_line


def add_user(raw_line):
    # This function adds a new user to the list of users
    # it parses the line and fetches the user name

    global CURRENT_LOGGED_USERS
    global NR_LOGGED_USERS

    user = process_line_in(raw_line)
    print("add: Processing user: " + user)

    # make sure not to add the same user twice
    if user not in CURRENT_LOGGED_USERS:
        CURRENT_LOGGED_USERS.append(user)
        NR_LOGGED_USERS = NR_LOGGED_USERS + 1
        update_html(NR_LOGGED_USERS, CURRENT_LOGGED_USERS)
        print("Added user: " + user)

    print("Active users: " + str(NR_LOGGED_USERS))


def remove_user(raw_line):
    # This function removes a user from the list of users
    # it parses the line and fetches the user name to
    # be removed

    global CURRENT_LOGGED_USERS
    global NR_LOGGED_USERS
    user = process_line_out(raw_line)
    print("remove: Processing user: " + user)

    # avoid removing non-existant elements
    if user in CURRENT_LOGGED_USERS:
        CURRENT_LOGGED_USERS.remove(user)
        # make sure it's allways >=0 or removed users that don't exist yet
        if NR_LOGGED_USERS > 0:
            NR_LOGGED_USERS = NR_LOGGED_USERS - 1
            update_html(NR_LOGGED_USERS, CURRENT_LOGGED_USERS)
            print("Removed user: " + user)

    print("Active users: " + str(NR_LOGGED_USERS))


def update_html(_nr_logged_users, _current_logged_users):
    # Prints the list of users and their number results to an html
    # which will autorefresh every 3 seconds

    user_list_str = '\n'.join(_current_logged_users)

    header = '''<html>
  <head>
  <title>VPN Users Online: </title>
  <meta http-equiv="refresh" content="3"
  </head>
  <body>
  <h2>VPN Users Online : {}</h2>
  <h5> {} </h5>
  </body>
  </html>'''.format(_nr_logged_users, user_list_str)

    with open(HTML_FILE_NAME, 'w') as out:
        out.write(header + '\n')


def process_line_in(raw_line):
    # Finds the strings in which the user name is between
    # Strips user name from it

    index_start = raw_line.find('usrName')
    index_end = raw_line.find("attackStatus")
    return raw_line[index_start + 8:index_end].strip()


def process_line_out(raw_line):
    # Finds the strings in which the user name is between
    # Strips user name from it

    index_start = raw_line.find('usrName')
    index_end = raw_line.find("ifdir")
    return raw_line[index_start + 8:index_end].strip()


if __name__ == '__main__':

    # The main, opens file and tails it every time a keyword is found
    # adds/removes an user

    logfile = open("x.log", "r")
    loglines = follow(logfile)

    # clean up html on start
    update_html(NR_LOGGED_USERS, CURRENT_LOGGED_USERS)

    for line in loglines:
        if FIND_ME_IN in line:
            # print (line)
            add_user(line)
        if FIND_ME_OUT in line:
            # print (line)
            remove_user(line)
