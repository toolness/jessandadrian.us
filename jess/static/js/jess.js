var Router = Backbone.Router.extend({
  routes: ROUTES.backbone,
  _showFormContent: function(sel) {
    $('.rsvp-form').stop().slideUp('fast').queue(function() {
      $('.rsvp-form-content').hide().filter(sel).show();
      $(this).dequeue();
    }).slideDown('fast');
  },
  home: function() { $('.rsvp-form').stop().slideUp('fast'); },
  rsvp: function() { this._showFormContent('#rsvp'); },
  rsvp_yay: function() { this._showFormContent('#yay'); },
  rsvp_boo: function() { this._showFormContent('#boo'); }
});

var FormSubmitHandlers = {
  _post: function(form, noSlideDown) {
    var request = new XMLHttpRequest();
    var rsvpForm = $('.rsvp-form');
    request.open('POST', $(form).attr('action'));
    request.setRequestHeader('Accept', 'application/json');
    request.onreadystatechange = function() {
      if (request.readyState != 4) return;

      var contentType = request.getResponseHeader('Content-Type');
      var response;
      if (request.status == 200 && contentType == 'application/json') {
        try {
          response = JSON.parse(request.responseText);
        } catch (e) {
          return alert("Error! Invalid JSON.");
        }
        Backbone.history.navigate(response.path.slice(1));
        rsvpForm.queue(function() {
          rsvpForm.html(response.rsvp_form);
          if (!noSlideDown) rsvpForm.slideDown();
          rsvpForm.dequeue();
        });
      } else {
        alert("Error! Response code " + request.status + " and type " +
              contentType);
      }
    };
    request.send(new FormData(form));
    rsvpForm.slideUp();
    return false;
  },
  rsvp: function(form) { return this._post(form); },
  login: function(form) { return this._post(form); },
  logout: function(form) { return this._post(form, true); }
};

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

  if (window.history && window.history.pushState)
    $(document.body).on('click', 'a[href^="/"]', function(e) {
      var fragment = $(this).attr('href').slice(1);
      if (doesRouteExist(fragment)) {
        Backbone.history.navigate(fragment, {trigger: true});
        return false;
      }
    });

  if ('FormData' in window && 'JSON' in window)
    $(document.body).on('submit', 'form[action^="/"]', function(e) {
      var fragment = $(this).attr('action').slice(1);
      var routeName = ROUTES.form[fragment];

      if ($(this).attr('method').toUpperCase() != "POST") return;
      if (!(routeName && FormSubmitHandlers[routeName])) return;

      return FormSubmitHandlers[routeName](this);
    });

  Backbone.history.start({
    pushState: true,
    hashChange: false,
    silent: true
  });
});
