for file in `find -type f `; do
    dos2unix "${file}"
done