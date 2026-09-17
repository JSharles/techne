(function () {
  // Learner-facing browser strings. The page language comes from <html lang>,
  // which init_workspace.py sets from the learner's chosen language.
  // Unknown languages fall back to English; add a dictionary to support more.
  const messages = {
    en: {
      "eyebrow.curriculum": "TECHNE — CURRICULUM",
      "exercise.run": "Run tests",
      "exercise.running": "Running…",
      "exercise.timeout": "Time limit exceeded: possible infinite loop.",
      "exercise.undefinedFunction": "Function {fn} is not defined.",
      "exercise.syntaxError": "Syntax error: {detail}",
      "exercise.mismatch": "expected {expected}, got {actual}",
      "exercise.summary": "{passed}/{total} tests passed.",
      "quiz.correct": "Yes.",
      "quiz.wrong": "No.",
      "quiz.score": "{answered}/{total} answered · {correct} correct",
      "recall.placeholder": "Answer from memory before revealing the model…",
      "recall.compare": "Compare with the model",
      "trace.iteration": "iteration",
      "trace.cellLabel": "{column}, iteration {row}",
      "trace.check": "Check my trace",
      "trace.summary": "{correct}/{total} cells correct.",
    },
    fr: {
      "eyebrow.curriculum": "TECHNE — CURSUS",
      "exercise.run": "Lancer les tests",
      "exercise.running": "Exécution…",
      "exercise.timeout": "Délai dépassé : boucle infinie possible.",
      "exercise.undefinedFunction": "La fonction {fn} n'est pas définie.",
      "exercise.syntaxError": "Erreur de syntaxe : {detail}",
      "exercise.mismatch": "attendu {expected}, obtenu {actual}",
      "exercise.summary": "{passed}/{total} tests réussis.",
      "quiz.correct": "Oui.",
      "quiz.wrong": "Non.",
      "quiz.score": "{answered}/{total} répondues · {correct} correctes",
      "recall.placeholder": "Réponds de mémoire avant d’afficher le modèle…",
      "recall.compare": "Comparer avec le modèle",
      "trace.iteration": "itération",
      "trace.cellLabel": "{column}, itération {row}",
      "trace.check": "Vérifier ma trace",
      "trace.summary": "{correct}/{total} cases correctes.",
    },
  };

  const primary = (document.documentElement.lang || "en").toLowerCase().split("-")[0];
  const active = messages[primary] || messages.en;

  function t(key, params = {}) {
    const template = active[key] ?? messages.en[key] ?? key;
    return template.replace(/\{(\w+)\}/g, (match, name) => (name in params ? String(params[name]) : match));
  }

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });

  window.I18n = { t };
})();
