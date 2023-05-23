/*
 * This file is part of the Discord-RAT project.
 * Repository: https://github.com/codeuk/discord-rat
 *
 * Written by codeuk (github.com/codeuk)
 *
 * Discord-RAT is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Discord-RAT is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Discord-RAT. If not, see <https://www.gnu.org/licenses/>.
 */
package system

import (
	"os/exec"
	"runtime"
)

// ExecuteCommand executes a command on the current system and returns its output.
func ExecuteCommand(command string) string {
	var shell, flag string

	// Allow ExecuteCommand to be used cross-platform by changing the commands shell
	// and flags to suit the current machines operating system.
	if runtime.GOOS == "windows" {
		shell = WIN_SHELL
		flag = WIN_FLAG
	} else {
		shell = NIX_SHELL
		flag = NIX_FLAG
	}

	// Execute the passed command with the appropriate shell and flags for the operating system.
	outputBytes, _ := exec.Command(shell, flag, command).Output()

	return string(outputBytes)
}

// Default command shell values for different operating systems
const (
	WIN_SHELL = "cmd"
	NIX_SHELL = "/bin/sh"
)

// Default command flag values for different operating systems
const (
	WIN_FLAG = "/c"
	NIX_FLAG = "-c"
)
