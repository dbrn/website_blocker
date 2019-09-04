# python 3.5+
from time import sleep, localtime
import argparse


def restore_hosts(hosts_file, original_contents):
    print("Unblocking hosts")
    with open(hosts_file, "w") as file:
        file.write(original_contents)


def main():
    hosts_file = "/etc/hosts"
    parser = argparse.ArgumentParser()
    parser.add_argument("timespan", help="The timespan when you want to block sites (eg: 8-18)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", help="File with the hosts to forbid", nargs=1, type=str)
    group.add_argument("-l", "--list", help='A list of hosts to forbid separated by space enclosed in ""'
                                            '(eg: "facebook.com twitter.com', type=str)
    args = parser.parse_args()
    times = tuple(map(int, args.timespan.split("-")))
    if times[0] > times[1]:
        print("Starting hour must be earlier than the ending one")
        return
    if args.file:
        with open(args.file[0], "r") as file:
            hosts_to_block = file.readlines()
    elif args.list:
        hosts_to_block = str(args.list).split()
    with open(hosts_file, "r") as file:
        original_hosts = file.read()
    started = False
    try:
        while True:
            hour = localtime()
            hour = hour[3]
            if times[0] <= hour < times[1] and started is False:
                print("Blocking hosts")
                started = True
                with open(hosts_file, "a") as file:
                    for host in hosts_to_block:
                        file.write(f"127.0.0.1 {host}\n")
            if hour >= times[1] and started is True:
                restore_hosts(hosts_file, original_hosts)
                started = False
            sleep(10)
    except KeyboardInterrupt:
        restore_hosts(hosts_file, original_hosts)
        print("\nApp terminated. Bye!")


if __name__ == "__main__":
    main()
