import urllib
import urllib2
import WSMA
import lxml.etree as etree
import json

# create a password manager
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

# Add the username and password.
top_level_url1 = 'https://192.168.1.76/'
top_level_url2 = 'http://192.168.1.76/'
password_mgr.add_password(None, top_level_url1, 'einarnn', 'einarnn')
password_mgr.add_password(None, top_level_url2, 'einarnn', 'einarnn')

# Create the handler.
handler = urllib2.HTTPBasicAuthHandler(password_mgr)

# create "opener" (OpenerDirector instance)
opener = urllib2.build_opener(handler)

# Install the opener. Now all calls to urllib2.urlopen use our opener.
urllib2.install_opener(opener)

# Do a 'show arp'
req = WSMA.form_http_request(
   '192.168.1.76',
   WSMA.form_input_exec_data_simple('show version', 'exec_test'))

# Do a 'hostname Router1'
# req = WSMA.form_http_request(
#     '10.10.10.110',
#     WSMA.form_input_config_data_simple('hostname Router1', 'config_test'))

resp = urllib2.urlopen(req)
print(resp.read())

#
# Now let's parse that response object
#
result = dict()
for _, element in etree.iterparse(resp):
    if element.tag=='{urn:cisco:wsma-exec}response':
        result['success'] = element.attrib['success']
        result['correlator'] = element.attrib['correlator']
    elif element.tag=='{urn:cisco:wsma-exec}text':
        result['cli-output'] = element.text
    elif element.tag=='{urn:cisco:wsma-exec}sent':
        result['cli-input'] = element.text

#
# Dump the result as JSON
#
print json.dumps(result)
