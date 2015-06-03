from flask import Flask, request, jsonify
import urllib
import urllib2
import WSMA
import lxml.etree as etree
import json

app = Flask(__name__)

def extract_cli_input_and_correlator(req):
    if req.form.has_key('cli-input'):
        cli_input = req.form['cli-input']
        correlator = req.form['correlator']
    else:
        try:
            json_input = json.loads(req.data)
            cli_input = json_input['cli-input']
            correlator = json_input['correlator']
        except Exception as e:
            print 'Failed to parse req.data as JSON'
            return '', ''
    return cli_input, correlator


@app.route('/api/v1.0/exec/<string:dev_addr>', methods=['POST'])
def api_exec(dev_addr):
    cli_input, correlator = extract_cli_input_and_correlator(request)
    if len(cli_input)==0:
        return '{"success": 0}'
    req = WSMA.form_http_request(
        dev_addr,
        WSMA.form_input_exec_data_simple(cli_input, correlator))
    resp = urllib2.urlopen(req)
    result = dict()
    for _, element in etree.iterparse(resp):
        if element.tag=='{urn:cisco:wsma-exec}response':
            result['success'] = int(element.attrib['success'])
            result['correlator'] = element.attrib['correlator']
        elif element.tag=='{urn:cisco:wsma-exec}text':
            result['cli-output'] = element.text
        elif element.tag=='{urn:cisco:wsma-exec}sent':
            result['cli-input'] = element.text
    return jsonify(result)


@app.route('/api/v1.0/config/<string:dev_addr>', methods=['POST'])
def api_config(dev_addr):
    cli_input, correlator = extract_cli_input_and_correlator(request)
    if len(cli_input)==0:
        return '{"success": 0}'
    req = WSMA.form_http_request(
        dev_addr,
        WSMA.form_input_config_data_simple(cli_input, correlator))
    resp = urllib2.urlopen(req)
    result = dict()
    for _, element in etree.iterparse(resp):
        if element.tag=='{urn:cisco:wsma-config}response':
            result['success'] = int(element.attrib['success'])
            result['correlator'] = element.attrib['correlator']
        elif element.tag=='{urn:cisco:wsma-config}success':
            result['change'] = element.attrib['change']
        elif element.tag=='{urn:cisco:wsma-exec}resultEntry':
            result['cli-input'] = element.attrib['cliString']
    return jsonify(result)


if __name__ == '__main__':
    # create a password manager
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

    # Add the username and password.
    top_level_url = 'http://10.10.10.110/'
    password_mgr.add_password(None, top_level_url, 'cisco', 'cisco123')

    # Create the handler.
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)

    # create "opener" (OpenerDirector instance)
    opener = urllib2.build_opener(handler)

    # Install the opener. Now all calls to urllib2.urlopen use our opener.
    urllib2.install_opener(opener)

    app.run(debug=True)
