#!/usr/bin/python

import optparse
import subprocess

parser = optparse.OptionParser()
parser.add_option('-d', '--debug', action='store_true', dest='debug', default=True)
opt, args = parser.parse_args()

if opt.debug:
    print 'opt: ', opt
    print 'args: ', args

cmd1 = 'adb uninstall com.trendmicro.mup'

p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
o1, e1 = p1.communicate()
if opt.debug:
    print 'out >>>>>>>>>>>>>>'
    print o1
    print '<<<<<<<<<<<<<< out'

