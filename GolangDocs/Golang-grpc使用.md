# go中grpc的使用

### 1. install go
### 2. install protocol buffer compiler [here](https://grpc.io/docs/protoc-installation/)
### 3. install go plugins

```shell
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2
```
### 4. write proto file

```protobuf
syntax = "proto3";

// 解析为go可调用包 可选用参数
option go_package = ".;helloworld";

// 定义服务
service RouteGuide {
    // 定义方法 普通模式
    rpc GetFeature(Point) returns (Feature) {}
    // 服务端流模式 服务端向客户端推流
    rpc GetServeStream(Point) returns (stream Feature){}
    // 客户端流模式 客户端向服务端推流
    rpc PutServeStream(stream Point) returns (Feature){}
    // 双向流模式 服务端客户端双向推流
    rpc AllServeStream(stream Point) returns (stream Feature){}
}

message Point {
    int32 x = 1;
    int32 y = 2;
}

message Feature {
    int32 z = 3;
}
```

### 5. compiler 

`protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative xxxx/xxx.proto`

### 6. 编辑server

```go
// GolangDocs/src/grpc/server/server.go
package main

import (
    "context"
    "fmt"
    "gogrpctoturial/helloworld"
    "google.golang.org/grpc"
    "net"
    "sync"
    )

type Server struct {
    helloworld.UnimplementedRouteGuideServer
}

// GetFeature 普通模式
func (s Server) GetFeature(ctx context.Context, point *helloworld.Point) (*helloworld.Feature, error) {
    val := point.GetX() + point.GetY()
    return &helloworld.Feature{Z: val}, nil
}

// GetServeStream 服务端流模式
    func (s Server) GetServeStream(point *helloworld.Point, serverStr helloworld.RouteGuide_GetServeStreamServer) error {
    val := point.GetX() + point.GetY()
    for i := 0; i < 10; i++ {
        val += int32(i)
        err := serverStr.Send(&helloworld.Feature{Z: val})
        if err != nil {
            return err
        }
    }
    return nil
}

// PutServeStream 客户端流模式
    func (s Server) PutServeStream(clientStr helloworld.RouteGuide_PutServeStreamServer) error {
    for {
        recv, err := clientStr.Recv()
        if err != nil {
            break
        }
        fmt.Printf("客户端流模式 current point x:%d y:%d\n", recv.GetX(), recv.GetY())
    }
    return nil
}

// AllServeStream 双向流模式
func (s Server) AllServeStream(allStr helloworld.RouteGuide_AllServeStreamServer) error {
    var wg = sync.WaitGroup{}
    wg.Add(2)

    // recv
    go func() {
        for {
            recv, err := allStr.Recv()
            if err != nil {
                break
            }
            fmt.Printf("双向流模式 current point x:%d y:%d\n", recv.GetX(), recv.GetY())
        }
    }()

    // send
    go func() {
        for i := 0; i < 10; i++ {
            err := allStr.Send(&helloworld.Feature{Z: int32(i)})
            if err != nil {
                break
            }
        }
    }()
    wg.Wait()
    return nil
}

func main() {
    g := grpc.NewServer()
    helloworld.RegisterRouteGuideServer(g, &Server{})
    listen, err := net.Listen("tcp", ":8080")
    if err != nil {
        fmt.Println(err)
        return
    }
    err = g.Serve(listen)
    if err != nil {
        return
    }
}
```

### 7. 编辑client

```go
// GolangDocs/src/grpc/client/client.go
package main

import (
    "context"
    "fmt"
    "gogrpctoturial/helloworld"
    "google.golang.org/grpc"
    "sync"
    )

func main() {
    conn, err := grpc.Dial("127.0.0.1:8080", grpc.WithInsecure())
    if err != nil {
        fmt.Println(err.Error())
        return
    }
    defer conn.Close()

    c := helloworld.NewRouteGuideClient(conn)

    // 普通模式
    feature, err := c.GetFeature(context.Background(), &helloworld.Point{
        X: 12,
        Y: 22,
    })
    if err != nil {
        return
    }
    fmt.Println(feature.GetZ())

    // 服务端流模式
    Serverstream, err := c.GetServeStream(context.Background(), &helloworld.Point{
        X: 100,
        Y: 2,
    })
    if err != nil {
        return
    }
    for i := 0; i < 10; i++ {
        recv, err := Serverstream.Recv()
        if err != nil {
            break
        }
        fmt.Printf("服务端流模式 current point feature value: %d\n", recv.GetZ())
    }

    // 客户端流模式
    Clientstream, err := c.PutServeStream(context.Background())
    if err != nil {
        return
    }
    for i := 0; i < 10; i++ {
        err := Clientstream.Send(&helloworld.Point{
            X: int32(i),
            Y: 1,
        })
        if err != nil {
            break
        }
    }

    // 双向流模式
    Allstream, err := c.AllServeStream(context.Background())
    if err != nil {
        return
    }
    var wg = sync.WaitGroup{}
    wg.Add(2)

    // recv
    go func() {
        defer wg.Done()
        for {
            recv, err := Allstream.Recv()
            if err != nil {
                break
            }
            fmt.Printf("双向流模式 current point feature value: %d\n", recv.GetZ())
        }
    }()

    // send
    go func() {
        defer wg.Done()
        for i := 0; i < 10; i++ {
            err := Allstream.Send(&helloworld.Point{
                X: int32(i),
                Y: 7,
            })
            if err != nil {
                break
            }
        }
    }()
    wg.Wait()
}
```
