(function () {
  const enabled = location.protocol.startsWith("http");
  const lesson = (location.pathname.split("/").pop() || "").replace(".html", "");

  function send(event) {
    if (!enabled) return;
    const body = JSON.stringify({ lesson, title: document.title, ...event });
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon("/api/event", new Blob([body], { type: "application/json" }));
      } else {
        fetch("/api/event", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body,
          keepalive: true,
        });
      }
    } catch (_) {
      // Logging must never block the exercise.
    }
  }

  send({ kind: "open" });
  window.Progress = { enabled, send };
})();
