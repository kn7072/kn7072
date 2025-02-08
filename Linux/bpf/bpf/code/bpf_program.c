#include <linux/bpf.h>

#include "/usr/include/bpf/bpf_helpers.h"

//  clang -O2 -target bpf -c bpf_program.c -o bpf_program.o
//  -target bpf
//  gcc -O2 -target bpf -c bpf_program.c -o bpf_program.o
//  clang -g -O2 -target bpf -c bpf_program.c  -I /usr/include/x86_64-linux-gnu/
//  -o bpf_program.o
/*
 https://github.com/iovisor/bcc/issues/4253
/usr/include/linux/types.h:5:10: fatal error: 'asm/types.h' file not found
    5 | #include <asm/types.h>
      |          ^~~~~~~~~~~~~


sudo ln -s /usr/include/x86_64-linux-gnu/asm /usr/include/asm

sudo find . -type f -name "bpf.h"

./usr/src/linux-headers-6.8.0-50/include/uapi/linux/bpf.h
./usr/src/linux-headers-6.8.0-50/include/net/netns/bpf.h
./usr/src/linux-headers-6.8.0-50/include/linux/lsm/bpf.h
./usr/src/linux-headers-6.8.0-50/include/linux/bpf.h
./usr/include/bpf/bpf.h
./usr/include/linux/bpf.h

apt-file list libbpf-dev | grep bpf_helpers.h

You can find all the tracepoints reserved by the system in the directory
/sys/kernel/debug/tracing/events/syscalls/.

 sudo bpftool prog load bpf_program.o /sys/fs/bpf/bpf_program
 sudo ls /sys/fs/bpf
 sudo bpftool prog list | grep "bpf_"
 sudo bpftool prog show id 61 --pretty

 sudo  rm /sys/fs/bpf/bpf_program
 */
#define SEC(NAME) __attribute__((section(NAME), used))
SEC("tracepoint/syscalls/sys_enter_execve")

int bpf_prog(void *ctx) {
    char msg[] = "Hello, BPF World!";
    bpf_trace_printk(msg, sizeof(msg));
    return 0;
}

char _license[] SEC("license") = "GPL";
