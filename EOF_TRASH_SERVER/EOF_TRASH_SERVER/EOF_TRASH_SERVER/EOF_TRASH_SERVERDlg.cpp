
// EOF_TRASH_SERVERDlg.cpp: 구현 파일
//

#include "pch.h"
#include "framework.h"
#include "EOF_TRASH_SERVER.h"
#include "EOF_TRASH_SERVERDlg.h"
#include "afxdialogex.h"

#ifdef _DEBUG
#define new DEBUG_NEW

// console
#pragma comment(linker, "/ENTRY:WinMainCRTStartup /subsystem:console")
#endif

//
CMutex m_mutexUdpEvent;
CMutex m_mutexTcpEvent;
//

// 응용 프로그램 정보에 사용되는 CAboutDlg 대화 상자입니다.

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// 대화 상자 데이터입니다.
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_ABOUTBOX };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 지원입니다.

// 구현입니다.
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialogEx(IDD_ABOUTBOX)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()


// CEOFTRASHSERVERDlg 대화 상자



CEOFTRASHSERVERDlg::CEOFTRASHSERVERDlg(CWnd* pParent /*=nullptr*/)
	: CDialogEx(IDD_EOF_TRASH_SERVER_DIALOG, pParent)
	, m_nUdpPort(8888)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);

	m_ImageCtrl.SubclassDlgItem(IDC_IMAGE1, this);
}

void CEOFTRASHSERVERDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CEOFTRASHSERVERDlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()

	ON_MESSAGE(WM_USER + 1, OnUdpThreadDone)
	ON_MESSAGE(WM_USER + 2, OnTcpThreadDone)
END_MESSAGE_MAP()


// CEOFTRASHSERVERDlg 메시지 처리기

BOOL CEOFTRASHSERVERDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// 시스템 메뉴에 "정보..." 메뉴 항목을 추가합니다.

	// IDM_ABOUTBOX는 시스템 명령 범위에 있어야 합니다.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != nullptr)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// 이 대화 상자의 아이콘을 설정합니다.  응용 프로그램의 주 창이 대화 상자가 아닐 경우에는
	//  프레임워크가 이 작업을 자동으로 수행합니다.
	SetIcon(m_hIcon, TRUE);			// 큰 아이콘을 설정합니다.
	SetIcon(m_hIcon, FALSE);		// 작은 아이콘을 설정합니다.

	// TODO: 여기에 추가 초기화 작업을 추가합니다.
	
	// 이벤트 초기화
	eventUdp.ResetEvent();
	eventTcp.ResetEvent();

	// 스레드 생성 및 시작
	pUdpThread = AfxBeginThread(UdpThreadProc, this);
	pTcpThread = AfxBeginThread(TcpThreadProc, this);

	return TRUE;  // 포커스를 컨트롤에 설정하지 않으면 TRUE를 반환합니다.
}

void CEOFTRASHSERVERDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}


// 대화 상자에 최소화 단추를 추가할 경우 아이콘을 그리려면
//  아래 코드가 필요합니다.  문서/뷰 모델을 사용하는 MFC 애플리케이션의 경우에는
//  프레임워크에서 이 작업을 자동으로 수행합니다.

void CEOFTRASHSERVERDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // 그리기를 위한 디바이스 컨텍스트입니다.

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// 클라이언트 사각형에서 아이콘을 가운데에 맞춥니다.
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// 아이콘을 그립니다.
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

// 사용자가 최소화된 창을 끄는 동안에 커서가 표시되도록 시스템에서
//  이 함수를 호출합니다.
HCURSOR CEOFTRASHSERVERDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}


LRESULT CEOFTRASHSERVERDlg::OnUdpThreadDone(WPARAM wParam, LPARAM lParam)
{
	int nDataSize = (int)wParam;
	const BYTE* pData = (const BYTE*)lParam;

	if (pData != NULL && nDataSize > 0)
	{
		cv::Mat image = cv::imdecode(cv::Mat(1, nDataSize, CV_8U, (void*)pData), cv::IMREAD_COLOR);

		if (!image.empty())
		{
			// 이미지를 표시할 CImage 생성
			CImage cImage;
			cImage.Create(image.cols, image.rows, 24); // 24는 비트 당 색상 비트 수

			// OpenCV Mat 데이터를 CImage에 복사
			uchar* dstData = (uchar*)cImage.GetBits();
			memcpy(dstData, image.data, image.rows * image.step);

			// 이미지를 표시할 컨트롤에 이미지 설정
			m_ImageCtrl.SetBitmap((HBITMAP)cImage.Detach());
			m_ImageCtrl.Invalidate(); // 컨트롤을 다시 그리도록 갱신 요청
		}

		// 메모리 해제
		delete[] pData;
	}

	return 0;
}


LRESULT CEOFTRASHSERVERDlg::OnTcpThreadDone(WPARAM wParam, LPARAM lParam)
{
	// TCP 스레드에서 작업이 완료되면 호출되는 함수
	// 추가 작업 수행
	// ...
	std::cout << "TCP" << std::endl;

	return 0;
}


UINT CALLBACK CEOFTRASHSERVERDlg::UdpThreadProc(LPVOID pParam)
{
	CEOFTRASHSERVERDlg* pDlg = (CEOFTRASHSERVERDlg*)pParam;

	// Winsock 초기화
	WSADATA wsaData;
	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
		AfxMessageBox(_T("Winsock 초기화에 실패했습니다."));
		return 1;
	}

	// UDP 통신 소켓 생성
	CAsyncSocket udpSocket;
	long lEvent = FD_READ | FD_WRITE | FD_CLOSE;
	if (!udpSocket.Create(pDlg->m_nUdpPort, SOCK_DGRAM, lEvent)) {
		return 1;
	}

	while (true) {
		// 뮤텍스 락
		m_mutexUdpEvent.Lock();

		// 데이터 수신
		BYTE buffer[1024];
		int bytesRead = udpSocket.Receive(buffer, sizeof(buffer), 0);
		if (bytesRead > 0) {
			// 수신된 데이터를 메인 다이얼로그에 전달
			BYTE* pData = new BYTE[bytesRead];
			memcpy(pData, buffer, bytesRead);
			pDlg->PostMessage(WM_USER + 1, (WPARAM)bytesRead, (LPARAM)pData);
		}
		else
		{
			pDlg->PostMessage(WM_USER + 1, 0, 0);
		}

		// 뮤텍스 언락
		m_mutexTcpEvent.Unlock();
	}
	return 0;
}

UINT CALLBACK CEOFTRASHSERVERDlg::TcpThreadProc(LPVOID pParam)
{
	CEOFTRASHSERVERDlg* pDlg = (CEOFTRASHSERVERDlg*)pParam;

	// Tcp Thread의 작업 수행
	while (true)
	{
		// 뮤텍스 락
		m_mutexTcpEvent.Lock();

		// 문자열 수신 코드
		// ...

		// 작업이 완료되면 PostMessage로 메시지 전송
		pDlg->PostMessage(WM_USER + 2, 0, 0);


		// 뮤텍스 언락
		m_mutexUdpEvent.Unlock();
	}

	return 0;
}

