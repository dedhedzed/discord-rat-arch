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
package agent

import (
	"os"

	"github.com/codeuk/discord-rat/pkg/agent/system"
)

// Agent represents a single target.
type Agent struct {
	HostName   string
	OS         string
	LocalIP    string
	ExternalIP string
	Status     string
	Timestamp  string
}

// NewAgent configures and returns a new Agent containing the current systems information.
func NewAgent() *Agent {
	agent := &Agent{}
	agent.HostName, _ = os.Hostname()
	agent.LocalIP = system.GetLocalIP()
	agent.ExternalIP = system.GetExternalIP()
	agent.OS = system.GetFormattedPlatform()

	return agent
}
