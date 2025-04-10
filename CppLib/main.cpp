#include <opencv2/opencv.hpp>
#include <iostream>
#include <chrono>
#include<string>
#include "vehicles/multirotor/api/MultirotorRpcLibClient.hpp"
#include "common/common_utils/FileSystem.hpp"

#include "common/common_utils/StrictMode.hpp"
STRICT_MODE_OFF
#ifndef RPCLIB_MSGPACK
#define RPCLIB_MSGPACK clmdep_msgpack
#endif // !RPCLIB_MSGPACK
#include "rpc/rpc_error.h"
STRICT_MODE_ON

int main()
{    
    using namespace msr::airlib;
    typedef ImageCaptureBase::ImageType ImageType;

    msr::airlib::MultirotorRpcLibClient client;
    client.confirmConnection();
    
    int width = 1280;
    int height = 720;
    int fps = 30;

    auto fontScale = 0.5;
    int thickness = 2;
    int textSize = 10;
    cv::Point textOrg(10, 10 + textSize);
    int frameCount = 0;
    auto startTime = std::chrono::high_resolution_clock::now();
    int fps_label = 0;
        
    std::string gstreamer_pipeline = "appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=1000 speed-preset=superfast ! rtph264pay ! "
    "udpsink host=127.0.0.1 port=5000";

    cv::VideoWriter writer;
    writer.open(gstreamer_pipeline, cv::CAP_GSTREAMER, 0, fps, cv::Size(width, height), true);
    
    if (!writer.isOpened())
    {
        std::cerr << "Error: Could not open video writer with GStreamer pipeline." << std::endl;
        return -1;
    }
    
    while (true) {
        auto startTimeReq = std::chrono::high_resolution_clock::now();
        const std::vector<uint8_t> image_data = client.simGetImage("0", ImageType::Scene);
        auto endTimeReq = std::chrono::high_resolution_clock::now();
        auto diffReq = std::chrono::duration_cast<std::chrono::milliseconds>(endTimeReq - startTimeReq);
        std::cout << diffReq.count() << std::endl;

        cv::Mat frame = cv::imdecode(image_data, cv::IMREAD_COLOR);

        if (frame.empty()) {
            std::cerr << "Error: Failed to decode image." << std::endl;
            continue;
        }
        if (frame.cols != width || frame.rows != height) {
            cv::resize(frame, frame, cv::Size(width, height));
        }
        writer.write(frame);

        frameCount++;
        auto endTime = std::chrono::high_resolution_clock::now();
        auto diff = std::chrono::duration_cast<std::chrono::seconds>(endTime - startTime);
        if (diff.count() > 1) {
            fps_label = frameCount;
            frameCount = 0;
            startTime = endTime;
        }
        cv::putText(frame,"FPS " + std::to_string(fps_label), textOrg, cv::FONT_HERSHEY_SIMPLEX, fontScale,(255,0,255),thickness);
        cv::imshow("AirSim Camera Stream", frame);
        if (cv::waitKey(1) == 'q')
        {
            std::cout << "Exiting..." << std::endl;
            break;
        }
    }
    writer.release();
    cv::destroyAllWindows();

    return 0;
}
