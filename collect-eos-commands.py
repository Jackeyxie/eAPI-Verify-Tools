#!/usr/bin/env python3

"""
This script collects show commands output from devices 
Help for verify Device before & After any operations!!!!
chunlin@arista.com
"""
import os
import ssl
from sys import exit
from argparse import ArgumentParser
from getpass import getpass
from socket import setdefaulttimeout
from jsonrpclib import Server
from yaml import safe_load
import time


ssl._create_default_https_context = ssl._create_unverified_context


def device_directories(device, root_dir):
    cwd = os.getcwd()
    output_directory = os.path.dirname(cwd + "/" + root_dir + "/")
    device_directory = output_directory + '/' + device + '-' + time.strftime(
        "%Y-%m-%d-%H%M%S", time.localtime(time.time()))
    summary_directory = device_directory + '/cli_summary'
    detail_directory = device_directory + '/cli_detail'
    for directory in [output_directory, device_directory, summary_directory, detail_directory]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    result = output_directory, device_directory, summary_directory, detail_directory
    return result


def main():
    parser = ArgumentParser(
        description='Collect output of EOS commands'
    )
    parser.add_argument(
        '-i',
        help='Text file containing a list of switches',
        dest='file',
        required=True
    )
    parser.add_argument(
        '-u',
        help='Devices username',
        dest='username',
        required=True
    )
    parser.add_argument(
        '-c',
        help='YAML file containing the list of EOS commands to collect',
        dest='eos_commands',
        required=True
    )
    parser.add_argument(
        '-o',
        help='Output directory',
        dest='output_directory',
        required=True
    )
    args = parser.parse_args()
    args.password = getpass(prompt='Device password: ')

    try:
        with open(args.eos_commands, 'r', encoding='utf8') as file:
            eos_commands = file.read()
            eos_commands = safe_load(eos_commands)
    except:
        print('Error opening ' + args.eos_commands)
        exit(1)

    try:
        with open(args.file, 'r', encoding='utf8') as file:
            devices = file.readlines()
    except:
        print('Error opening ' + args.file)
        exit(1)

    for i, device in enumerate(devices):
        devices[i] = device.strip()

    # Delete unreachable devices from devices list
    unreachable = []

    print('Connecting to devices .... please be patient ... ')

    for device in devices:
        try:
            setdefaulttimeout(5)
            url = 'https://%s:%s@%s/command-api' % (
                args.username, args.password, device)
            switch = Server(url)
            response = switch.runCmds(1, ['show version'])
        except:
            unreachable.append(device)

    for item in unreachable:
        devices.remove(item)
        print("Can not connect to device " + item)

    for device in devices:
        url = 'https://%s:%s@%s/command-api' % (
            args.username, args.password, device)
        switch = Server(url)
        print('\n')
        print('Collecting show commands output on device ' + device)
        output_dir = device_directories(device, args.output_directory)
        if 'cli_summary' in eos_commands:
            for eos_command in eos_commands['cli_summary']:
                try:
                    setdefaulttimeout(10)
                    result = switch.runCmds(1, ['enable', eos_command], 'text')
                    outfile = output_dir[2] + '/' + \
                        'cli_summary' + '.txt'
                    outfile = open(outfile, 'a')
                    outfile.write(
                        "------" + eos_command + "-----------------------------------------------------------------\n")
                    outfile.write(result[1]['output'])
                    outfile.write("\n")
                    outfile.close()
                except:
                    print(
                        'Unable to collect and save the cli_summary command ' + eos_command)
        if 'cli_detail' in eos_commands:
            for eos_command in eos_commands['cli_detail']:
                try:
                    setdefaulttimeout(100)
                    result = switch.runCmds(1, ['enable', eos_command], 'text')
                    outfile = output_dir[3] + '/' + eos_command
                    outfile = open(outfile, 'w')
                    outfile.write(result[1]['output'])
                    outfile.close()
                except:
                    print(
                        'Unable to collect and save the cli_detail command ' + eos_command)


if __name__ == '__main__':
    main()
