$(function () {
  function renderTime() {
    return moment($(this).data('timestamp')).format('lll');
  }
  $('[data-toggle="tooltip"]').tooltip({ title: renderTime });
});