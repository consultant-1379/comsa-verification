#!/bin/bash
connect_to_serial 134.138.66.7 7009 > Cots-19_SC-1.log & connect_to_serial 134.138.66.7 7010 > Cots-19_SC-2.log & connect_to_serial 134.138.66.6 7015 > Cots-7_SC-1.log & connect_to_serial 134.138.66.6 7016 > Cots-7_SC-2.log
