//go:build windows
// +build windows

package platforms

import "syscall"

// HideConsole hides the applications console window using the WinAPI.
func HideConsole() {
	// Get the window handle of the current application/console window.
	getWin := syscall.NewLazyDLL("kernel32.dll").NewProc("GetConsoleWindow")
	hwnd, _, _ := getWin.Call()

	// Check if the window handle returned is valid.
	if hwnd != 0 {
		// Call the ShowWindowAsync with the parameter 0, as opposed to 1 which
		showWindowAsync := syscall.NewLazyDLL("user32.dll").NewProc("ShowWindowAsync")
		showWindowAsync.Call(hwnd, 0)
	}
}
