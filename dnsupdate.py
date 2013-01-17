import os
import socket
import urllib2
from dnsimple import DNSimple
from dnsimple.dnsimple import DNSimpleException

IP_PROVIDER='http://icanhazip.com/'

def get_settings():
    mail = os.environ.get('EMAIL')
    token = os.environ.get('TOKEN')
    domain = os.environ.get('DOMAIN')
    hostname = socket.gethostname()
    return (mail, token, domain, hostname)

def get_current_ip():
    conn = urllib2.urlopen(IP_PROVIDER)
    address = conn.read().rstrip()
    conn.close()
    return address

def update_dynamic_ip(mail, token, host, domain, address):
    try:
        dns = DNSimple(email=mail, api_token=token)
        results = dns.records(domain)
        response = "Host {0}.{1} not found for update".format(host, domain)
        for result in results:
            record = result['record']
            record_name = record['name']
            record_content = record['content'].rstrip()
            record_id = record['id']
            if record_name == host:
                if record_content == address:
                    response = None
                else:
                    record_data = { 'content' : address, 'record_type' : 'A' }
                    dns.update_record(domain, record_id, record_data)
                    response = "Updating host {0}.{1} with id {2} to address '{3}' from address '{4}'".format(record_name, domain, record_id, address, record_content)
    except DNSimpleException as e:
        response = "Error when updating dynamic address ({0})".format(e)
    return response

def main():
    (mail, token, domain, host) = get_settings()
    address = get_current_ip()
    response = update_dynamic_ip(mail, token, host, domain, address)
    if response:
        print response

if __name__ == "__main__":

    main()
