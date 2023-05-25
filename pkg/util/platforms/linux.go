//go:build linux
// +build linux

package platforms

import (
	"os"
	"syscall"
)

// HideConsole hides the applications console window using linux syscalls.
func HideConsole() {
	// Get the file descriptor for the current console window.
	fd := int(os.Stdout.Fd())

	// Hide the console window by setting the flag to zero.
	_, _, _ = syscall.Syscall(
		syscall.SYS_IOCTL,
		uintptr(fd),
		uintptr(syscall.TIOCCONS),
		0,
	)
}
