#!/APSshare/anaconda3/x86_64/bin/python3

import os
import sys
import argparse
import time
import datetime as dt
from pathlib import Path

import epics

SCAN_OPTIONS = {'10': 3, "5": 4, "2": 5, "1": 6, "0.5": 7, "0.2": 8, "0.1": 9}

pv = None
period = None
file_prefix = None
monitor = None
verbose = None

def vprint(message):
	global verbose
	if verbose:
		print(message)

def fprint(fh, message):
	if fh != None:
		fh.write(message + os.linesep)

def main(options):
	# Get the timestamp as close to the start as possible
	now = time.strftime("%Y%m%d-%H%M%S")
	
	global pv
	global period
	global file_prefix
	global monitor
	global verbose
	pv = options.pv
	period = options.period
	file_prefix = options.file_prefix
	# TODO: implement monitoring
	#!monitor = options.monitor
	verbose = options.verbose
	
	#!print(pv, type(pv))
	#!print(period, type(period))
	#!print(file_prefix, type(file_prefix))
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
		
		#
		fh = None
		if file_prefix != None:
			filename = "{}_{}.txt".format(file_prefix, now)
			filepath = Path(filename)
			if filepath.exists():
				print("Error: file already exists")
				sys.exit(1)
			else:
				vprint("Opening {} for writing".format(filename))
				fh = open(filename, "a", buffering=128)
		
		try:
			while True:
				results = pv_obj.get_with_metadata(use_monitor=False)
				timestamp = results['timestamp']
				ts = dt.datetime.fromtimestamp(timestamp)
				message = "{} {} {}".format(pv, ts, results['value'])
				fprint(fh, message)
				print(message)
				time.sleep(sleep_period)
		except KeyboardInterrupt:
			vprint("\nClosing {}".format(filename))
		finally:
			fh.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser("pvRecorder.py")
    
    parser.add_argument('pv', help="PV to record")
    parser.add_argument('-p', choices=SCAN_OPTIONS.keys(), dest='period', nargs='?', const='1', default='1', help="Poll period (in seconds)")
    parser.add_argument('-f', dest='file_prefix', action="store", help="File prefix")
    # TODO: implement monitoring
    #!parser.add_argument('-m', dest='monitor', action="store_true", help="Monitor the PV instead of poll")
    parser.add_argument('-v', '--verbose', dest='verbose', action="store_true", help="Print extra output")
    
    options = parser.parse_args(sys.argv[1:])
    
    main(options)
