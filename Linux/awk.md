cat file | awk  -F' — '  '{print "\"" $1 "\"" ","}'
cat file | awk  -F' — '  '{print "if;" "    " $1 ";" "    " $2}'
