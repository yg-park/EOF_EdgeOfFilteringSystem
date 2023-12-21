#include "comm_server.h"

UdpImageReceiver::UdpImageReceiver(int portNumber) : port(portNumber), clientAddrSize(sizeof(clientAddr)) {
    // Winsock initialization
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "Failed to initialize Winsock" << std::endl;
        std::exit(1);
    }

    // UDP socket creation
    udpSocket = socket(AF_INET, SOCK_DGRAM, 0);

    // Server address configuration
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
    serverAddr.sin_port = htons(port);

    // Socket binding
    bind(udpSocket, (sockaddr*)&serverAddr, sizeof(serverAddr));
}

UdpImageReceiver::~UdpImageReceiver() {
    // Winsock cleanup
    closesocket(udpSocket);
    WSACleanup();
}

CImage* UdpImageReceiver::ReceiveAndProcessImage() {
    const int maxBufferSize = 65536;
    char buffer[maxBufferSize];
    int bytesRead = recvfrom(udpSocket, buffer, sizeof(buffer), 0, (sockaddr*)&clientAddr, &clientAddrSize);

    CImage* receivedImage = nullptr;

    // Check if this is the first chunk (header)
    if (bytesRead >= sizeof(int)) {
        // Read the total size of the image from the header
        int imageSize;
        memcpy(&imageSize, buffer, sizeof(int));

        // Create a folder named "images" if it doesn't exist
        const std::string folderPath = "image";
        std::experimental::filesystem::create_directory(folderPath);

        // Open a new file for writing in binary mode in the "images" folder
        static int frameCounter = 0;
        const std::string filename = folderPath + "/received_image.jpg";
        std::ofstream outputFile(filename, std::ios::binary);
        frameCounter++;

        // Write the data (excluding the header) to the file
        if (outputFile.is_open()) {
            outputFile.write(buffer + sizeof(int), bytesRead - sizeof(int));
            outputFile.close();
            std::cout << "Received frame saved to: " << filename << "_" << frameCounter << std::endl;

            // Load the image into a CImage object
            receivedImage = new CImage();
            receivedImage->Load(filename.c_str());
        }
        else {
            std::cerr << "Failed to open the file for writing: " << filename << std::endl;
        }
    }

    return receivedImage;
}

int main() {
    UdpImageReceiver udpReceiver(12345);

    while (true) {
        CImage* receivedImage = udpReceiver.ReceiveAndProcessImage();

        if (receivedImage != nullptr) {
            // 여기서 receivedImage를 활용하여 MFC에서 필요한 작업을 수행
            // 예를 들면 receivedImage를 Picture Control에 표시하는 등의 작업이 가능합니다.

            // 메모리 누수를 방지하기 위해 CImage 객체를 삭제
            delete receivedImage;
        }
    }

    return 0;
}














/*
#include "comm_server.h"

UdpImageReceiver::UdpImageReceiver(int portNumber) : port(portNumber), clientAddrSize(sizeof(clientAddr)) {
    // Winsock initialization
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "Failed to initialize Winsock" << std::endl;
        std::exit(1);
    }

    // UDP socket creation
    udpSocket = socket(AF_INET, SOCK_DGRAM, 0);

    // Server address configuration
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
    serverAddr.sin_port = htons(port);

    // Socket binding
    bind(udpSocket, (sockaddr*)&serverAddr, sizeof(serverAddr));
}

UdpImageReceiver::~UdpImageReceiver() {
    // Winsock cleanup
    closesocket(udpSocket);
    WSACleanup();
}

void UdpImageReceiver::ReceiveAndProcessImage() {
    const int maxBufferSize = 65536;
    char buffer[maxBufferSize];
    int bytesRead = recvfrom(udpSocket, buffer, sizeof(buffer), 0, (sockaddr*)&clientAddr, &clientAddrSize);

    // Check if this is the first chunk (header)
    if (bytesRead >= sizeof(int)) {
        // Read the total size of the image from the header
        int imageSize;
        memcpy(&imageSize, buffer, sizeof(int));

        // Create a folder named "images" if it doesn't exist
        const std::string folderPath = "image";
        std::experimental::filesystem::create_directory(folderPath);

        // Open a new file for writing in binary mode in the "images" folder
        static int frameCounter = 0;
        const std::string filename = folderPath + "/received_image.jpg";
        std::ofstream outputFile(filename, std::ios::binary);
        frameCounter++;
        // Write the data (excluding the header) to the file
        if (outputFile.is_open()) {
            outputFile.write(buffer + sizeof(int), bytesRead - sizeof(int));
            outputFile.close();
            std::cout << "Received frame saved to: " << filename << "_" << frameCounter << std::endl;
        }
        else {
            std::cerr << "Failed to open the file for writing: " << filename << std::endl;
        }
    }
}




int main() {
    UdpImageReceiver udpReceiver(12345);

    while (true) {
        udpReceiver.ReceiveAndProcessImage();
    }

    return 0;
}


*/