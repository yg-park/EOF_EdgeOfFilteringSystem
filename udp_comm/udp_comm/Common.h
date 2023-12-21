
//Common.h
#pragma once

#include <string>
#include <iostream>

#define OPENCV_480
#include <opencv2/opencv.hpp>
#include <opencv2/core/ocl.hpp>
#ifdef OPENCV_480
#include <opencv2/highgui/highgui_c.h>
#include <opencv2/imgproc/imgproc_c.h>
#include <opencv2/imgproc/types_c.h>
#endif // OPENCV_480

#ifdef _DEBUG//디버그일때는 뭘쓰고 
#pragma comment(lib,"opencv_world480d.lib")//pragma comment는 
#else	//RELEASE//릴리즈일때는 뭘쓰고 
#pragma comment(lib,"opencv_world480.lib")
#endif
using namespace std;
using namespace cv;