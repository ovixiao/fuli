spider_list=(
    youdianying
    flkong
    fuliba
    fulidang
    wuxianfuli
)

for spider in ${spider_list[@]}; do
    scrapy crawl ${spider}
done
