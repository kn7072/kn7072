#!/bin/bash

# (72 points == 1 inch == 25.4 mm)
width_a4=595 # ширана a4 в points
hight_a4=842
const_mm_to_pt=$(bc <<<"scale=2;72/25.4") # коэффициент для перевода миллиметвов в поинты
margin_const_x_mm=8                       # константа - получени имперически(распечатав страницу и измерив линейкой)
margin_const_x=$(bc <<<"scale=2;${const_mm_to_pt}*${margin_const_x_mm}")
margin_const_y_mm=8 # константа - получени имперически(распечатав страницу и измерив линейкой)
margin_const_y=$(bc <<<"scale=2;${const_mm_to_pt}*${margin_const_y_mm}")
scale=1.2         # коэффициент увеличения страницы
margin_left_mm=30 # на печате при желаемом отступе 25 будет добавлен дополнительный отступ 5 мм итого будет примерно 30
margin_top_mm=15
margin_left_pt=$(bc <<<"scale=2;${const_mm_to_pt}*${margin_left_mm}") # желаемы отступы в point
margin_top_pt=$(bc <<<"scale=2;${const_mm_to_pt}*${margin_top_mm}")

dir_mediabox_a4='./mediabox_a4' # тут нахорятся страницы с изменунными границами mediabox под формат A4
dir_scale_files='./scale_files'
dir_with_margin_0='./temp-margins-0-for-test/' # сюда попадают страницы без отступов
dir_scale_min_shift='./scale_min_shift'
dir_ready_files='./ready_files'

mkdir -p $dir_mediabox_a4 # no error if existing
mkdir -p $dir_scale_files
mkdir -p $dir_ready_files
mkdir -p $dir_scale_min_shift

for FILE in $(find $dir_with_margin_0 -type f -name '*page.pdf' | sort -V); do
  echo "######"
  echo "path file ${FILE}"
  arrIN=(${FILE//_/ }) # массив полученный разделением строки с помощью символо _(фактичести
  # произошла замена символа _ на символ пробела и получившиеся данные стали массивом, так как данные находятся в круглых скобках)
  # echo ${arrIN[0]}
  echo "${arrIN[0]//$dir_with_margin_0/}"
  number_zeros=${arrIN[0]//$dir_with_margin_0/}
  number=$((10#$number_zeros))

  name_file="${number}_output_${arrIN[1]}.pdf"
  path_file_media="${dir_mediabox_a4}/${name_file}"
  echo "${path_file_media}"

  # команда расширяет страницу до формата a4
  command_create_media="cpdf -mediabox '0pt 0pt ${width_a4}pt ${hight_a4}pt' ${FILE} -o ${path_file_media}"
  echo "${command_create_media}"
  eval "${command_create_media}"

  # увеличим размер старницы на величину scale
  path_to_scale_file="${dir_scale_files}/${name_file}"
  command_scale="cpdf -scale-contents ${scale} ${path_file_media} -o ${path_to_scale_file}"
  eval "${command_scale}"

  page_size_str=$(pdfinfo ${FILE} | grep 'Page size')
  page_size_array=($(echo ${page_size_str} | awk '{printf "%.0f %.0f", $3, $5}'))
  width_page="${page_size_array[0]}"
  hight_page="${page_size_array[1]}"

  width_page_scale=$(bc <<<"scale=2;${width_page}*${scale}")
  hight_page_scale=$(bc <<<"scale=2;${hight_page}*${scale}")

  echo "${page_size_str}"
  echo "width ${width_page}, width_scale ${width_page_scale}"
  echo "hight ${hight_page}, hight_scale ${hight_page_scale}"

  # minimum_shift_x это минимальное число на которое нужно сместить mediabox после того как его увеличили в scale раз
  # при увеличении часть изображения "ушла" вниз и влево на величину ${width_page_scale}-${width_page})/2 + ${margin_const}"
  # константа margin_const (не могу сказать почему она такая - вероятно это удвоенный отступ = 8 (4 * 2 где 4 минимальный отспуп при печати))
  # после этих смещений, увеличенная стнаница должна полностью помещаться (быть видимой полностью без смещений) т.e левый нижний
  # угол страницы(контента) должен совпадать с нижним левым углом всей страницы - слева и сверху будут отступы и их мы и будем изменять
  # отрицательные числа говорят, что смещать нужно вправо и вверх
  minimum_shift_x=$(bc <<<"scale=2;(${width_page_scale}-${width_page})/2 + ${margin_const_x}")
  minimum_shift_y=$(bc <<<"scale=2;(${hight_page_scale}-${hight_page})/2 + ${margin_const_y}")
  echo "shift to right -${minimum_shift_x}"
  echo "shift to up -${minimum_shift_y}"

  path_to_shift_files="${dir_scale_min_shift}/${name_file}"
  command_finish_shift="cpdf -shift-boxes '-${minimum_shift_x} -${minimum_shift_y}' ${path_to_scale_file} -o ${path_to_shift_files}"
  echo "${command_finish_shift}"
  eval "${command_finish_shift}"

  # вичислим смещение вверх чтобы добиться желаемого отступа сверху
  #
  additional_shift_top=$(bc <<<"scale=2;${hight_a4}-(${hight_page_scale}+${margin_top_pt})")
  finish_shift_top=$(bc <<<"scale=2;${minimum_shift_y}+${additional_shift_top}")
  if [[ $((number % 2)) -eq 0 ]]; then
    echo "четное"
    finish_shift_left=$(bc <<<"scale=2;${minimum_shift_x}+${margin_left_pt}")
  else
    echo "нечетное"
    finish_shift_left=$(bc <<<"scale=2;${width_a4}-(${width_page_scale}+${margin_left_pt})+${minimum_shift_x}")
  fi

  echo "${finish_shift_left}"

  path_to_ready_files="${dir_ready_files}/${name_file}"
  command_finish_shift="cpdf -shift-boxes '-${finish_shift_left} -${finish_shift_top}' ${path_to_scale_file} -o ${path_to_ready_files}"
  echo "${command_finish_shift}"
  eval "${command_finish_shift}"
done
