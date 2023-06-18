DIRECTORY=bin
UPX=upx
MAC=macos-agent
LINUX=linux-agent
WIN=windows-agent
RASP=rasp-agent
BSD=bsd-agent
FLAGS=-ldflags "-s -w"
WIN-FLAGS=-ldflags "-s -w"

all: request-upx agent-mac agent-linux agent-windows agent-raspberrypi agent-freebsd

request-upx:
	@echo "[+] Installing the UPX package..."
	sudo pacman -S upx;

agent-mac:
	clear
	@echo "[1/5] Compiling MacOS binary..."
	@env GOOS=darwin GOARCH=amd64 go build ${FLAGS} -o ${DIRECTORY}/${MAC} cmd/agent/main.go
	@if [ -x $$(command -v ${UPX}) ]; then \
		echo "[1/5] Compressing MacOS binary..."; \
		${UPX} ${DIRECTORY}/${MAC}; \
	fi

agent-linux:
	clear
	@echo "[2/5] Compiling Linux binary..."
	@env GOOS=linux GOARCH=amd64 go build ${FLAGS} -o ${DIRECTORY}/${LINUX} cmd/agent/main.go
	@if [ -x $$(command -v ${UPX}) ]; then \
		echo "[2/5] Compressing Linux binary..."; \
		${UPX} ${DIRECTORY}/${LINUX}; \
	fi

agent-windows:
	clear
	@echo "[3/5] Compiling Windows binary..."
	@env GOOS=windows GOARCH=amd64 go build ${WIN-FLAGS} -o ${DIRECTORY}/${WIN}.exe cmd/agent/main.go
	@if [ -x $$(command -v ${UPX}) ]; then \
		echo "[3/5] Compressing Windows binary..."; \
		${UPX} ${DIRECTORY}/${WIN}.exe; \
	fi

agent-raspberrypi:
	clear
	@echo "[4/5] Compiling Raspberry Pi binary..."
	@env GOOS=linux GOARCH=arm GOARM=7 go build ${FLAGS} -o ${DIRECTORY}/${RASP} cmd/agent/main.go
	@if [ -x $$(command -v ${UPX}) ]; then \
		echo "[4/5] Compressing Raspberry Pi binary..."; \
		${UPX} ${DIRECTORY}/${RASP}; \
	fi

agent-freebsd:
	clear
	@echo "[5/5] Compiling FreeBSD binary..."
	@env GOOS=freebsd GOARCH=amd64 go build ${FLAGS} -o ${DIRECTORY}/${BSD} cmd/agent/main.go
	@echo "[5/5] Compression for FreeBSD binaries is disabled..."
