# Xcode_lldb
熟练掌握Xcode自带的lldb，再深入定制开发自己需要的lldb插件



```help``` 获取所有可用命令

另外，例如```help po```可以获取po命令的用法



《**与调试器共舞 - LLDB 的华尔兹**》这篇译文还是讲的非常全面的！

https://objccn.io/issue-19-2/



里面介绍了facebook开发的lldb插件集合chisel，还是挺好用的

https://github.com/facebook/chisel



另外，也借鉴了别人在lldb中迁移ls命令的用法

https://zhuanlan.zhihu.com/p/34634263



也可以通过命令删除断点

https://www.jianshu.com/p/70423a4ddf65?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation



于是乎，我结合自己项目调试需求：lldb命令给某个类所有方法批量加断点，以便更快捷的熟悉一个项目的逻辑走向

开发了自己定制化的lldb命令（插件）addBrs

用法有3种：

- ```addBrs 类文件全路径``` 后回车，为指定类加断点

- ```addBrs``` 后回车，为本类加断点

- ```addBrs 类名``` 后回车，为指定类加断点

后2种方式，虽然写起来不繁琐，但有个小缺陷：

需要在加断点的类中#import <objc/runtime.h>



lldb_test只是一个我用于Xcode演示的iOS项目

addBrs.py是核心实现代码，注意其中不能含中文



为了能在Xcode打开后，自动载入自己写的lldb插件，这里需要在~/下创建.lldbinit文件（如果它原本不存在才创建）、打开、植入载入自己写的插件脚本

```
cd ~
touch .lldbinit
open .lldbinit
```

写入以下内容到.lldbinit中，后保存，杀死Xcode进程、重新打开即可生效：

```command script import addBrs.py完整路径```

例如我的：

```
command script import /Users/wubocheng/Documents/xcode_lldb/addBrs.py
```

