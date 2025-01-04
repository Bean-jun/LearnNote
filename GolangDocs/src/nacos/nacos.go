package server

import (
	"bytes"
	"encoding/json"
	"log"
	"strconv"
	"strings"

	"github.com/nacos-group/nacos-sdk-go/v2/clients"
	"github.com/nacos-group/nacos-sdk-go/v2/clients/config_client"
	"github.com/nacos-group/nacos-sdk-go/v2/clients/naming_client"
	"github.com/nacos-group/nacos-sdk-go/v2/common/constant"
	"github.com/nacos-group/nacos-sdk-go/v2/model"
	"github.com/nacos-group/nacos-sdk-go/v2/vo"
	"github.com/spf13/viper"
)

func getNacosServerUrl() []string {
	nacosUrlSclice := make([]string, 0)
	nacosUrl := viper.GetString("nacos.server")
	if strings.Contains(nacosUrl, ";") {
		nacosUrlSclice = strings.Split(nacosUrl, ";")
	} else {
		nacosUrlSclice = append(nacosUrlSclice, nacosUrl)
	}
	return nacosUrlSclice
}

func getNacosConfig() (constant.ClientConfig, []constant.ServerConfig) {
	// 创建clientConfig
	clientConfig := constant.ClientConfig{
		TimeoutMs:           5000,
		NotLoadCacheAtStart: true,
		LogDir:              "/tmp/nacos/log",
		CacheDir:            "/tmp/nacos/cache",
		LogLevel:            "warn",
	}

	// 至少一个ServerConfig
	serverConfigs := make([]constant.ServerConfig, 0)
	for _, addr := range getNacosServerUrl() {
		ipPort := strings.Split(addr, ":")
		if len(ipPort) != 2 {
			continue
		}
		port, _ := strconv.Atoi(ipPort[1])
		serverConfigs = append(serverConfigs, constant.ServerConfig{
			IpAddr:      ipPort[0],
			ContextPath: "/nacos",
			Port:        uint64(port),
		})
	}
	return clientConfig, serverConfigs
}

// GetNacosNamingClient 获取Nacos服务发现客户端
func GetNacosNamingClient() (naming_client.INamingClient, error) {
	clientConfig, serverConfigs := getNacosConfig()
	// 创建服务发现客户端
	return clients.CreateNamingClient(map[string]interface{}{
		"serverConfigs": serverConfigs,
		"clientConfig":  clientConfig,
	})
}

// GetNacosConfigClient 获取Nacos动态配置客户端
func GetNacosConfigClient() (config_client.IConfigClient, error) {
	clientConfig, serverConfigs := getNacosConfig()
	// 创建服务发现客户端
	return clients.CreateConfigClient(map[string]interface{}{
		"serverConfigs": serverConfigs,
		"clientConfig":  clientConfig,
	})
}

// RegisterService2Nacos 注册服务至Nacos
func RegisterService2Nacos(ip string, port uint64, endpoint string, metadata map[string]string) (bool, error) {
	client, err := GetNacosNamingClient()
	if err != nil {
		return false, err
	}

	return client.RegisterInstance(vo.RegisterInstanceParam{
		Ip:          ip,
		Port:        port,
		ServiceName: endpoint,
		Weight:      10,
		Enable:      true,
		Healthy:     true,
		Ephemeral:   true,
		Metadata:    metadata,
		GroupName:   endpoint,
	})
}

// UnRegisterService2Nacos 从Nacos中注销服务
func UnRegisterService2Nacos(ip string, port uint64, endpoint string) (bool, error) {
	client, err := GetNacosNamingClient()
	if err != nil {
		return false, err
	}

	return client.DeregisterInstance(vo.DeregisterInstanceParam{
		Ip:          ip,
		Port:        port,
		ServiceName: endpoint,
		Ephemeral:   true,
		GroupName:   endpoint,
	})
}

// GetServiceNacos 获取健康可用的服务对象
func GetServiceNacos(endpoint string) ([]model.Instance, error) {
	client, err := GetNacosNamingClient()
	if err != nil {
		return nil, err
	}
	return client.SelectInstances(vo.SelectInstancesParam{
		ServiceName: endpoint,
		GroupName:   endpoint,
		HealthyOnly: true,
	})
}

// SubscribeServiceNacos 监听Nacos服务
func SubscribeServiceNacos(endpoint string, callback func(services []model.Instance, err error)) error {
	client, err := GetNacosNamingClient()
	if err != nil {
		return err
	}
	param := &vo.SubscribeParam{
		ServiceName:       endpoint,
		GroupName:         endpoint,
		SubscribeCallback: callback,
	}
	return client.Subscribe(param)
}

// UnSubscribeServiceNacos 取消监听Nacos服务
func UnSubscribeServiceNacos(endpoint string, callback func(services []model.Instance, err error)) error {
	client, err := GetNacosNamingClient()
	if err != nil {
		return err
	}
	return client.Unsubscribe(&vo.SubscribeParam{
		ServiceName:       endpoint,
		GroupName:         endpoint,
		SubscribeCallback: callback,
	})
}

// GetConfigByNacos 获取nacos配置
func GetConfigByNacos(endpoint string) (string, error) {
	client, err := GetNacosConfigClient()
	if err != nil {
		return "", err
	}
	content, err := client.GetConfig(vo.ConfigParam{
		DataId: endpoint,
		Group:  endpoint})
	return content, nil
}

// PublicConfig2Nacos 发布配置文件至nacos
func PublicConfig2Nacos(endpoint string, metadata map[string]string) (bool, error) {
	client, err := GetNacosConfigClient()
	if err != nil {
		return false, err
	}
	dataBytes, err := json.Marshal(metadata)
	if err != nil {
		return false, err
	}
	return client.PublishConfig(vo.ConfigParam{
		DataId:  endpoint,
		Group:   endpoint,
		Content: string(dataBytes),
	})
}

// DeleteConfigByNacos 删除nacos配置文件
func DeleteConfigByNacos(endpoint string) (bool, error) {
	client, err := GetNacosConfigClient()
	if err != nil {
		return false, err
	}
	return client.DeleteConfig(vo.ConfigParam{
		DataId: endpoint,
		Group:  endpoint,
	})
}

// ListenConfigByNacos 监听nacos配置变化
func ListenConfigByNacos(endpoint string, callback func(namespace, group, dataId, data string)) error {
	client, err := GetNacosConfigClient()
	if err != nil {
		return err
	}
	return client.ListenConfig(vo.ConfigParam{
		DataId:   endpoint,
		Group:    endpoint,
		OnChange: callback,
	})
}

// UnListenConfigByNacos 取消监听nacos配置变化
func UnListenConfigByNacos(endpoint string) error {
	client, err := GetNacosConfigClient()
	if err != nil {
		return err
	}
	return client.CancelListenConfig(vo.ConfigParam{
		DataId: endpoint,
		Group:  endpoint,
	})
}

/*
------------------------------------------------------------------
		基于nacos动态配置
------------------------------------------------------------------
*/

func InitNacosDynamicConfig(endpoint string) {
	config, err := GetConfigByNacos(endpoint)
	if err != nil {
		log.Println("fetch remote config failed：", err.Error())
		panic(err)
	}
	err = viper.ReadConfig(bytes.NewBufferString(config))
	if err != nil {
		log.Println("parse remote config failed：", err.Error())
		panic(err)
	}

	err = ListenConfigByNacos(endpoint, func(namespace, group, dataId, data string) {
		log.Printf("listen config change: namespace: %s, group: %s, dataId: %s, data: \n%s\n", namespace, group, dataId, data)
		err := viper.ReadConfig(bytes.NewBufferString(data))
		if err != nil {
			log.Println("parse remote new config failed：", err.Error())
			panic(err)
		}
	})
	if err != nil {
		log.Println("listen remote config failed：", err.Error())
		panic(err)
	}
}
