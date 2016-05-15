function addPage(type, page) {
  $.get("/append/" + type + "/" + page, function(data) {
    $('.infinite-scroll-bottom .cards').append(data);
  });
}

function infinite_scroll() {
  // 如果正在加载，则退出
  if (loading) return;
  // 设置flag
  loading = true;
  console.log(curPage);
  setTimeout(function() {
    // 重置加载flag
    if (curPage > maxPage) {
      // 加载完毕，则注销无限加载事件，以防不必要的加载
      $.detachInfiniteScroll($('.infinite-scroll'));
      // 删除加载提示符
      $('.infinite-scroll-preloader').remove();
      $('#next-page').attr('href', '/' + type + '/' + curPage);
      $('#next-page').css('display', 'block');
      return;
    }
    // 添加新条目
    addPage(type, curPage);
    curPage += 1;
    //容器发生改变,如果是js滚动，需要刷新滚动
    $.refreshScroller();
    loading = false;
  }, 500);
}
