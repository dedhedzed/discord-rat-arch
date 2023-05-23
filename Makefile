DIRECTORY=bin
UPX=upx.exe
MAC=macos-agent
LINUX=linux-agent
WIN=windows-agent.exe
RASP=rasp-agent
BSD=bsd-agent
FLAGS=-ldflags "-s -w"
WIN-FLAGS=-ldflags "-s -w"

all: request-permissions agent-mac agent-linux agent-windows agent-raspberrypi agent-freebsd

request-permissions:
	@chmod +x bin/upx.exe

agent-mac:
	$(info [1/5] Compiling MacOS binary...)
	@env GOOS=darwin GOARCH=amd64 go build ${FLAGS} -o ${DIRECTORY}/${MAC} cmd/agent/main.go

	$(info [1/5] Compressing MacOS binary...)
	${DIRECTORY}/${UPX} ${DIRECTORY}/${MAC}

agent-linux:
	$(info [2/5] Compiling Linux binary...)
	@env GOOS=linux GOARCH=amd64 go build ${FLAGS} -o ${DIRECTORY}/${LINUX} cmd/agent/main.go

	$(info [2/5] Compressing Linux binary...)
	${DIRECTORY}/${UPX} ${DIRECTORY}/${LINUX}

agent-windows:
	$(info [3/5] Compiling Windows binary...)
	@env GOOS=windows GOARCH=amd64 go build ${WIN-FLAGS} -o ${DIRECTORY}/${WIN} cmd/agent/main.go

	$(info [3/5] Compressing Windows binary...)
	${DIRECTORY}/${UPX} ${DIRECTORY}/${WIN}

agent-raspberrypi:
	$(info [4/5] Compiling Raspberry Pi binary...)
	@env GOOS=linux GOARCH=arm GOARM=7 go build ${FLAGS} -o ${DIRECTORY}/${RASP} cmd/agent/main.go

	$(info [4/5] Compressing Raspberry Pi binary...)
	${DIRECTORY}/${UPX} ${DIRECTORY}/${RASP}

agent-freebsd:
	$(info [5/5] Compiling FreeBSD binary...)
	@env GOOS=freebsd GOARCH=amd64 go build ${FLAGS} -o ${DIRECTORY}/${BSD} cmd/agent/main.go

	$(info [5/5] Compression for FreeBSD binaries is disabled...)
