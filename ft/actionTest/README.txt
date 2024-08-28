This is instructon how to run function test on action
=====================================================

Create a new model
------------------

Note: This step can be skipped if only regression test is executed.

1. Install RAS
2. Open RAS
   Import project from /vobs/com_sa/dev/src/test/actionTest/dxtool/Sdp617ActionTest
3. Do the changes
4. Create new model files for COM and IMM: 
	Right click on model Sdp617ActionTestModel ->  ECIM -> Transform to...
	Deselect "MMAS CM POJO"
	Click OK 
	The models will be generated to directory dxtool/Sdp617ActionTest/Output_Models/Sdp617ActionTestModel   
 
5. Copy the new model files to model
   > cp  dxtool/Sdp617ActionTest/Output_Models/Sdp617ActionTestModel/*.xml model/


Build actionTestAppl
--------------------

> cd implementor
> make clean; make

Copy to target machine
--------------------

> scp dxtool/Sdp617ActionTest/Output_Models/Sdp617ActionTestModel/Sdp617ActiontestMom_mp.xml root@134.138.66.169:/cluster/actionTest/
> scp dxtool/Sdp617ActionTest/Output_Models/Sdp617ActionTestModel/Sdp617ActiontestMom_imm_classes.xml root@134.138.66.169:/cluster/actionTest/
> scp implementor/actionTestAppl root@134.138.66.169:/cluster/actionTest/
   
Setup target machine
--------------------
   
> ssh root@<ip address>                 (eg ssh root@134.138.66.169)

edit file /cluster/home/com/etc/model/model_file_list.cfg:
  insert /cluster/actionTest/Sdp617ActiontestMom_mp.xml
 
# pkill com  

Setup actiontest appl:   
# cd /cluster/actionTest
# immcfg -f Sdp617ActiontestMom_imm_classes.xml
# immcfg -c Sdp617ActiontestRoot sdp617ActiontestRootId=1
# immcfg -c ActionTest actionTestId=1,sdp617ActiontestRootId=1

# ./actionTestAppl &
# kill -usr2 $!
  
Create SSH key (if running from a new machine)
--------------
> cd $HOME/.ssh
> ssh-keygen -t rsa -f key_rsa_<hostname>               (eg. hostname = seasc0663)
> scp key_rsa_<hostname>.pub root@<ip-address>:/tmp
> ssh root@<ip-address>

# cat /tmp/key_rsa_<hostname>.pub >> /boot/patch/root/.ssh/authorized_keys
# cat /tmp/key_rsa_<hostname>.pub >> /root/.ssh/authorized_keys

Run function test from  development machine
-------------------------------------------
> cd /vobs/com_sa/dev/src/test/actionTest/netconf
> ./runalltests.sh <ip-address> <ssh key>                (ssh key = key_rsa_<hostname>)

   
