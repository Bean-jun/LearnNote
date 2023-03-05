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
