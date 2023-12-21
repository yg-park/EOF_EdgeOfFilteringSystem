#pragma once
#define _SILENCE_EXPERIMENTAL_FILESYSTEM_DEPRECATION_WARNING
#include <iostream>
#include <fstream>
#include <Winsock2.h>
#include <experimental/filesystem>
#include <string>
#pragma comment(lib, "ws2_32.lib")

class UdpImageReceiver {
public:
    UdpImageReceiver(int portNumber);
    ~UdpImageReceiver();

    void ReceiveAndProcessImage();

private:
    int port;
    WSADATA wsaData;
    SOCKET udpSocket;
    sockaddr_in serverAddr;
    sockaddr_in clientAddr;
    int clientAddrSize;
};



