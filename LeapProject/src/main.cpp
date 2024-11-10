#include <iostream>
#include <LeapC.h>
#include <WinSock2.h> // Windows-specific for sockets
#include <ws2tcpip.h>
#include <string>

#pragma comment(lib, "ws2_32.lib") // Link Windows sockets library

LEAP_CONNECTION connection;

// Function to send data over UDP
void SendData(const std::string& data) {
    WSADATA wsa;
    SOCKET sock;
    struct sockaddr_in server;

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        std::cerr << "Failed to initialize Winsock." << std::endl;
        return;
    }

    // Create socket
    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock == INVALID_SOCKET) {
        std::cerr << "Could not create socket: " << WSAGetLastError() << std::endl;
        WSACleanup();
        return;
    }

    // Set up server address
    server.sin_family = AF_INET;
    server.sin_port = htons(65432); // Port to send data to
    inet_pton(AF_INET, "127.0.0.1", &server.sin_addr); // Localhost

    // Send data
    sendto(sock, data.c_str(), data.size(), 0, (struct sockaddr*)&server, sizeof(server));

    // Clean up
    closesocket(sock);
    WSACleanup();
}

// Leap Motion frame callback
void OnFrame(const LEAP_TRACKING_EVENT* frame) {
    if (frame->nHands > 0) {
        const LEAP_HAND* hand = &frame->pHands[0];
        float handX = hand->palm.position.x;
        float grabStrength = hand->grab_strength;

        // Prepare JSON data with hand position and shoot status
        std::string data = "{\"x\": " + std::to_string(handX);
        if (grabStrength > 0.8) {  // Adjust threshold as needed
            data += ", \"shoot\": true";
        } else {
            data += ", \"shoot\": false";
        }
        data += "}";

        SendData(data);
    }
}

// Main function
int main() {
    // Initialize Leap Motion connection
    if (LeapCreateConnection(nullptr, &connection) == eLeapRS_Success) {
        if (LeapOpenConnection(connection) == eLeapRS_Success) {
            std::cout << "Connected to Leap Motion service." << std::endl;

            LEAP_CONNECTION_MESSAGE msg;
            while (true) {
                LeapPollConnection(connection, 1000, &msg);
                if (msg.type == eLeapEventType_Tracking) {
                    OnFrame(msg.tracking_event);
                } else {
                    std::cout << "No tracking event in this message." << std::endl;
                }
            }
        } else {
            std::cerr << "Failed to open Leap Motion connection." << std::endl;
        }
    } else {
        std::cerr << "Failed to create Leap Motion connection." << std::endl;
    }

    // Clean up Leap Motion connection
    LeapDestroyConnection(connection);
    return 0;
}
