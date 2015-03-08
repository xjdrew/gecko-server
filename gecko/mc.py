# coding: utf8
from base64 import b64encode
from string import Template
from uuid import uuid1

from gecko import app

# produce mobileconfig

pptp_template = Template('''  
        <dict>
            <key>EAP</key>
            <dict/>
            <key>IPv4</key>
            <dict>
                <key>OverridePrimary</key>
                <integer>1</integer>
            </dict>
            <key>PPP</key>
            <dict>
                <key>AuthName</key>
                <string>$user</string>
                <key>AuthPassword</key>
                <string>$password</string>
                <key>CCPEnabled</key>
                <integer>1</integer>
                <key>CCPMPPE128Enabled</key>
                <integer>1</integer>
                <key>CCPMPPE40Enabled</key>
                <integer>0</integer>
                <key>CommRemoteAddress</key>
                <string>$ip</string>
            </dict>
            <key>PayloadDescription</key>
            <string>Configures VPN settings, including authentication.</string>
            <key>PayloadDisplayName</key>
            <string>$name</string>
            <key>PayloadIdentifier</key>
            <string>$identifier</string>
            <key>PayloadOrganization</key>
            <string></string>
            <key>PayloadType</key>
            <string>com.apple.vpn.managed</string>
            <key>PayloadUUID</key>
            <string>$uuid</string>
            <key>PayloadVersion</key>
            <integer>1</integer>
            <key>Proxies</key>
            <dict/>
            <key>UserDefinedName</key>
            <string>$name</string>
            <key>VPNType</key>
            <string>PPTP</string>
            <key>PayloadOrganization</key>
            <string>$organization</string>
        </dict>
''')


def get_pptp_config(config):
    d = dict(user=config['user'],
             password=config['password'],
             ip=config['ip'],
             identifier="%s.%d" % (app.config["MC_IDENTIFIER"], config['sid']),
             uuid=str(uuid1()),
             name=config['name'],
             organization = app.config["MC_ORGANIZATION"])
    return pptp_template.substitute(d)


l2tp_template = Template('''  
        <dict>
            <key>EAP</key>
            <dict/>
            <key>IPSec</key>
            <dict>
                <key>AuthenticationMethod</key>
                <string>SharedSecret</string>
                <key>SharedSecret</key>
                <data>
                $token
                </data>
            </dict>
            <key>IPv4</key>
            <dict>
                <key>OverridePrimary</key>
                <integer>1</integer>
            </dict>
            <key>PPP</key>
            <dict>
                <key>AuthName</key>
                <string>$user</string>
                <key>AuthPassword</key>
                <string>$password</string>
                <key>CommRemoteAddress</key>
                <string>$ip</string>
            </dict>
            <key>PayloadDescription</key>
            <string>Configures VPN settings, including authentication.</string>
            <key>PayloadDisplayName</key>
            <string>$name</string>
            <key>PayloadIdentifier</key>
            <string>$identifier</string>
            <key>PayloadOrganization</key>
            <string></string>
            <key>PayloadType</key>
            <string>com.apple.vpn.managed</string>
            <key>PayloadUUID</key>
            <string>$uuid</string>
            <key>PayloadVersion</key>
            <integer>1</integer>
            <key>Proxies</key>
            <dict/>
            <key>UserDefinedName</key>
            <string>$name</string>
            <key>VPNType</key>
            <string>L2TP</string>
            <key>PayloadOrganization</key>
            <string>$organization</string>
        </dict>
''')
def get_l2tp_config(config):
    d = dict(user=config['user'],
             password=config['password'],
             ip=config['ip'],
             identifier="%s.%d" % (app.config["MC_IDENTIFIER"], config['sid']),
             uuid=str(uuid1()),
             name="%s-l2tp" % config['name'],
             token=b64encode(config['token']),
             organization = app.config["MC_ORGANIZATION"])
    return l2tp_template.substitute(d)


mc_template = Template('''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadContent</key>
    <array>
    $payload
    </array>
    <key>PayloadDescription</key>
    <string>描述文件描述。</string>
    <key>PayloadDisplayName</key>
    <string>$name</string>
    <key>PayloadIdentifier</key>
    <string>$identifier</string>
    <key>PayloadOrganization</key>
    <string></string>
    <key>PayloadRemovalDisallowed</key>
    <false/>
    <key>PayloadType</key>
    <string>Configuration</string>
    <key>PayloadUUID</key>
    <string>EA4B7102-AA10-493A-97DA-BB4C8A7FA352</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
</dict>
</plist>
''')


def get_mobileconfig(configs):
    if not configs:
        return None

    payloads = []
    for config in configs:
        if config.is_pptp():
            payloads.append(get_pptp_config(config))
        if config.is_l2tp():
            payloads.append(get_l2tp_config(config))

    d = dict(name=app.config["MC_NAME"],
             identifier=app.config["MC_IDENTIFIER"],
             payload='\n'.join(payloads))
    return mc_template.substitute(d)
