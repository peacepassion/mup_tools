#!/usr/bin/python

import subprocess
import optparse

parser = optparse.OptionParser('Usage: %prog [options] pair_code')
parser.add_option('-d', '--debug', action='store_true', dest='debug', default=False, help='switch on debug mode for more detailed output')
opt, args = parser.parse_args()

if opt.debug:
    print 'opt: ', opt
    print 'args: ', args

if len(args) == 0:
    print 'please input pair code'
    exit(1)

pair_code = args[0]

cmd1 = '''find .. -name *.apk | sed -n '1p' | xargs adb install'''

if opt.debug:
    print 'cmd1: ', cmd1

p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
out1, err1 = p1.communicate()
if opt.debug:
    print 'out1 >>>>>>>>>>>>>>'
    print out1
    print err1
    print '<<<<<<<<<<<<<< out1'

cmd2 = 'adb shell am broadcast ' \
       '-a com.android.vending.INSTALL_REFERRER ' \
       '-n com.trendmicro.mup/com.trendmicro.mup.pairing.InstallTrackingReceiver ' \
       '--es  "referrer" "utm_term=' + pair_code + '%7C3"'

if opt.debug:
    print 'cmd2: ', cmd2

p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
out2, err2 = p2.communicate()
if opt.debug:
    print 'out2 >>>>>>>>>>>>>>'
    print out2
    print err2
    print '<<<<<<<<<<<<<< out2'

