(function () {
  function mount(root, config) {
    root.classList.add("activity");
    const table = document.createElement("table");
    const head = document.createElement("tr");
    [window.I18n.t("trace.iteration"), ...config.columns].forEach((label) => {
      const cell = document.createElement("th");
      cell.textContent = label;
      head.append(cell);
    });
    table.append(head);

    const inputs = [];
    config.rows.forEach((row, rowIndex) => {
      const line = document.createElement("tr");
      const iteration = document.createElement("td");
      iteration.textContent = String(rowIndex + 1);
      line.append(iteration);
      row.forEach((expected, columnIndex) => {
        const cell = document.createElement("td");
        const given = config.given?.[rowIndex]?.[columnIndex];
        if (given) {
          cell.textContent = expected;
        } else {
          const input = document.createElement("input");
          input.dataset.expected = expected;
          input.setAttribute("aria-label", window.I18n.t("trace.cellLabel", { column: config.columns[columnIndex], row: rowIndex + 1 }));
          inputs.push(input);
          cell.append(input);
        }
        line.append(cell);
      });
      table.append(line);
    });

    const button = document.createElement("button");
    button.type = "button";
    button.textContent = window.I18n.t("trace.check");
    const result = document.createElement("p");
    button.addEventListener("click", () => {
      let correct = 0;
      const wrong = [];
      inputs.forEach((input) => {
        const matches = input.value.replace(/\s/g, "") === input.dataset.expected.replace(/\s/g, "");
        input.classList.toggle("correct", matches);
        input.classList.toggle("wrong", !matches);
        if (matches) correct += 1;
        else wrong.push({ cell: input.getAttribute("aria-label"), value: input.value });
      });
      result.textContent = window.I18n.t("trace.summary", { correct, total: inputs.length });
      window.Progress?.send({ kind: "trace", activity: config.id || "trace", correct, total: inputs.length, wrong });
    });

    root.append(table, button, result);
  }

  window.Trace = { mount };
})();
