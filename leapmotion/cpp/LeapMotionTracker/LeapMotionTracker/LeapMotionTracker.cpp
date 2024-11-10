#include <iostream>
#include <LeapC.h>
#include <WinSock2.h>
#include <WS2tcpip.h>  // For InetPtonA
#include <string>
#include <thread>
#pragma comment(lib, "ws2_32.lib")  // Link Winsock library

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 8080

void sendPositionAndGrabStrength(float xPosition, float grabStrength) {
    WSADATA wsa;
    SOCKET sock;
    struct sockaddr_in server;

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        std::cerr << "Failed to initialize Winsock. Error Code: " << WSAGetLastError() << std::endl;
        return;
    }

    // Create socket
    if ((sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == INVALID_SOCKET) {
        std::cerr << "Could not create socket. Error Code: " << WSAGetLastError() << std::endl;
        WSACleanup();
        return;
    }

    // Setup server address
    server.sin_family = AF_INET;
    server.sin_port = htons(SERVER_PORT);
    if (InetPtonA(AF_INET, SERVER_IP, &server.sin_addr) <= 0) {  // Use InetPtonA for ANSI string
        std::cerr << "Invalid IP address. Error Code: " << WSAGetLastError() << std::endl;
        closesocket(sock);
        WSACleanup();
        return;
    }

    // Format the message with xPosition and grabStrength
    std::string message = std::to_string(xPosition) + "," + std::to_string(grabStrength);
    if (sendto(sock, message.c_str(), static_cast<int>(message.size()), 0, (struct sockaddr*)&server, sizeof(server)) == SOCKET_ERROR) {
        std::cerr << "Failed to send data. Error Code: " << WSAGetLastError() << std::endl;
    }

    closesocket(sock);
    WSACleanup();
}

void trackHandMovement() {
    LEAP_CONNECTION connection;
    LeapCreateConnection(nullptr, &connection);
    LeapOpenConnection(connection);

    LEAP_CONNECTION_MESSAGE msg;
    while (true) {
        LeapPollConnection(connection, 1000, &msg);  // Poll for new messages from the Leap Motion device

        if (msg.type == eLeapEventType_Tracking) {
            const LEAP_TRACKING_EVENT* tracking_event = msg.tracking_event;  // Updated to use const LEAP_TRACKING_EVENT*
            if (tracking_event->nHands > 0) {
                LEAP_HAND hand = tracking_event->pHands[0];
                float xPosition = hand.palm.position.x;
                float grabStrength = hand.grab_strength;  // Get grab strength value (0.0 to 1.0)

                // Print values for debugging
                std::cout << "X-coordinate: " << xPosition << ", Grab Strength: " << grabStrength << std::endl;

                // Send X-position and grab strength over UDP
                sendPositionAndGrabStrength(xPosition, grabStrength);
            }
        }
    }

    LeapCloseConnection(connection);
    LeapDestroyConnection(connection);
}

int main() {
    std::thread trackingThread(trackHandMovement);

    std::cout << "Press Enter to quit..." << std::endl;
    std::cin.get();

    trackingThread.detach();  // Detach the tracking thread when exiting
    return 0;
}
