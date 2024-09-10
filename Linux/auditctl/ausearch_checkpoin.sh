# checkpoint means ausearch will use the timestamp found within  a
# valid  checkpoint  file ignoring the recorded inode, device, serial, 
# node and event type also found within a  checkpoint  file.
# Essentially, this is the recovery action should an invocation of
# ausearch with a checkpoint option fail with an  exit  status  of
# 10, 11 or 12. It could be used in a shell script something like:


ausearch --checkpoint /etc/audit/auditd_checkpoint.txt -i -k git
_au_status=$?
if test ${_au_status} eq 10 -o ${_au_status} eq 11 -o ${_au_status} eq 12 then
    ausearch --checkpoint /etc/audit/auditd_checkpoint.txt --start checkpoint -i -k git
fi

