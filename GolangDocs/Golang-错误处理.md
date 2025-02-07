1. 介绍

在 Go 语言中，错误处理是编写健壮程序的重要组成部分。Go 语言没有传统意义上的异常机制，而是通过函数返回值来传递错误信息。

2. 基本错误处理

在 Go 中，函数通常会返回两个值：结果值和错误值。如果错误值为`nil`，表示操作成功；否则表示操作失败。


2.1 示例代码

```go
package main

import (
	"errors"
	"fmt"
)

// divide 函数返回两个值：结果和错误
func divide(a, b int) (int, error) {
	if b == 0 {
		// 返回错误信息
		return 0, errors.New("division by zero")
	}
	return a / b, nil
}

func main() {
	result, err := divide(10, 0)
	if err != nil {
		fmt.Println("Error:", err)
	} else {
		fmt.Println("Result:", result)
	}
}
```



2.2 运行结果

```
Error: division by zero
```



3. 自定义错误

Go 允许通过实现`error`接口来自定义错误类型。这使得我们可以更灵活地处理错误，例如添加额外的上下文信息。


3.1 示例代码

```go
package main

import (
	"fmt"
)

// 自定义错误类型
type MyError struct {
	Code    int
	Message string
}

// 实现 error 接口
func (e *MyError) Error() string {
	return fmt.Sprintf("Error %d: %s", e.Code, e.Message)
}

func doSomething() error {
	return &MyError{Code: 404, Message: "Resource not found"}
}

func main() {
	err := doSomething()
	if err != nil {
		fmt.Println(err)
	}
}
```



3.2 运行结果

```
Error 404: Resource not found
```



4. 错误链

在复杂的程序中，错误可能发生在多个层级。为了更好地跟踪错误的上下文，Go 提供了错误链机制。通过`%w`格式化符，可以将错误包装起来，形成一个错误链。


4.1 使用`%w`格式化符
从 Go 1.13 开始，`fmt.Errorf`支持`%w`格式化符，用于包装错误。


示例代码

```go
package main

import (
	"errors"
	"fmt"
)

func foo() error {
	return errors.New("foo error")
}

func bar() error {
	err := foo()
	if err != nil {
		return fmt.Errorf("bar error: %w", err)
	}
	return nil
}

func main() {
	err := bar()
	if err != nil {
		fmt.Println(err)
	}
}
```



运行结果

```
bar error: foo error
```



4.2 使用`errors.Is`和`errors.As`

`errors.Is`和`errors.As`是用于处理错误链的两个重要函数。

`errors.Is`：用于检查一个错误是否等于另一个错误，或者是否包裹了另一个错误。它会深度优先遍历错误链（通过   Unwrap   方法），检查链中的每个错误是否与目标错误相等。

`errors.As`： 用于检查一个错误是否可以转换为某种特定类型的错误，并将该错误赋值给目标变量。它会遍历错误链，查找是否有匹配的错误类型。


示例代码

```go
package main

import (
	"errors"
	"fmt"
)

func foo() error {
	return errors.New("foo error")
}

func bar() error {
	err := foo()
	if err != nil {
		return fmt.Errorf("bar error: %w", err)
	}
	return nil
}

func main() {
	err := bar()
	if err != nil {
		if errors.Is(err, errors.New("foo error")) {
			fmt.Println("Foo error found")
		}
		var myErr *MyError
		if errors.As(err, &myErr) {
			fmt.Println("MyError found:", myErr.Message)
		}
	}
}
```



运行结果

```
Foo error found
```

4.3 使用场景

`errors.Is`的使用场景

当你需要判断一个错误是否是某个特定错误时，例如检查文件是否不存在（  os.ErrNotExist  ）。

适用于简单的错误匹配场景。

`errors.As`的使用场景

当你需要获取错误的具体类型，以便进行进一步处理时，例如获取   os.PathError   的详细信息。

适用于需要对错误进行类型断言的场景。

5. `errors.Join`

`errors.Join`函数可以将多个错误组合成一个错误对象。这在需要同时报告多个错误时非常方便。


5.1 示例代码

```go
package main

import (
	"errors"
	"fmt"
)

func main() {
	err1 := errors.New("error 1")
	err2 := errors.New("error 2")
	err3 := errors.New("error 3")

	// 使用 errors.Join 组合多个错误
	combinedErr := errors.Join(err1, err2, err3)

	// 打印组合后的错误
	fmt.Println("Combined Error:", combinedErr)

	// 使用 errors.Is 检查组合错误中是否包含某个特定错误
	if errors.Is(combinedErr, err1) {
		fmt.Println("Combined error contains error 1")
	}
	if errors.Is(combinedErr, err2) {
		fmt.Println("Combined error contains error 2")
	}
	if errors.Is(combinedErr, err3) {
		fmt.Println("Combined error contains error 3")
	}

	// 使用 errors.Unwrap 获取所有原始错误
	if unwrappedErrs, ok := errors.Unwrap(combinedErr).([]error); ok {
		fmt.Println("Unwrapped Errors:", unwrappedErrs)
	}
}
```



5.2 运行结果

```
Combined Error: error 1
error 2
error 3
Combined error contains error 1
Combined error contains error 2
Combined error contains error 3
Unwrapped Errors: [error 1 error 2 error 3]
```



6. `panic`和`recover`

`panic`和`recover`是 Go 中用于处理不可恢复错误的机制。`panic`用于触发程序崩溃，而`recover`用于捕获`panic`，防止程序崩溃。


6.1 示例代码

```go
package main

import "fmt"

func mayPanic() {
	panic("Something went wrong!")
}

func main() {
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("Recovered from panic:", r)
		}
	}()
	mayPanic()
	fmt.Println("This will not be printed if panic is not recovered")
}
```



6.2 运行结果

```
Recovered from panic: Something went wrong!
```


7. 小结

Go 语言的错误处理机制虽然简单，但非常灵活和强大。通过合理使用基本错误处理、自定义错误、错误链以及`panic`和`recover`，可以编写出健壮且易于维护的代码。以下是一些最佳实践：

避免冗余的错误检查：使用`%w`格式化符时，无需手动检查错误是否为`nil`。

使用自定义错误类型：自定义错误类型可以携带更多上下文信息，便于调试和日志记录。

合理使用错误链：通过`errors.Join`和`errors.Unwrap`，可以方便地组合和解构多个错误。

谨慎使用`panic`和`recover`：`panic`和`recover`通常用于处理不可恢复的错误，避免滥用。
