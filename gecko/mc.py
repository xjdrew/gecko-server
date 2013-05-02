# coding: utf8
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
    <string>配置 VPN 设置（包括鉴定）。</string>
    <key>PayloadDisplayName</key>
    <string>VPN (91vpn2)</string>
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
</dict>
''')


def get_pptp_config(config):
    d = dict(user=config['user'],
             password=config['password'],
             ip=config['ip'],
             identifier="%s.%d" % (app.config["MC_IDENTIFIER"], config['sid']),
             uuid=str(uuid1()),
             name=config['name'])
    return pptp_template.substitute(d)


def get_l2tp_config(name, user, password, token):
    pass


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
        payloads.append(get_pptp_config(config))

    d = dict(name=app.config["MC_NAME"],
             identifier=app.config["MC_IDENTIFIER"],
             payload='\n'.join(payloads))
    return mc_template.substitute(d)
