import smtplib, shutil, os, subprocess, re, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-s', dest='stream', default='coremw3.2_sv', help='stream [default: %default]')
parser.add_option('-m', dest='maillist', default='joel.andersson@ericsson.com joel.andersson@ericsson.com', help='maillist to send mail to [default: %default]')
parser.add_option('-d', dest='reportdir', default='/home/eanjoel/workspace_phoenix/jcat_com_sa/src/test_env/misc/scripts/bttestprog', help='release directory [default: %default]')
(options, args) = parser.parse_args()

stream = options.stream
maillist = options.maillist
reportdir = options.reportdir

#read testreport
f = open('%s/mytestsummary.csv' % reportdir, 'r')
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

#create list of clearcase activities (compares latest baseline with latest RELEASED (promotion level) baseline)
process = subprocess.Popen(['cleartool', 'lsbl', '-component', 'CORE_MW_DEV@/vobs/coremw/pvob', '-stream', '%s@/vobs/coremw/pvob' % stream, '-short'], stdout=subprocess.PIPE)
process.wait()
baselines = process.stdout.read().split('\n')[:-1]
latest_baseline = baselines[-1]

process = subprocess.Popen(['cleartool', 'lsbl', '-component', 'CORE_MW_DEV@/vobs/coremw/pvob', '-stream', '%s@/vobs/coremw/pvob' % stream, '-short', '-level', 'RELEASED'], stdout=subprocess.PIPE)
process.wait()
baselines = process.stdout.read().split('\n')[:-1]
latest_released = baselines[-1]

process = subprocess.Popen(['cleartool', 'diffbl', '-activities', '-baselines', '%s@/vobs/coremw/pvob' % latest_released, '%s@/vobs/coremw/pvob' % latest_baseline], stdout=subprocess.PIPE)
process.wait()
artifactstemp = process.stdout.read()
artifactlist = []
for item in artifactstemp.split('\n'):
	data = '%s<br>' % item
	artifactlist.append(data)
artifacttext = '\n'.join(artifactlist)

#send a mail to specified maillist with the testreport and activity list
msg = MIMEMultipart('alternative')
me = sys.argv[0]

you = maillist.split()
msg['Subject'] = 'Test results & Activity list'
msg['From'] = me
msg['To'] = ' '.join(you)
mailhtml = """\
<html>
  <head>
    <title>Tutorial: HelloWorld</title>
  </head>
  <body>
  	<h1>Test results</h1>
	<table border="1">
	%s
	</table>
	<h1>Activity list</h1>
  	%s
  </body>
</html>
""" % (reporttabletext, artifacttext)
part1 = MIMEText(mailhtml, 'html')
msg.attach(part1)
s = smtplib.SMTP('localhost')
s.sendmail(me, you, msg.as_string())
s.quit()
