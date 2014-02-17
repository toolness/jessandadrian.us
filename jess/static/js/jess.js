var Router = Backbone.Router.extend({
  routes: ROUTES,
  home: function() {
    $('.rsvp-form').slideUp();
  },
  rsvp: function() {
    $('.rsvp-form').slideDown();
  }
});

function doesRouteExist(path) {
  return _.any(Backbone.history.handlers, function(handler) {
    return handler.route.test(path);
  });
}

$(document).ready(function() {
  var router = new Router();

  $('#animation').click(function() {
    $('div', this).toggleClass('beginAnimation');
  });

  $(document.body).on('click', 'a[href^="/"]', function(e) {
    var fragment = $(this).attr('href').slice(1);
    if (doesRouteExist(fragment)) {
      Backbone.history.navigate(fragment, {trigger: true});
      return false;
    }
  });

  Backbone.history.start({
    pushState: true,
    hashChange: false,
    silent: true
  });
});
