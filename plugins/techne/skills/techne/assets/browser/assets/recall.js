(function () {
  function mount(root, config) {
    root.classList.add("activity", "recall");
    const prompt = document.createElement("div");
    prompt.className = "prompt";
    prompt.innerHTML = config.prompt;

    const answer = document.createElement("textarea");
    answer.rows = config.rows || 5;
    answer.placeholder = window.I18n.t("recall.placeholder");
    answer.spellcheck = false;
    answer.autocapitalize = "off";
    answer.autocomplete = "off";

    // Code is written here, so the box behaves like an editor: Tab indents
    // instead of leaving the field, and the box grows with the answer.
    const grow = () => {
      answer.style.height = "auto";
      answer.style.height = `${Math.max(answer.scrollHeight, 120)}px`;
    };
    answer.addEventListener("input", grow);
    answer.addEventListener("keydown", (event) => {
      if (event.key !== "Tab") return;
      event.preventDefault();
      const { selectionStart: from, selectionEnd: to, value } = answer;
      if (event.shiftKey) {
        const lineStart = value.lastIndexOf("\n", from - 1) + 1;
        if (value.slice(lineStart, lineStart + 2) !== "  ") return;
        answer.value = value.slice(0, lineStart) + value.slice(lineStart + 2);
        answer.selectionStart = answer.selectionEnd = Math.max(from - 2, lineStart);
      } else {
        answer.value = `${value.slice(0, from)}  ${value.slice(to)}`;
        answer.selectionStart = answer.selectionEnd = from + 2;
      }
      grow();
    });

    const button = document.createElement("button");
    button.type = "button";
    button.textContent = window.I18n.t("recall.compare");

    const model = document.createElement("div");
    model.className = "model";
    model.hidden = true;
    model.innerHTML = config.model;

    button.addEventListener("click", () => {
      if (!answer.value.trim()) {
        answer.focus();
        return;
      }
      model.hidden = false;
      button.disabled = true;
      window.Progress?.send({
        kind: "recall",
        activity: config.id || "recall",
        prompt: prompt.textContent.slice(0, 240),
        answer: answer.value,
      });
    });

    root.append(prompt, answer, button, model);
  }

  window.Recall = { mount };
})();
