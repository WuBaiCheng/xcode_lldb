#!/usr/bin/python

import lldb
import commands
import optparse
import shlex
import re
import os
import sys


def feFormat(s, className):
    s = re.sub('[ \n]+{', '{', s)
    res = re.findall('-.+{', s) + re.findall('\+.+{', s)
    myCommands = []
    res2 = []
    for i in res:
        i = re.sub(' +:', ':', i)
        res3 = ''.join(re.findall('[0-9a-zA-Z]+:', i))
        if res3 == '':
            res3 = re.findall('[0-9a-zA-Z]+{', i)[0]
            res3 = res3[:len(res3) - 1]

        myCommand = 'br set -n "{}[{} {}]"'.format(i[0:1], className,res3)
        print(myCommand)
        myCommands.append(myCommand)
    return myCommands

def addBrs(debugger, command, result, internal_dict):
    if command == '':
        # todo: how can I get the lldb result?
        # debugger.HandleCommand('po self')
        pass
    else:
        with open(command, 'r', encoding='utf-8') as f:
            c = f.read()
            # debugger.HandleCommand('br set -n "-[ViewController method1]"')
            myCommands = feFormat(c, command.split('/')[-1].split('.')[0])
            for myCommand in myCommands:
                debugger.HandleCommand(myCommand)

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f addBrs.addBrs addBrs')
    print('The python commands has been installed and is ready for use.')