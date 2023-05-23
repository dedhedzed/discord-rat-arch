DIRECTORY=bin
UPX=upx.exe
MAC=macos-agent
LINUX=linux-agent
WIN=windows-agent.exe
RASP=rasp-agent
BSD=bsd-agent
FLAGS=-ldflags "-s -w"
WIN-FLAGS=-ldflags "-s -w"

all: request-permissions agent-linux agent-windows agent-mac agent-raspberrypi agent-freebsd

request-permissions:
	chmod +x bin/upx.exe

agent-mac:
	echo "Compiling MacOS binary..."
	env GOOS=darwin GOARCH=amd64 go build ${FLAGS} -o ${DIRECTORY}/${MAC} cmd/agent/main.go

	echo "Compressing MacOS binary..."
	${DIRECTORY}/${UPX} ${DIRECTORY}/${MAC}

agent-linux:
	echo "Compiling Linux binary..."
	env GOOS=linux GOARCH=amd64 go build ${FLAGS} -o ${DIRECTORY}/${LINUX} cmd/agent/main.go

	echo "Compressing Linux binary..."
	${DIRECTORY}/${UPX} ${DIRECTORY}/${LINUX}

agent-windows:
	echo "Compiling Windows binary..."
	env GOOS=windows GOARCH=amd64 go build ${WIN-FLAGS} -o ${DIRECTORY}/${WIN} cmd/agent/main.go

	echo "Compressing Windows binary..."
	${DIRECTORY}/${UPX} ${DIRECTORY}/${WIN}

agent-raspberrypi:
	echo "Compiling Raspberry Pi binary..."
	env GOOS=linux GOARCH=arm GOARM=7 go build ${FLAGS} -o ${DIRECTORY}/${RASP} cmd/agent/main.go

	echo "Compressing Raspberry Pi binary..."
	${DIRECTORY}/${UPX} ${DIRECTORY}/${RASP}

agent-freebsd:
	echo "Compiling FreeBSD binary..."
	env GOOS=freebsd GOARCH=amd64 go build ${FLAGS} -o ${DIRECTORY}/${BSD} cmd/agent/main.go

	echo "Compressing FreeBSD binary..."
	${DIRECTORY}/${UPX} ${DIRECTORY}/${BSD}
