(function () {
  function mount(root, config) {
    root.classList.add("activity", "recall");
    const prompt = document.createElement("div");
    prompt.className = "prompt";
    prompt.innerHTML = config.prompt;

    const answer = document.createElement("textarea");
    answer.rows = config.rows || 5;
    answer.placeholder = window.I18n.t("recall.placeholder");

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
