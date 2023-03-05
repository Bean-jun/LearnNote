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
