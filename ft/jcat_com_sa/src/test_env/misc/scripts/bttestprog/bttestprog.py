import smtplib, shutil, os, subprocess, re, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-s', dest='stream', default='coremw3.2_sv', help='stream [default: %default]')
parser.add_option('-n', dest='btname', default='COREMW_3.2_04', help='blue train name [default: %default]')
parser.add_option('-a', dest='btarea', default='/home/eanjoel/Desktop/temp/mybtareatest', help='blue train area [default: %default]')
parser.add_option('-r', dest='releasedir', default='/vobs/coremw/release/cxp_archive', help='release directory [default: %default]')
(options, args) = parser.parse_args()

stream = options.stream
btname = options.btname
btarea = options.btarea
releasedir = options.releasedir
btarchives = '%s/archives' % btarea
btnext = '%s/next' % btarea
cmwfiles = ['COREMW_COMMON-CXP9017566_1.sdp', 'COREMW_DEPLOYMENT_TEMPLATE-CXP9017564_1.tar', 'COREMW_OPENSAF-CXP9017656_1.sdp', 'COREMW_RUNTIME-CXP9020355_1.tar', 'COREMW_SC-CXP9017565_1.sdp', 'COREMW_SDK-CXP9020356_1.cxp'] #, 'COREMW-CAY901198_1-R2A05.tar.gz'] 

#read testreport
f = open('mytestsummary.csv', 'r')
testreport = f.readlines()
f.close()
reporttable = []
for line in testreport:
	elements = line.strip().split(',')
	reporttable.append('<tr>')
	for element in elements:
		data = '<td>%s</td>' % element
		reporttable.append(data)
	reporttable.append('</tr>')
reporttabletext = '\n'.join(reporttable)

#create list of clearcase activities
process = subprocess.Popen(['cleartool', 'lsbl', '-component', 'CORE_MW_DEV@/vobs/coremw/pvob', '-stream', '%s@/vobs/coremw/pvob' % stream, '-short'], stdout=subprocess.PIPE)
process.wait()
baselines = process.stdout.read().split('\n')[:-1]
latest_baseline = baselines[-1]
process = subprocess.Popen(['cleartool', 'diffbl', '-predecessor', '%s@/vobs/coremw/pvob' % latest_baseline], stdout=subprocess.PIPE)
process.wait()
artifactstemp = process.stdout.read()
artifactlist = []
for item in artifactstemp.split('\n'):
	#data = '<p>%s</p>' % item
	data = '%s<br>' % item
	artifactlist.append(data)
artifacttext = '\n'.join(artifactlist)

#upload the release to the BT ftp area and create an empty file in next folder
btdir = '%s/%s' % (btarchives, btname)
if not os.path.exists(btdir):
	os.makedirs(btdir)
for item in cmwfiles:
	bundle = item.split('.')[0]
	extension = item.split('.')[-1]
	src = '%s/%s' % (releasedir, item)
	process = subprocess.Popen(['packageinfo', '%s/%s' % (releasedir, item)], stdout=subprocess.PIPE)
	process.wait()
	packageinfo = process.stdout.read().split('\n')[0]
	revision = packageinfo.split('-')[-1]
	dest = '%s/%s-%s.%s' % (btdir, bundle, revision, extension)
	shutil.copyfile(src, dest)
open('%s/%s' % (btnext, btname), 'w').close()

#display a list of the files that have been successfully uploaded
filelist = []
for file in os.listdir('%s/%s' % (btarchives, btname)):
	#data = '<p>%s/%s/%s</p>' % (btarchives, btname, str(file))
	data = '%s/%s/%s<br>' % (btarchives, btname, str(file))
	filelist.append(data)
for file in os.listdir(btnext):
	if re.search(btname,file):
		#data = '<p>%s/%s</p>' % (btnext, str(file))
		data = '%s/%s<br>' % (btnext, str(file))
		filelist.append(data)

#send a mail to the DO-team with the testreport and activity list
msg = MIMEMultipart('alternative')
me = 'joel.andersson@ericsson.com'
you = 'joel.andersson@ericsson.com'
msg['Subject'] = btname
msg['From'] = me
msg['To'] = you
mailhtml = """\
<html>
  <head>
    <title>Tutorial: HelloWorld</title>
  </head>
  <body>
  	<h1>Activity list</h1>
  	%s
  	<h1>Test results</h1>
	<table border="1">
	%s
	</table>
	<h1>Blue train file list</h1>
	%s
  </body>
</html>
""" % (artifacttext, reporttabletext, '\n'.join(filelist))
part1 = MIMEText(mailhtml, 'html')
msg.attach(part1)
s = smtplib.SMTP('localhost')
s.sendmail(me, [you], msg.as_string())
s.quit()