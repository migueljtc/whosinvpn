import time

find_me_in = "Log In"
find_me_out = "Log Out"
usr_name_string = "usrName"

html_file_name = "index.html"

current_logged_users = []
nr_logged_users = 0


def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def add_user(raw_line):
    global current_logged_users
    global nr_logged_users 

    user = process_line_in(raw_line)
    print ("add: Processing user: " + user)

    #make sure not to add the same user twice
    if user not in current_logged_users:
        current_logged_users.append(user)
        nr_logged_users = nr_logged_users + 1
        update_html(nr_logged_users, current_logged_users)
        print ("Added user: " + user )

    print("Active users: " + str(nr_logged_users))

def remove_user(raw_line):
    global current_logged_users
    global nr_logged_users
    user = process_line_out(raw_line)
    
    print ("remove: Processing user: " + user)

    #avoid removing non-existant elements
    if user in current_logged_users:
        current_logged_users.remove(user)
        #make sure it's allways >=0 or removed users that don't exist yet
        if nr_logged_users > 0:
            nr_logged_users = nr_logged_users - 1
            update_html(nr_logged_users, current_logged_users)
            print ("Removed user: " + user )

    print("Active users: " + str(nr_logged_users))


def update_html(nr_logged_users, current_logged_users):
    user_list_str = '\n'.join(current_logged_users)
     
    header =''' <html>
  <head>
  <title>VPN Users Online: </title>
  <meta http-equiv="refresh" content="3"
  </head>
  <body>
  <h2>VPN Users Online : {}</h2>
  <h5> {} </h5>
  </body>
  </html>'''.format(nr_logged_users, user_list_str)

    with open(html_file_name, 'w') as out:
        out.write(header + '\n')


def process_line_in(raw_line):
    index_start =  raw_line.find('usrName')
    index_end = raw_line.find("attackStatus")
    return raw_line[index_start+8:index_end].strip()

def process_line_out(raw_line):
    index_start =  raw_line.find('usrName')
    index_end = raw_line.find("ifdir")
    return raw_line[index_start+8:index_end].strip()


if __name__ == '__main__':
    logfile = open("x.log","r")
    loglines = follow(logfile)

    #clean up html on start 
    #update_html(nr_logged_users, current_logged_users)

    for line in loglines:
        if find_me_in in line: 
            #print (line)
            add_user (line)
        if find_me_out in line:
            #print (line)
            remove_user (line)
