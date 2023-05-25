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
	"strconv"
	"strings"

	"github.com/bwmarrin/discordgo"
)

// BotMessage represents the Messages parent Session and Message attributes.
type BotMessage struct {
	Session *discordgo.Session
	Message *discordgo.MessageCreate
}

func HandlePing(message *BotMessage) {
	// Simple message to show that the Bot is still connected and listening.
	message.Session.ChannelMessageSend(message.Message.ChannelID, "I'm alive!")
}

func HandlePurge(message *BotMessage) {
	// Purge a certain amount of messages.
	commandBreakdown := strings.Fields(message.Message.Content)

	if len(commandBreakdown) == 2 {
		// Parse the integer amount of messages to purge from the command.
		purgeAmountStr := commandBreakdown[1]
		purgeAmount, err := strconv.Atoi(purgeAmountStr)
		if err != nil {
			// Couldn't bulk purge the messages.
			message.Session.ChannelMessageSend(message.Message.ChannelID, fmt.Sprintf("**Failed to purge %d messages!**", purgeAmount))
			return
		}

		// Check if we have exceeded the maximum purge amount and adjust accordingly.
		if purgeAmount > PURGE_LIMIT {
			// Purge amount is over the maximum.
			message.Session.ChannelMessageSend(message.Message.ChannelID, fmt.Sprintf("**Exceeded the purge limit! Purging %d instead...**", PURGE_LIMIT))

			// Reset the purge amount to the maximum
			purgeAmount = PURGE_LIMIT
		}

		messagesToDelete := []string{}

		// Iterate through the last x messages (purgeAmount).
		st, _ := message.Session.ChannelMessages(message.Message.ChannelID, purgeAmount, "", "", "")
		for _, s := range st {
			messagesToDelete = append(messagesToDelete, s.ID)
		}

		// Delete the collected messages in bulk.
		if err = message.Session.ChannelMessagesBulkDelete(message.Message.ChannelID, messagesToDelete); err != nil {
			// Couldn't bulk purge the messages.
			message.Session.ChannelMessageSend(message.Message.ChannelID, fmt.Sprintf("**Failed to purge %d messages!**", purgeAmount))
			return
		}

		// Messages were purged successfully.
		message.Session.ChannelMessageSend(message.Message.ChannelID, fmt.Sprintf("**Successfully purged %d messages!**", purgeAmount))
	} else {
		// Invalid delete command syntax.
		message.Session.ChannelMessageSend(message.Message.ChannelID, "**Command usage** ```purge <amount of messages> \nExample: \"purge 100\"```")
	}
}

// Limit on how many messages can be purged at a time.
const PURGE_LIMIT = 100
