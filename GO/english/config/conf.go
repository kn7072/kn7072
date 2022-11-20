package config

import (
	"log"

	"github.com/spf13/viper"
)

type Reader interface {
	GetAllKeys() []string
	Get(key string) interface{}
	GetBool(key string) bool
	GetString(key string) string
}

type viperConfigReader struct {
	viper *viper.Viper
}

var ConfReader *viperConfigReader

func (v *viperConfigReader) GetAllKeys() []string {
	return v.viper.AllKeys()
}

func (v *viperConfigReader) Get(key string) interface{} {
	return v.viper.Get(key)
}

func (v *viperConfigReader) GetBool(key string) bool {
	return v.viper.GetBool(key)
}

func (v *viperConfigReader) GetString(key string) string {
	return v.viper.GetString(key)
}

func (v *viperConfigReader) GetViper() *viper.Viper {
	return v.viper
}

func (v *viperConfigReader) GetInt(key string) int {
	return v.viper.GetInt(key)
}

func init() {
	v := viper.New()
	// v.SetConfigName("config.yaml")
	// v.AddConfigPath("./config/")
	v.SetConfigFile("./config/config.yaml")
	err := v.ReadInConfig()

	if err != nil {
		log.Panic("Not able to read configuration", err.Error())
	}

	ConfReader = &viperConfigReader{
		viper: v,
	}
}