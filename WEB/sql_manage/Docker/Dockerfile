FROM reyesoft/php-mysql56

COPY sources.list /etc/apt/sources.list

RUN wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg \
    && apt-get update \
    && apt-get install -y apache2 libapache2-mod-php7.1 libapache2-mod-security2 --allow-unauthenticated\
    && rm -rf /var/www/html/* \
    && a2enmod rewrite \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY dump.sql /dump.sql

COPY source /var/www/html
COPY flag /flag
COPY start.sh /start.sh
COPY php.ini /etc/php/7.1/apache2/php.ini
COPY default.conf /default.conf
COPY my.cnf /etc/mysql/conf.d/mysql.cnf
COPY rm.sh /root/rm.sh

RUN chmod +x /start.sh

WORKDIR /var/www/html

ENTRYPOINT ["/start.sh"]