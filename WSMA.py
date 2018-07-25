import urllib
import urllib2
import lxml.etree as etree
from jinja2 import Template

#
# Some constants for creating WSMA payloads. Very, very simple for
# now. Can add stuff like correlators later.
#
exec_template = Template("""<?xml version="1.0" encoding="UTF-8"?> 
<SOAP:Envelope xmlns:SOAP="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" 
xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
 <SOAP:Body>
  <request xmlns="urn:cisco:wsma-exec" correlator="{{CORRELATOR}}">
   <execCLI>
    <cmd>{{EXEC_CMD}}</cmd>
   </execCLI>
  </request>
 </SOAP:Body>
</SOAP:Envelope>""")

config_template = Template("""<?xml version="1.0" encoding="UTF-8"?>
<SOAP:Envelope xmlns:SOAP="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" 
xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
 <SOAP:Body>
  <request xmlns="urn:cisco:wsma-config" correlator="{{CORRELATOR}}">
   <configApply details="all">
    <config-data>
     <cli-config-data>
      <cmd>{{CONFIG_CMD}}</cmd>
     </cli-config-data>
    </config-data>
   </configApply>
  </request>
 </SOAP:Body>
</SOAP:Envelope>""")

config_block_template = Template("""<?xml version="1.0" encoding="UTF-8"?>
<SOAP:Envelope xmlns:SOAP="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" 
xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
 <SOAP:Body>
  <request xmlns="urn:cisco:wsma-config" correlator="{{CORRELATOR}}">
   <configApply details="all">
    <config-data>
     <cli-config-data-block>{{CONFIG_CMDS}}</cli-config-data-block>
    </config-data>
   </config>
  </request>
 </SOAP:Body>
</SOAP:Envelope>""")

def form_input_exec_data_simple(exec_cmd, correlator):
    """
    Create a simple WSMA exec request payload from a single CLI.
    """
    return exec_template.render(EXEC_CMD=exec_cmd, CORRELATOR=correlator)

def form_input_config_data_simple(config_cmd, correlator):
    """
    Create a simple WSMA config request payload from a single CLI.
    """
    return config_template.render(CONFIG_CMD=config_cmd, CORRELATOR=correlator)

def form_input_config_data_block(config_cmd_block, correlator):
    """
    Create a simple WSMA config request payload from a single CLI.
    """
    return config_block_template.render(CONFIG_CMDS=config_cmd_block, CORRELATOR=correlator)

def form_http_request(device_addr_or_fqdn,exec_data):
    """
    Create a WSMA POST request from the IP or FQDN of the device plus the payload.
    """
    return urllib2.Request('http://'+device_addr_or_fqdn+'/wsma', exec_data)

def form_https_request(device_addr_or_fqdn,exec_data):
    """
    Create a WSMA POST request from the IP or FQDN of the device plus the payload.
    """
    return urllib2.Request('https://'+device_addr_or_fqdn+'/wsma_secure', exec_data)

def extract_exec_response_simple(xml_from_wsma):
    """
    Pull out just the raw text response for now.
    """
    root = etree.fromstring(xml_from_wsma);
    

#
# Simple test code to demonstrate usage.
#
if __name__ == "__main__":

    # We need to authenticate, so create a password manager
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

    # Add the username and password to the password manager
    top_level_url = 'http://10.10.10.110/'
    password_mgr.add_password(None, top_level_url, 'cisco', 'cisco123')

    # Create the Basic Auth handler to use
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)

    # Create the "opener" (OpenerDirector instance)
    opener = urllib2.build_opener(handler)

    # Install the opener. Now all calls to urllib2.urlopen use our
    # opener.
    urllib2.install_opener(opener)

    # A device usually in the AiO VM
    device_addr = '10.10.10.110'

    # Let's do a ping!
    ping_data = form_input_exec_data_simple('ping 10.10.10.110', 'ping')

    # Now create the basic request, secure form
    ping_reqs = form_https_request(device_addr, ping_data)

    # Finally, we can do the request!!!
    resps = urllib2.urlopen(ping_reqs)

    # Print the response!
    print resps.read()
