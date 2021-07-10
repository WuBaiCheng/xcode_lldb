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



于是乎，我结合自己项目调试需求：lldb命令给某个类所有方法批量加断点，以便更快捷的熟悉一个项目的逻辑走向

开发了自己定制化的lldb命令（插件）addBrs

用法也很简单，```addBrs 类的全路径```



lldb_test只是一个我用于Xcode演示的iOS项目

