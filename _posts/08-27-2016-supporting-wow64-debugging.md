---
layout: post
title: 64bit Debugging and the WoW64 File System Redirection
author: genuine
website: https://github.com/blaquee
---

## A small note on WoW64 Redirection on Windows

With the introduction to a 64bit Windows Operating System Microsoft introduced the Wow64 emulator. This is a combination of DLLs (aptly named wow64xxx.dll) that automatically handle the proper loading of x86 versions ofsystem libraries for 32-bit processes on 64-bit Windows.

In addition to this, in order to prevent file access and registry collisions WoW64 automatically handles redirecting file operations for 32-bit applications requesting access to system resources. Notice on a 64bit version of Windows, when a 32-bit application requests to open a System file located in ``` %wndir%\system32 ```, if that file is also located in the ``` %windir\SysWOW64 ``` Windows File System Redirection kicks in and provides that application with the 32bit version of the application. This is done due to a combination of factors including pre-defined Registry settings and environment variables setup by WoW64 during application start up. 

## How this affected the x96dbg.exe loader

In the x64dbg package, a loader is provided as a convenience to the user in order to support Right-Click Context Menu debugging of applications and Desktop shortcuts. However up until recent commits [1](https://github.com/x64dbg/x64dbg/commit/86b27c9eb8fd45e11717be796814c6fbce23d33f) and [2](https://github.com/x64dbg/x64dbg/commit/ab5f04f900d7d99cdc6a99310be876c4bf2a483d)  proper handling of redirection was not present. More information about this issue can be read here in Issue [#899](https://github.com/x64dbg/x64dbg/issues/89). 

Due to the fact that x96dbg.exe is a 32-bit application, when a Right Click context menu is invoked to debug a 64-bit application in the System directory, File System Redirection will automatically provide it with the 32-bit version of the application. 
This redirection in fact affects the function ```c++ GetFileArchitecture() ``` :

```c++
static arch GetFileArchitecture(const TCHAR* szFileName)
{
    auto retval = notfound;
    auto hFile = CreateFile(szFileName, GENERIC_READ, FILE_SHARE_READ, nullptr, OPEN_EXISTING, 0, nullptr);
    if(hFile != INVALID_HANDLE_VALUE)
    {
        unsigned char data[0x1000];
        DWORD read = 0;
        auto fileSize = GetFileSize(hFile, nullptr);
        auto readSize = DWORD(sizeof(data));
        if(readSize > fileSize)
            readSize = fileSize;
        if(ReadFile(hFile, data, readSize, &read, nullptr))
        {
            retval = invalid;
            auto pdh = PIMAGE_DOS_HEADER(data);
            if(pdh->e_magic == IMAGE_DOS_SIGNATURE && size_t(pdh->e_lfanew) < readSize)
            {
                auto pnth = PIMAGE_NT_HEADERS(data + pdh->e_lfanew);
                if(pnth->Signature == IMAGE_NT_SIGNATURE)
                {
                    if(pnth->FileHeader.Machine == IMAGE_FILE_MACHINE_I386)  //x32
                        retval = x32;
                    else if(pnth->FileHeader.Machine == IMAGE_FILE_MACHINE_AMD64)  //x64
                        retval = x64;
                }
            }
        }
        CloseHandle(hFile);
    }
    return retval;
}
```
The call to ```CreateFile``` will invoke the FS Redirector and if the file requested is a system resource and is a 64-bit application with an equivalent 32-bit version, Windows will return the 32-bit version of that application. So debugging notepad.exe in ``` %windir\system32 ``` will become debugging notepad.exe in ``` %windir\SysWOW64 ``` which is not what was intended.


## The Fix

Luckily for us, Microsoft provides an easy way to bypass the default behavior of File System Redirection. The fix applied to the x96dbg.exe loader is one function that determines whether FS Redirection is supported, and a structure that facilitates disabling this and re-enabling it once done. 
Two conditions need to be met before we can determine whether FS Redirection can be disabled:
1. Are we running under WoW64 context? (Meaning is this a 32bit application running under 64-bit Windows) and 
2. Does this OS support File System Redirection?

Checking for FS Redirection is a simple matter of seeing if the pertinent functions are available:
```c++
static BOOL isWowRedirectionSupported()
{

    BOOL bRedirectSupported = FALSE;

    _Wow64DisableRedirection = (LPFN_Wow64DisableWow64FsRedirection)GetProcAddress(GetModuleHandle(TEXT("kernel32")), "Wow64DisableWow64FsRedirection");
    _Wow64RevertRedirection = (LPFN_Wow64RevertWow64FsRedirection)GetProcAddress(GetModuleHandle(TEXT("kernel32")), "Wow64RevertWow64FsRedirection");

    if(!_Wow64DisableRedirection || !_Wow64RevertRedirection)
        return bRedirectSupported;
    else
        return !bRedirectSupported;

}
```
The structure that encapsulates the calls to these functions is defined like so:
```c++
struct RedirectWow
{
    PVOID oldValue = NULL;
    RedirectWow() {}
    bool DisableRedirect()
    {
        if(!_Wow64DisableRedirection(&oldValue))
        {
            return false;
        }
        return true;
    }
    ~RedirectWow()
    {
        if(oldValue != NULL)
        {
            if(!_Wow64RevertRedirection(oldValue))
                MessageBox(nullptr, TEXT("Error in Reverting Redirection"), TEXT("Error"), MB_OK | MB_ICONERROR);
        }
    }
};
```
Once we've determined that our conditions for FS redirection are met, we can disable it using a simple call to the member function ```DisableRedirect()```. This must be invoked before we attempt to determine the files architecture and this can be seen here at [Line #412](https://github.com/x64dbg/x64dbg/blob/ab5f04f900d7d99cdc6a99310be876c4bf2a483d/src/launcher/x64_dbg_launcher.cpp#L412)

With these changes, x96dbg.exe can now properly allow a user to Debug redirected 64-bit applications as intended.

###References

More reading material on WoW64 can be found from the resources below:
- [WoW64 Implementation Details](https://msdn.microsoft.com/en-us/library/windows/desktop/aa384274(v=vs.85).aspx)
- [File System Redirector](https://msdn.microsoft.com/en-us/library/windows/desktop/aa384187(v=vs.85).aspx)
- [Wow64DisableWow64FsRedirection function](https://msdn.microsoft.com/en-us/library/windows/desktop/aa365743(v=vs.85).aspx)
- [Wow64RevertWow64FsRedirection function](https://msdn.microsoft.com/en-us/library/windows/desktop/aa365745(v=vs.85).aspx)