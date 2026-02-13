[source](https://stackoverflow.com/questions/2500436/how-does-cat-eof-work-in-bash)

The `cat <<EOF` syntax is very useful when working with multi-line text in Bash, eg. when assigning multi-line string to a shell variable, file or a pipe.

# Examples of `cat <<EOF` syntax usage in Bash:

## 1. Assign multi-line string to a shell variable

```bash
$ sql=$(cat <<EOF
SELECT foo, bar FROM db
WHERE foo='baz'
EOF
)
```

_The `$sql` variable now holds the new-line characters too. You can verify with `echo -e "$sql"`._

## 2. Pass multi-line string to a file in Bash

```bash
$ cat <<EOF > print.sh
#!/bin/bash
echo \$PWD
echo $PWD
EOF
```

_The `print.sh` file now contains:_

```bash
#!/bin/bash
echo $PWD
echo /home/user
```

## 3. Pass multi-line string to a pipe in Bash

```bash
$ cat <<EOF | grep 'b' | tee b.txt
foo
bar
baz
EOF
```

_The `b.txt` file contains `bar` and `baz` lines. The same output is printed to `stdout`._
