package main

import (
	"log"
	"net"
	"net/rpc"
)

/*
   定义一个serviceA 给其他client调用
*/
// 定义参数
type Args struct {
	X, Y int
}
package main

    import (
        "log"
        "net"
        "net/rpc"
        "net/rpc/jsonrpc"
    )

    /*
    定义一个serviceA 给其他client调用
    */
    // 定义参数
    type Args struct {
        X, Y int
    }

    // serviceA 服务
    type ServiceA struct{}

    // 自定义方法 要求 func(x interface, reply *ponit) error
    func (s *ServiceA) Add(args *Args, reply *int) error {
        // reply 必须是一个指针
        *reply = args.X + args.Y
        return nil
    }

    // rpc 包默认使用的是gob协议对传输数据进行序列化/反序列化
    func main() {
        service := new(ServiceA)
        // 注册RPC服务
        rpc.Register(service)

        // 设置RPC协议
        listen, err := net.Listen("tcp", ":9000")
        if err != nil {
            log.Fatal(err)
        }
        for {
            conn, _ := listen.Accept()
            // 使用golang原始的gob协议
            // rpc.ServeConn(conn)

            // 使用JSON协议
            rpc.ServeCodec(jsonrpc.NewServerCodec(conn))
        }
    }
// serviceA 服务
type ServiceA struct{}

// 自定义方法 要求 func(x interface, reply *ponit) error
func (s *ServiceA) Add(args *Args, reply *int) error {
	// reply 必须是一个指针
	*reply = args.X + args.Y
	return nil
}

// rpc 包默认使用的是gob协议对传输数据进行序列化/反序列化
func main() {
	service := new(ServiceA)
	// 注册RPC服务
	rpc.Register(service)

	listen, err := net.Listen("tcp", ":9000")
	if err != nil {
		log.Fatal(err)
	}
	for {
		conn, _ := listen.Accept()
		// 使用golang原始的gob协议
		rpc.ServeConn(conn)
	}
}
