/* for windows64 */
#define GET_HINST( hwnd )		(HINSTANCE)GetWindowLongPtr( hwnd, GWLP_HINSTANCE );
#define GET_WM_COMMAND_CMD(wp, lp)      HIWORD(wp)
#define GET_WM_COMMAND_HWND(wp, lp)     (HWND)(lp)
#define GET_WM_COMMAND_MPS(id, hwnd, cmd) (UINT)MAKELONG(id, cmd), (LONG)(hwnd)
#define GET_WM_VSCROLL_POS( wp, lp )	HIWORD(wp)
#define GET_WM_VSCROLL_HWND( wp, lp )	(HWND)(lp)
#define GET_WM_VSCROLL_CODE( wp, lp )	LOWORD(wp)
#define GET_WM_HSCROLL_POS( wp, lp )	HIWORD(wp)
#define GET_WM_HSCROLL_HWND( wp, lp )	(HWND)(lp)
#define GET_WM_HSCROLL_CODE( wp, lp )	LOWORD(wp)
#define GET_CURSOR( hwnd )		GetWindowLong( hwnd, GCL_HCURSOR )
#define MAKE_POINT( pt, lp )		pt.x = (long)(short)LOWORD( lp ); \
					pt.y = (long)(short)HIWORD( lp ) 
#define MK_FP32(x)			(x)
#define MK_LOCAL32(a) 			((void far *) a)
#define PASS_WORD_AS_POINTER(i) 	((LPSTR)(WORD)(i))
#define AllocAlias16(a) 		((DWORD)(LPSTR)(a))
#define FreeAlias16(a)
#ifdef __WINDOWS_386__
#define _EXPORT
#else
#define _EXPORT __export
#endif

