#!/bin/bash

sleep 1

pkill apache2

chmod 600 /flag
chmod 700 /start.sh
chown -R root:root /var/www/html
chmod -R 775 /var/www/html
chmod +s /usr/bin/tac
chmod +x /root/rm.sh
/root/rm.sh > /dev/null 2>&1 &

cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
sed -i 's/Options Indexes FollowSymLinks/Options None/' /etc/apache2/apache2.conf
sed -i 's/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf
sed -i 's/combined/#combined/' /etc/apache2/apache2.conf
echo 'LogFormat "%h %l %u %t \"%r\" %>s" combined' >> /etc/apache2/apache2.conf
cat /default.conf > /etc/apache2/sites-enabled/000-default.conf
rm -rf /default.conf

mv /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf
sed -i 's/ABDEFHIJZ/ABC/' /etc/modsecurity/modsecurity.conf
echo "SecAuditLog /var/log/apache2/modsec_audit.log" >> /etc/modsecurity/modsecurity.conf

service mysql start
mysql  -e "CREATE DATABASE  Nu1L  DEFAULT CHARACTER SET utf8;"  -uroot  -proot
mysql -e "create user 'Smi1e'@'localhost' identified by 'N1CTF2019';grant select on Nu1L.* to 'Smi1e'@'localhost';grant FILE on *.* to 'Smi1e'@'localhost';FLUSH PRIVILEGES;"  -uroot -proot
mysql -u root -proot Nu1L</dump.sql
mysql -e "set password for 'root'@'localhost'=password('10b64fed764fee029073f30789c1ba08');" -uroot -proot

rm -rf /dump.sql /start.sh /wkhtmltox-0.12.4_linux-generic-amd64.tar.xz /wkhtmltox /root/.mysql_history
service apache2 start
tail -F /var/log/apache2/access.log
