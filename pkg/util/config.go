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
package util

// Whether to delete the agents Discord channel after exiting the program or not.
// If set to false, the Bot will archive the agents now-old command channel (#channel -> #archive-channel).
var DeleteOnExit bool = false

// Server to create the agent logs in (I suggest you make the server private).
var ServerID = "XXXXXXXXXXXXXXXXXXX"

// The token for the Bot used to communicate through.
//
// Here are the permissions that you will have to give your bot in your Discord Developer Portal:
//   - Send Messages
//   - Read Messages
//   - Attach Files
//   - Manage Server
var BotToken = "XXXXXXXXXXXXXXXXXXXXXXXXXX.XXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
