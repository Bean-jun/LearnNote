package main

import (
	"crypto/hmac"
	// "crypto/sha256"
	"encoding/hex"
	"fmt"
	"math/rand"
	"strconv"
	"strings"
	"time"

	"github.com/minio/sha256-simd"
	"golang.org/x/crypto/pbkdf2"
)

var (
	Iterations = 260000
)

// RandomString returns a random string with a fixed length
func genSalt(n int) string {
	SaltChars := []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

	b := make([]rune, n)
	for i := range b {
		b[i] = SaltChars[rand.Intn(len(SaltChars))]
	}
	return string(b)
}

func hashInternal(salt, password string) string {
	digest := sha256.New
	ret := pbkdf2.Key([]byte(password), []byte(salt), Iterations, 32, digest)
	h := hex.EncodeToString(ret)
	return h
}

// GeneratePasswordHash 加密密码 类比werkzeug的generate_password_hash
func GeneratePasswordHash(password string) (salt, hashPassword string) {

	salt = genSalt(16)

	args := "sha256" // method := "pbkdf2:sha256"   method[7:].split(":") 即"sha256"
	method := args
	actualMethod := fmt.Sprintf("pbkdf2:%s:%s", method, strconv.Itoa(Iterations))

	h := hashInternal(salt, password)

	hashPassword = actualMethod + "$" + salt + "$" + h
	// fmt.Println(hashPassword)
	return salt, hashPassword
}

// CheckPasswordHash 检测密码
func CheckPasswordHash(hashPassword, password string) bool {

	if strings.Count(hashPassword, "$") < 2 {
		return false
	}

	ret := strings.Split(hashPassword, "$")
	hashval := ret[2]
	h := hashInternal(ret[1], password)
	result := hmac.Equal([]byte(h), []byte(hashval))
	return result
}

func main() {
	start := time.Now()
	password := "LQpgMbRFBIILcf4wF2n4"
	nums := 1024 * 1
	salt, hashPassword := GeneratePasswordHash(password)
	fmt.Println(password, salt, hashPassword)
	for i := 0; i <= nums; i++ {
		GeneratePasswordHash(password)
	}
	fmt.Println("use time:", time.Since(start))
}
