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
	"fmt"
	"os"
	"runtime"
)

// The current working directory the agent is running at.
// This will change when the cd command is used.
var CurrentDirectory = GetCurrentDirectory()

// GetCurrentDirectory retrieves the current working directory and will
// return "Unknown" if it fails to do so.
func GetCurrentDirectory() string {
	// Get the current working directory.
	directory, err := os.Getwd()
	if err != nil {
		return "Unknown"
	}

	return directory
}

// GetFormattedPlatform utilizes runtime.GOOS to return a formatted version of
// the current operating system platform.
func GetFormattedPlatform() string {
	// Format the raw system string to a more presentable version.
	switch runtime.GOOS {
	case "windows":
		return "Windows"
	case "linux":
		return "Linux"
	case "darwin":
		return "MacOS"
	}

	return fmt.Sprintf("Unknown (%s)", runtime.GOOS)
}
