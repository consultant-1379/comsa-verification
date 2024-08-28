import mechanize

br = mechanize.Browser()
br.set_proxies({"http": "www-proxy.ericsson.se:3132"})
br.open("https://cc-isisupp.rnd.ki.sw.ericsson.se/RDA/")
assert br.viewing_html()
br.select_form(nr=0)
print "old=", br
br['userid'] = 'hudsonuser'
br['email'] = 'joel.andersson@ericsson.com'
br['componentname1'] = ['coremw',]
br['path1'] = '/home/hudsonuser/cmwbuilds/second/COREMW_RUNTIME-CXP9020355_1.tar'
br['inst1'] = '/home/hudsonuser/cmwbuilds/second/COREMW_DEPLOYMENT_TEMPLATE-CXP9017564_1.tar'
print "new=", br

#res = br.submit()
#print res
