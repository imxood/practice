# gdb program_with_debug

    (gdb) target remote 127.0.0.1:49101
    (gdb) b timer_handler
    (gdb) monitor reset
    (gdb) b main
    (gdb) i b
    (gdb) d 1
    (gdb) r
    (gdb) n
    (gdb) s
    (gdb) clear main
    (gdb) p VARIABLE
    (gdb) set listsize 50
    (gdb) show listsize
    (gdb) l main

