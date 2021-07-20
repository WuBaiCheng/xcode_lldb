#!/usr/bin/python

import lldb
import commands
import optparse
import shlex
import re
import os
import sys

import json

def isSuccess(error):
    # When evaluating a `void` expression, the returned value will indicate an
    # error. This error is named: kNoResult. This error value does *not* mean
    # there was a problem. This logic follows what the builtin `expression`
    # command does. See: https://git.io/vwpjl (UserExpression.h)
    kNoResult = 0x1001
    return error.success or error.value == kNoResult

# evaluates expression in Objective-C++ context, so it will work even for
# Swift projects
def evaluateExpressionValue(
    expression,
    printErrors=True,
    language=lldb.eLanguageTypeObjC_plus_plus,
    tryAllThreads=False,
):
    frame = (
        lldb.debugger.GetSelectedTarget()
        .GetProcess()
        .GetSelectedThread()
        .GetSelectedFrame()
    )
    options = lldb.SBExpressionOptions()
    options.SetLanguage(language)

    # Allow evaluation that contains a @throw/@catch.
    #   By default, ObjC @throw will cause evaluation to be aborted. At the time
    #   of a @throw, it's not known if the exception will be handled by a @catch.
    #   An exception that's caught, should not cause evaluation to fail.
    options.SetTrapExceptions(False)

    # Give evaluation more time.
    options.SetTimeoutInMicroSeconds(5000000)  # 5s

    # Most Chisel commands are not multithreaded.
    options.SetTryAllThreads(tryAllThreads)

    value = frame.EvaluateExpression(expression, options)
    error = value.GetError()

    # Retry if the error could be resolved by first importing UIKit.
    if (
        error.type == lldb.eErrorTypeExpression
        and error.value == lldb.eExpressionParseError
        and importModule(frame, "UIKit")
    ):
        value = frame.EvaluateExpression(expression, options)
        error = value.GetError()

    if printErrors and not isSuccess(error):
        print(error)

    return value

def handleCommandsWithFullPath(debugger, command):
    with open(command, 'r', encoding='utf-8') as f:
        s = f.read()
        className = command.split('/')[-1].split('.')[0]
        s = re.sub('[ \n]+{', '{', s)
        res = re.findall('-.+{', s) + re.findall('\+.+{', s)
        myCommands = []
        for i in res:
            i = re.sub(' +:', ':', i)
            res2 = ''.join(re.findall('[0-9a-zA-Z]+:', i))
            if res2 == '':
                res3 = re.findall('[0-9a-zA-Z]+{', i)
                if len(res3) > 0:
                    res2 = res3[0]
                    res2 = res2[:len(res2) - 1]
            if res2 != '':
                myCommand = 'br set -n "{}[{} {}]"'.format(i[0:1], className,res2)
                debugger.HandleCommand(myCommand)
                myCommands.append(myCommand)
        j = 0
        for tmpCmd in myCommands:
            j = j + 1
            print(j, tmpCmd)

def handleCommandsWithClassName(debugger, className):
    methodsDes = evaluateExpressionValue('''^{
        Class aClass = NSClassFromString(@"%s");
        unsigned int methodCount = 0;
        Method *methodList = class_copyMethodList(aClass, &methodCount);
        NSMutableArray *methodsArray = [NSMutableArray array];
        for (int i = 0; i < methodCount; i++) {
            Method temp = methodList[i];
            const char *name_s = sel_getName(method_getName(temp));
            NSString *methodStr = [NSString stringWithUTF8String:name_s];
            if (![methodStr hasPrefix:@"."]) {
                [methodsArray addObject:[@"-" stringByAppendingString:methodStr]];
            }
        }
        free(methodList);
        
        aClass = object_getClass(NSClassFromString(@"%s"));
        methodList = class_copyMethodList(aClass, &methodCount);
        for (int i = 0; i < methodCount; i++) {
            Method temp = methodList[i];
            const char *name_s = sel_getName(method_getName(temp));
            NSString *methodStr = [NSString stringWithUTF8String:name_s];
            if (![methodStr hasPrefix:@"."]) {
                [methodsArray addObject:[@"+" stringByAppendingString:methodStr]];
            }
        }
        free(methodList);
        
        return methodsArray;
    }()''' % (className, className)).GetObjectDescription()
    methodsDes = '\n'.join(methodsDes.split('\n')[1:])
    methods = re.findall('[-+a-zA-Z0-9:_]+', methodsDes)
    myCommands = []
    for method in methods:
        myCommand = 'br set -n "{}[{} {}]"'.format(method[0:1], className, method[1:])
        debugger.HandleCommand(myCommand)
        myCommands.append(myCommand)
    j = 0
    for tmpCmd in myCommands:
        j = j + 1
        print(j, tmpCmd)

# debugger.HandleCommand('br set -n "-[ViewController method1]"')
def addBrs(debugger, command, result, internal_dict):
    if command == '':
        currentClassName = evaluateExpressionValue("[self class]").GetObjectDescription()
        handleCommandsWithClassName(debugger, currentClassName)
    elif '/' in command:
        handleCommandsWithFullPath(debugger, command)
    else:
        handleCommandsWithClassName(debugger, command)

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f addBrs.addBrs addBrs')
    print('addBrs loaded.')