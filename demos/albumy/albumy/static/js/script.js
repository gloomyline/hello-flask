$(function () {
  // login password input toggle display
  const renderTime = function () {
    return momment($(this).data('timestamp')).format('LL');
  }
  $('[data-toggle="tooltip"]').tooltip({ title: renderTime });
});