ReleaseBin="shortUrl.exe"

build: clear
	go build -o ${ReleaseBin}

clear:
	del *.exe

run:
	go run main.go

runb: build
	${ReleaseBin}