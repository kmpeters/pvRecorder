# pvRecorder

### Usage
```
hostname% ./pvRecorder.py -h
usage: pvRecorder.py [-h] [-p [{10,5,2,1,0.5,0.2,0.1}]] [-f FILE_PREFIX] [-v] pv

positional arguments:
  pv                    PV to record

optional arguments:
  -h, --help            show this help message and exit
  -p [{10,5,2,1,0.5,0.2,0.1}]
                        Poll period (in seconds)
  -f FILE_PREFIX        File prefix
  -v, --verbose         Print extra output
hostname%
```

### Example
```
hostname% ./pvRecorder.py -p 0.5 -v -f "test" IOC:adam1:tc0.VAL
Setting IOC:adam1:tc0.SCAN to 0.5
Polling IOC:adam1:tc0.VAL every 0.5 seconds
Opening test_20220708-152140.txt for writing
IOC:adam1:tc0.VAL 2022-07-08 15:21:39.697560 21.0
IOC:adam1:tc0.VAL 2022-07-08 15:21:41.008412 21.0
IOC:adam1:tc0.VAL 2022-07-08 15:21:41.509158 21.0
IOC:adam1:tc0.VAL 2022-07-08 15:21:42.008275 21.0
IOC:adam1:tc0.VAL 2022-07-08 15:21:42.008275 21.0
IOC:adam1:tc0.VAL 2022-07-08 15:21:43.007901 21.0
IOC:adam1:tc0.VAL 2022-07-08 15:21:43.512137 21.0
IOC:adam1:tc0.VAL 2022-07-08 15:21:44.007841 21.0
IOC:adam1:tc0.VAL 2022-07-08 15:21:44.007841 21.0
IOC:adam1:tc0.VAL 2022-07-08 15:21:45.008024 21.0
IOC:adam1:tc0.VAL 2022-07-08 15:21:45.511916 21.0
^C
Closing test_20220708-152140.txt
hostname% 
```
