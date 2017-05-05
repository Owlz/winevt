
import cffi, re

# Our defs we want to use
cdef = r"""
typedef enum { EvtRpcLogin = 1 } EVT_LOGIN_CLASS;

typedef HANDLE EVT_HANDLE;

EVT_HANDLE WINAPI EvtOpenSession(
    _In_ EVT_LOGIN_CLASS LoginClass,
    _In_ PVOID           Login,
    _In_ DWORD           Timeout,
    _In_ DWORD           Flags
);

typedef struct _EVT_RPC_LOGIN {
  LPWSTR Server;
  LPWSTR User;
  LPWSTR Domain;
  LPWSTR Password;
  DWORD  Flags;
} EVT_RPC_LOGIN;

typedef enum _EVT_RPC_LOGIN_FLAGS { 
  EvtRpcLoginAuthDefault    = 0,
  EvtRpcLoginAuthNegotiate  = 1,
  EvtRpcLoginAuthKerberos   = 2,
  EvtRpcLoginAuthNTLM       = 3
} EVT_RPC_LOGIN_FLAGS;

typedef enum _EVT_SUBSCRIBE_NOTIFY_ACTION { 
  EvtSubscribeActionError    = 0,
  EvtSubscribeActionDeliver  = 1
} EVT_SUBSCRIBE_NOTIFY_ACTION;

typedef DWORD ( WINAPI *EVT_SUBSCRIBE_CALLBACK)(
   EVT_SUBSCRIBE_NOTIFY_ACTION Action,
   PVOID                       UserContext,
   EVT_HANDLE                  Event
);

EVT_HANDLE WINAPI EvtSubscribe(
  _In_ EVT_HANDLE             Session,
  _In_ HANDLE                 SignalEvent,
  _In_ LPCWSTR                ChannelPath,
  _In_ LPCWSTR                Query,
  _In_ EVT_HANDLE             Bookmark,
  _In_ PVOID                  context,
  _In_ EVT_SUBSCRIBE_CALLBACK Callback,
  _In_ DWORD                  Flags
);

EVT_HANDLE WINAPI EvtQuery(
  _In_ EVT_HANDLE Session,
  _In_ LPCWSTR    Path,
  _In_ LPCWSTR    Query,
  _In_ DWORD      Flags
);

typedef enum _EVT_QUERY_FLAGS { 
  EvtQueryChannelPath          = 0x1,
  EvtQueryFilePath             = 0x2,
  EvtQueryForwardDirection     = 0x100,
  EvtQueryReverseDirection     = 0x200,
  EvtQueryTolerateQueryErrors  = 0x1000
} EVT_QUERY_FLAGS;

BOOL WINAPI EvtNext(
  _In_  EVT_HANDLE  ResultSet,
  _In_  DWORD       EventArraySize,
  _In_  EVT_HANDLE* EventArray,
  _In_  DWORD       Timeout,
  _In_  DWORD       Flags,
  _Out_ PDWORD      Returned
);

typedef enum _EVT_RENDER_FLAGS { 
  EvtRenderEventValues  = 0,
  EvtRenderEventXml     = 1,
  EvtRenderBookmark     = 2
} EVT_RENDER_FLAGS;

BOOL WINAPI EvtRender(
  _In_  EVT_HANDLE Context,
  _In_  EVT_HANDLE Fragment,
  _In_  DWORD      Flags,
  _In_  DWORD      BufferSize,
  _In_  PVOID      Buffer,
  _Out_ PDWORD     BufferUsed,
  _Out_ PDWORD     PropertyCount
);

DWORD WINAPI GetLastError(void);

BOOL WINAPI EvtClose(
  _In_ EVT_HANDLE Object
);
"""


# Simple source file
source = r"""
#include <windows.h>
#include <WinEvt.h>

void main()
{
    return 0;
}
"""

def ffibuilder():
    """Do out-of-line build."""

    # Insantiate a class
    ffi = cffi.FFI()

    # Setup our definitions
    ffi.cdef(re.sub(r"\b(_In_|_Inout_|_Out_|_Outptr_)(opt_)?\b", " ",cdef))

    # Setup our binary
    ffi.set_source("_winevt",source,libraries=["Wevtapi"])

    return ffi


# Default build and compile it.
if __name__ == "__main__":
    ffi = ffibuilder()

    # Compile it!
    ffi.compile(verbose=True)

