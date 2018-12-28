from sys import argv, exit
from csv import reader
from requests import post
from tqdm import tqdm


def get_attendee_json(csv_file):
    json_list = list()
    for attendee in csv_file:
        json_list.append({"name": attendee[0],
                          "surname": attendee[1],
                          "organization": attendee[2],
                          "degree": attendee[3]})
    return json_list


def get_section_json(csv_file):
    json_list = list()
    for attendee in csv_file:
        json_list.append({"name": attendee[0],
                          "building": attendee[1],
                          "room": attendee[2]})
    print(json_list)
    return json_list


def send_data(file, target, host="localhost:8080"):
    csv_file = open(file)
    csv = reader(csv_file, delimiter=';')
    if target == "attendees":
        json_list = get_attendee_json(csv) 
    elif target == "sections":
        json_list = get_section_json(csv)
    for json in tqdm(list(json_list)):
        response = post("http://{}/api/{}".format(host, target),
                        json=json,
                        headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            print("\n{}: {}".format(response.status_code, response.reason), end="")
            break
    csv_file.close()


host = "localhost:8080"

iter_argv = iter(argv[1:])
for arg in iter_argv:
    if arg == "--host":
        host = next(iter_argv)
    elif arg == "--attendees":
        send_data(next(iter_argv), "attendees", host)
    elif arg == "--sections":
        send_data(next(iter_argv), "sections", host)
    else:
        exit("Invalid syntax")
