#!/APSshare/anaconda3/x86_64/bin/python3

import os
import sys
import argparse
import time
import datetime as dt

import epics

SCAN_OPTIONS = {'10': 3, "5": 4, "2": 5, "1": 6, "0.5": 7, "0.2": 8, "0.1": 9}

pv = None
period = None
monitor = None
verbose = None

def vprint(message):
	global verbose
	if verbose:
		print(message)

def main(options):
	global pv
	global period
	global monitor
	global verbose
	pv = options.pv
	period = options.period
	# TODO: implement monitoring
	#!monitor = options.monitor
	verbose = options.verbose
	
	#!print(pv, type(pv))
	#!print(period, type(period))
	#!print(monitor, type(monitor))
	#!print(verbose, type(verbose))
	
	if '.' in pv:
		# The user specified a field
		scan_pv = pv.split('.')[0] + ".SCAN"
	else:
		# The user specified the record name
		scan_pv = pv + ".SCAN"
	
	#!print(scan_pv)
	
	# Set the SCAN field to the desired period
	vprint("Setting {} to {}".format(scan_pv, period))
	epics.caput(scan_pv, SCAN_OPTIONS[period])
	
	if monitor:
		# TODO: implement monitoring
		pass
	else:
		pv_obj = epics.PV(pv, auto_monitor=False)
		sleep_period = float(period)
		vprint("Polling {} every {} seconds".format(pv, period))
		
		while True:
			results = pv_obj.get_with_metadata(use_monitor=False)
			timestamp = results['timestamp']
			ts = dt.datetime.fromtimestamp(timestamp)
			message = "{} {} {}".format(pv, ts, results['value'])
			print(message)
			time.sleep(sleep_period)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("pvRecorder.py")
    
    parser.add_argument('pv', help="PV to record")
    parser.add_argument('-p', choices=SCAN_OPTIONS.keys(), dest='period', nargs='?', const='1', default='1', help="Poll period (in seconds)")
    # TODO: implement monitoring
    #!parser.add_argument('-m', dest='monitor', action="store_true", help="Monitor the PV instead of poll")
    parser.add_argument('-v', '--verbose', dest='verbose', action="store_true", help="Print extra output")
    
    options = parser.parse_args(sys.argv[1:])
    
    main(options)
