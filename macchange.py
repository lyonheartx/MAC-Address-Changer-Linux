#!/usr/bin/python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface (NIC) to change it's MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Updated MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error(" [+] Please select an interface (NIC/Adapter) to change MAC Address, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please choose a new MAC address, use --help for more info.")
        return options


def change_mac(interface, new_mac):
    print("[+] Change MAC address of: " + interface + "to" + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current(interface):
    ipconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ipconfig_result)

    if mac_result:
        return mac_result.group(0)
    else:
        print("(/-_-)/ Sorry, could not read MAC address.")


options = get_arguments()
current_mac = get_current(options.interface)
print("Current MAC Address is: = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was changed to: " + current_mac)
else:
    print("[-] MAC address was not changed. " + current_mac)
