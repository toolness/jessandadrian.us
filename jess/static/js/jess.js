var Router = Backbone.Router.extend({
  routes: ROUTES.backbone,
  home: function() {
    $('.rsvp-form').slideUp();
  },
  rsvp: function() {
    $('.rsvp-form').slideDown();
  }
});

var FormSubmitHandlers = {
  _post: function(form, cb) {
    var request = new XMLHttpRequest();
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
        if (cb) {
          cb(response);
        } else {
          Backbone.history.navigate(response.path.slice(1), {
            trigger: true
          });
          $('.rsvp-form').html(response.rsvp_form)
        }
      } else {
        alert("Error! Response code " + request.status + " and type " +
              contentType);
      }
    };
    request.send(new FormData(form));
    return false;
  },
  rsvp: function(form) {
    return this._post(form);
  },
  login: function(form) {
    return this._post(form);
  },
  logout: function(form) {
    return this._post(form, function(response) {
      Backbone.history.navigate(response.path.slice(1));
      $('.rsvp-form').slideUp(function() {
        $(this).html(response.rsvp_form);
      });
    });
  }
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
