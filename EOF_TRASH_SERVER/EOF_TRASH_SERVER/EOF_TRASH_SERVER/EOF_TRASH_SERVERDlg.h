
// EOF_TRASH_SERVERDlg.h: 헤더 파일
//

#pragma once
#include <afxsock.h>  // MFC Socket 클래스 헤더 파일
#include <mutex>
#include <iostream>

#define WM_USER_UDP_COMM WM_USER + 1
#define WM_USER_TCP_COMM WM_USER + 2

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <atlimage.h> // CImage를 사용하기 위한 헤더
// DB
//#include <mysql.h>

// CEOFTRASHSERVERDlg 대화 상자
class CEOFTRASHSERVERDlg : public CDialogEx
{
// 생성입니다.
public:
	CEOFTRASHSERVERDlg(CWnd* pParent = nullptr);	// 표준 생성자입니다.

// 대화 상자 데이터입니다.
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_EOF_TRASH_SERVER_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV 지원입니다.


// 구현입니다.
protected:
	HICON m_hIcon;

	// 생성된 메시지 맵 함수
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();

	afx_msg LRESULT OnUdpThreadDone(WPARAM wParam, LPARAM lParam);
	afx_msg LRESULT OnTcpThreadDone(WPARAM wParam, LPARAM lParam);

	DECLARE_MESSAGE_MAP()

private:
	CWinThread* pUdpThread;
	CWinThread* pTcpThread;
	CEvent eventUdp;  // UDP 이벤트 추가
	CEvent eventTcp;  // TCP 이벤트 추가

	// port
	int m_nUdpPort;
	int m_nTcpPort;

	// UdpThreadProc와 TcpThreadProc를 static 멤버 함수로 선언
	static UINT CALLBACK UdpThreadProc(LPVOID pParam);
	static UINT CALLBACK TcpThreadProc(LPVOID pParam);

	CStatic m_ImageCtrl;
};
