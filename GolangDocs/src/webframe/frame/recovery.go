package frame

import (
	"fmt"
	"log"
	"runtime"
	"strings"
)

func trace(err string) string {
	var pcs [32]uintptr
	n := runtime.Callers(3, pcs[:]) // skip first 3 caller
	var str strings.Builder
	str.WriteString(err + "\nTraceback:")
	for _, pc := range pcs[:n] {
		fn := runtime.FuncForPC(pc)
		file, line := fn.FileLine(pc)
		str.WriteString(fmt.Sprintf("\n\t%s:%d", file, line))
	}
	return str.String()
}

// Recovery 捕获异常
func Recovery() HandlerFunc {
	return func(c *Context) {
		defer func() {
			if err := recover(); err != nil {
				msg := trace(fmt.Sprintf("%s", err))
				log.Printf("%s\n\n", msg)
			}
		}()
		c.Next()
	}
}
