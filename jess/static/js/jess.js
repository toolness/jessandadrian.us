function hasLocalStorage() {
  try {
    window.localStorage['_test'] = '1';
    delete window.localStorage['_test'];
    return true;
  } catch (e) {
    return false;
  }
}

$(document).ready(function() {
  var logoutForm = $('.logout');

  $('#animation').click(function() {
    $('div').toggleClass('beginAnimation');
  });

  if (!hasLocalStorage()) return;

  $('.rsvp').click(function() {
    if ('show_rsvp_form' in window.localStorage) {
      delete window.localStorage['show_rsvp_form'];
      if (logoutForm.length) logoutForm.submit();
      $('.rsvp-form').slideUp();
    } else {
      window.localStorage['show_rsvp_form'] = '1';
      $('.rsvp-form').slideDown();
    }
  });

  logoutForm.submit(function() {
    delete window.localStorage['show_rsvp_form'];
  });

  $('.rsvp-form').toggle(!!('show_rsvp_form' in window.localStorage));
});
