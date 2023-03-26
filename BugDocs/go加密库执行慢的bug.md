1. 起因

    之前项目都是基于python+flask开发，由于业务需要，有部分业务需要使用golang进行重构(小白刚接触golang一个月![](image/2023-03-26-11-46-38.png))，在重构之后的测试过程中，发现重构之后的性能反倒没有提升，竟然下滑了....

2. 问题表现

    所有源码地址：BugDocs/src/goEncrypt

    在做登录接口测试时，发现接口响应居然很慢，我这里放出一张移除业务的代码测试结果：

    测试环境：
    ```shell
    Go 1.19
    Python 3.9.13
    werkzeug 2.2.3
    循环迭代次数 1024
    ```

    ![](image/2023-03-26-11-06-46.png)

    上图中，左右两个框是golang编译前后的执行耗时，中间的是Python的执行耗时，golang用时92s左右，Python用时70s左右，相差20几秒？？？纳尼，什么情况？？？

3. 问题排查

    由于是Web项目，使用go提供的pprof进行排查。在server启动中导入CPU占用分析工具`import _ "net/http/pprof"`, 开始对server进行性能测试，测试过程中使用`go tool pprof http://127.0.0.1:8080/debug/pprof/profile`在命令行中获取当前cpu执行情况，通过`top 10` 及`top cum 10`查看cpu占用及过去cpu占用情况，得到的结果如下：

    ```shell
    Showing top 10 nodes out of 35
        flat  flat%   sum%        cum   cum%
        295.63s 62.87% 62.87%    295.64s 62.88%  crypto/sha256.block
        29.22s  6.21% 69.09%    453.22s 96.39%  golang.org/x/crypto/pbkdf2.Key
        22.54s  4.79% 73.88%    328.80s 69.93%  crypto/sha256.(*digest).Write
        19.77s  4.20% 78.09%    341.29s 72.59%  crypto/sha256.(*digest).checkSum
        18s  3.83% 81.92%        18s  3.83%  runtime.memmove
        16.01s  3.41% 85.32%     17.08s  3.63%  runtime.(*itabTableType).find
        13.21s  2.81% 88.13%     13.24s  2.82%  crypto/sha256.consumeUint32
        6.66s  1.42% 89.55%     27.11s  5.77%  crypto/sha256.(*digest).UnmarshalBinary
        6.45s  1.37% 90.92%    390.41s 83.03%  crypto/hmac.(*hmac).Sum
        6.30s  1.34% 92.26%       355s 75.50%  crypto/sha256.(*digest).Sum
    (pprof) top -cum 10
    Showing nodes accounting for 42.15s, 8.96% of 470.19s total
    Dropped 561 nodes (cum <= 2.35s)
    Showing top 10 nodes out of 35
        flat  flat%   sum%        cum   cum%
        0.05s 0.011% 0.011%    464.12s 98.71%  net/http.(*conn).serve
        0.01s 0.0021% 0.013%    460.42s 97.92%  net/http.(*ServeMux).ServeHTTP
            0     0% 0.013%    460.42s 97.92%  net/http.serverHandler.ServeHTTP
        0.03s 0.0064% 0.019%    460.39s 97.92%  net/http.HandlerFunc.ServeHTTP
        0.08s 0.017% 0.036%    460.35s 97.91%  goweb/views.Login
            0     0% 0.036%    453.26s 96.40%  goweb/utils.CheckPasswordHash
        0.01s 0.0021% 0.038%    453.25s 96.40%  goweb/utils.hashInternal
        29.22s  6.21%  6.25%    453.22s 96.39%  golang.org/x/crypto/pbkdf2.Key
        6.45s  1.37%  7.62%    390.41s 83.03%  crypto/hmac.(*hmac).Sum
        6.30s  1.34%  8.96%       355s 75.50%  crypto/sha256.(*digest).Sum
    ```

4. 解决过程

    baidu....,得到一篇帖子[crypto/sha256: optimize sha256 implementation #34037](https://github.com/golang/go/issues/34037)

    尝试修改，修改代码如下：
    
    ```go
    import (
        // "crypto/sha256"              // 不用这个包了
        "github.com/minio/sha256-simd"  // 改用这个
    )
    ```

    继续测试，测试结果如下,测试环境同上：

    ![](image/2023-03-26-11-10-20.png)

    此时，时间来到了55s左右

6. 解决方案

    尝试修改，修改代码如下：
    
    ```go
    import (
        // "crypto/sha256"              // 不用这个包了
        "github.com/minio/sha256-simd"  // 改用这个
    )
    ```