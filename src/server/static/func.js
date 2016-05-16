function addPage(type, page) {
  $.getJSON("/append/" + type + "/" + page, function(data) {
    if (!data.more) {
      withContent = false;
    }
    if (data.len > 0) {
      $('.infinite-scroll-bottom .cards').append(data.embed_code);
    }
  });
}

function infinite_scroll() {
  // 如果正在加载，则退出
  if (loading) return;
  // 设置flag
  loading = true;
  // 重置加载flag
  if (!withContent || curPage > maxPage) {
    // 加载完毕，则注销无限加载事件，以防不必要的加载
    $.detachInfiniteScroll($('.infinite-scroll'));
    // 删除加载提示符
    $('.infinite-scroll-preloader').remove();
    $('#next-page').attr('href', '/page/' + type + '/' + curPage);
    $('#next-page').css('display', 'block');
    return;
  }
  setTimeout(function() {
    // 添加新条目
    addPage(type, curPage);
    curPage += 1;
    //容器发生改变,如果是js滚动，需要刷新滚动
    $.refreshScroller();
    loading = false;
  }, 100);
}
