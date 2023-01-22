(function (window) {
  window.env = window.env || {};

  // Environment variables
  window["env"]["backend"] = "${BACKEND}";
  window["env"]["debug"] = "${DEBUG}";
})(this);
