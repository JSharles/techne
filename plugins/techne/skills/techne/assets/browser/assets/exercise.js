(function () {
  const workerSource = `
self.onmessage = (event) => {
  const { code, fn, args } = event.data;
  try {
    const target = new Function(code + "\\n;return typeof " + fn + " === 'function' ? " + fn + " : undefined;")();
    if (!target) {
      self.postMessage({ error: "La fonction " + fn + " n'est pas définie." });
      return;
    }
    const output = args.map((input) => {
      try { return { value: target(...structuredClone(input)) }; }
      catch (error) { return { error: String(error?.message || error) }; }
    });
    self.postMessage({ output });
  } catch (error) {
    self.postMessage({ error: "Erreur de syntaxe : " + String(error?.message || error) });
  }
};`;

  const same = (left, right) => JSON.stringify(left) === JSON.stringify(right);

  function mount(root, config) {
    root.classList.add("activity", "exercise");
    const openedAt = Date.now();
    let attempts = 0;
    const storageKey = config.storageKey ? `techne:${config.storageKey}` : null;
    const editor = document.createElement("textarea");
    editor.rows = config.rows || 15;
    editor.spellcheck = false;
    editor.value = storageKey ? localStorage.getItem(storageKey) ?? config.starter : config.starter;
    editor.addEventListener("input", () => {
      if (storageKey) localStorage.setItem(storageKey, editor.value);
    });

    const run = document.createElement("button");
    run.type = "button";
    run.textContent = "Lancer les tests";
    const summary = document.createElement("p");
    const details = document.createElement("ul");

    function execute() {
      run.disabled = true;
      details.replaceChildren();
      summary.textContent = "Exécution…";
      const url = URL.createObjectURL(new Blob([workerSource], { type: "text/javascript" }));
      const worker = new Worker(url);
      const stop = () => {
        worker.terminate();
        URL.revokeObjectURL(url);
        run.disabled = false;
      };
      const timer = setTimeout(() => {
        stop();
        attempts += 1;
        summary.textContent = "Délai dépassé : boucle infinie possible.";
        window.Progress?.send({ kind: "exercise", activity: config.storageKey || config.fn, attempt: attempts, error: "timeout", code: editor.value });
      }, config.timeoutMs || 2000);

      worker.onmessage = (event) => {
        clearTimeout(timer);
        stop();
        attempts += 1;
        if (event.data.error) {
          summary.textContent = event.data.error;
          window.Progress?.send({ kind: "exercise", activity: config.storageKey || config.fn, attempt: attempts, error: event.data.error, code: editor.value });
          return;
        }

        const normalize = config.normalize || ((value) => value);
        let passed = 0;
        const failing = [];
        config.tests.forEach((test, index) => {
          const actual = event.data.output[index];
          const item = document.createElement("li");
          const matches = !actual.error && same(normalize(actual.value), normalize(test.expect));
          if (matches) {
            passed += 1;
            item.textContent = `✓ ${test.name || `test ${index + 1}`}`;
          } else {
            const reason = actual.error || `attendu ${JSON.stringify(test.expect)}, obtenu ${JSON.stringify(actual.value)}`;
            item.textContent = `✗ ${test.name || `test ${index + 1}`} — ${reason}`;
            failing.push(test.name || String(index + 1));
          }
          item.className = matches ? "pass" : "fail";
          details.append(item);
        });
        summary.textContent = `${passed}/${config.tests.length} tests réussis.`;
        window.Progress?.send({
          kind: "exercise",
          activity: config.storageKey || config.fn,
          fn: config.fn,
          attempt: attempts,
          passed,
          total: config.tests.length,
          failing,
          secondsSinceOpen: Math.round((Date.now() - openedAt) / 1000),
          code: editor.value,
        });
      };
      worker.postMessage({ code: editor.value, fn: config.fn, args: config.tests.map((test) => test.args) });
    }

    run.addEventListener("click", execute);
    editor.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && (event.metaKey || event.ctrlKey)) {
        event.preventDefault();
        execute();
      }
    });
    root.append(editor, run, summary, details);
  }

  window.Exercise = { mount };
})();
