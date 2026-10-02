---
id: frontend-senior
title: Frontend senior
version: 4
activity_kinds: code, browser, oral, writing
lesson_to_practice: balanced
timeboxes: lesson=10, exercise=30, review=5, placement=15
red_thread: no
survey_ceiling: discovered
---

# Frontend senior

## Outcome and boundary

Pour un développeur React/Node qui veut atteindre le niveau technique d'un frontend senior : comprendre
en profondeur le langage, le navigateur et React, écrire du code correct à partir d'une page blanche,
travailler avec aisance dans une base de code existante, et concevoir une application frontend en
défendant ses choix.

Hors du programme, volontairement : la préparation aux entretiens, le backend, l'infrastructure, les
algorithmes de concours et la programmation dynamique. L'édition collaborative temps réel et quelques
mécanismes avancés du langage sont traités en survol seulement.

Le programme est autonome : un inconnu doit pouvoir le suivre seul. Il garde ses propres preuves : ce
qui a été démontré dans un autre programme ne compte pas ici.

## Sequence

### Unité 1 — Le langage

- Valeurs et références, closures, portée et hoisting : var, let, const, zone morte temporelle.
- Le mot-clé this, et sa préservation par call, apply et bind.
- Fonctions d'ordre supérieur, paramètres du reste, décomposition, valeurs par défaut.
- Égalité stricte et coercition. null, undefined et variable non déclarée.
- Classes et prototypes. Modules CommonJS et modules ES.
- La mémoire : ce qui garde un objet en vie, WeakMap et WeakSet, les fuites classiques d'une page.

### Unité 2 — Asynchrone et temps

- La boucle d'événements : pile d'appels, file de tâches, file de microtâches, ordre d'exécution.
- Promesses, async et await, propagation et capture des erreurs asynchrones.
- Minuteries, leurs identifiants et leur annulation.

### Unité 3 — Utilitaires JavaScript

- Écrire de zéro, avec leurs cas limites : Classnames, Flatten, Curry, Deep Equal, Deep Clone, Memoize,
  Debounce, Throttle, Event Emitter, Promise.all, Map Async Limit.

### Unité 4 — Structures de données et coût

- Tableaux, tables de hachage (Map, Set), piles, files, arbres.
- Le coût en temps et en mémoire de chaque opération.

### Unité 5 — Le navigateur

- DOM : parcours, création, manipulation.
- Propagation des événements, capture et remontée, puis délégation.
- fetch et AbortController. Chargement des scripts : classique, async, defer. Stockage : cookies,
  localStorage, sessionStorage.
- Du HTML aux pixels : chemin critique de rendu, puis mise en page, peinture et composition.
- Sécurité côté navigateur : XSS et CSP, CSRF et CORS, où garder un jeton d'authentification.

### Unité 6 — HTTP et le dialogue avec le back

- HTTP : méthodes, codes de statut, en-têtes, et ce que chacun engage.
- Authentification côté navigateur : cookie de session ou jeton, rafraîchissement, déconnexion.
- Consommer une API : pagination, limitation de débit, envoi de fichiers, temps réel par WebSocket.
- Quand l'API échoue : distinguer une panne d'une erreur métier, réessayer sans dupliquer l'effet,
  expiration et idempotence.
- Sécurité : dépendances vulnérables, validation des entrées, données sensibles exposées côté client.

### Unité 7 — HTML, formulaires, accessibilité

- HTML sémantique, validation et soumission de formulaire.
- Rôles, états et propriétés ARIA, interactions clavier attendues par motif, gestion du focus.
- Vérifier l'accessibilité d'une page : lecteur d'écran, clavier seul, outils d'audit, et leurs limites.

### Unité 8 — CSS

- Modèle de boîte, sélecteurs, spécificité, positionnement, unités.
- Flexbox, Grid, propriétés personnalisées, mise en page adaptative.
- Contexte d'empilement, conteneurs de défilement et débordement.

### Unité 9 — TypeScript pour le frontend

- Rétrécissement de type, unions discriminées, prédicats de type.
- Modéliser l'état d'une interface comme une machine à états, dont chaque état ne porte que les données
  qu'il possède vraiment.
- Génériques, keyof et accès indexé, types utilitaires.
- Typer des props, des hooks et des composants génériques.

### Unité 10 — React en profondeur

- Le modèle de rendu, l'identité des composants, la réconciliation et les clés.
- État local et dérivé, réducteurs, contexte ou magasin externe.
- Effets et leurs alternatives, useLayoutEffect, références, règles des hooks, hooks personnalisés.
- Formulaires et champs contrôlés, mémoïsation, coût d'un rendu.
- Composition, error boundaries, portails, Suspense et découpage du code.
- États de chargement, d'erreur et de vide, conditions de course.

### Unité 11 — Composants d'interface

- Construire de zéro, avec une passe d'accessibilité : Todo List, Accordion, Nested Checkboxes,
  Contact Form, Tic-tac-toe, Image Carousel, Job Board, File Explorer, Data Table.
- Todo List et Accordion refaits sans framework, en DOM natif.

### Unité 12 — Rendu et données avec Next.js

- Rendu côté client, côté serveur, à la génération, et le choix entre eux. Hydratation.
- Composants serveur et composants client. Chargement des données, cache et invalidation.
- L'App Router : arborescence de routes, layouts imbriqués, états de chargement et d'erreur.
- La frontière entre serveur et client : ce qui la traverse, ce qui ne doit pas la traverser.
- Le middleware, et ce qu'il peut faire avant qu'une page ne soit rendue.
- Les métadonnées d'une page, et ce que les moteurs et les réseaux sociaux en lisent.
- Analyser le bundle d'une application rendue côté serveur, et tenir une application en production :
  pannes partielles, caches périmés, reprises après erreur.

### Unité 13 — Structure du code et frontières

- Où vit une responsabilité : découpage par fonctionnalité, code partagé, modules et leurs frontières.
- Qui possède quel état, et ce que coûte un état possédé trop haut ou trop bas.
- Quand ne pas ajouter d'architecture : l'abstraction qu'on n'écrit pas, la bibliothèque d'état dont on
  n'a pas besoin, la couche qui ne sert qu'une fois.
- Lire une structure existante et dire ce qu'elle rend facile et ce qu'elle rend pénible.

### Unité 14 — Performance

- Core Web Vitals : LCP, INP, CLS, ce qu'ils mesurent et ce qui les dégrade.
- Mesurer avant d'optimiser : l'onglet Performance, Lighthouse, les mesures de terrain.
- Poids du bundle, images et polices, virtualisation des longues listes.
- Observer une application en production : erreurs, mesures réelles des utilisateurs.

### Unité 15 — Tests et débogage

- Quoi tester, et le comportement plutôt que l'implémentation.
- Tests unitaires, d'intégration et de bout en bout, doublures de test.
- Tester un composant React du point de vue de l'utilisateur.
- Déboguer dans l'ordre : symptôme, preuve, cause racine, correction, puis ce qui empêche son retour.
- Les instruments : onglet réseau, profileur, source maps, historique Git.

### Unité 16 — Travailler dans une base de code existante

- Lire un code qu'on découvre, reproduire un bug, le diagnostiquer avec le débogueur.
- Ajouter une fonctionnalité en respectant les conventions et les tests en place.
- Relire une pull request : ce qui bloque, ce qui se discute, ce qui se laisse passer.
- Auditer une page en performance et en accessibilité, et prioriser les corrections.

### Unité 17 — Concevoir une application frontend

- Une démarche de conception : besoins, architecture, modèle de données, interfaces, optimisations.
- Les briques transverses : pagination, cache client, défilement infini et virtualisation, mise à jour
  optimiste, temps réel, images.
- Des cas : Autocomplete, News Feed, Pinterest, E-commerce, Travel Booking, un design system, un tableau
  de bord temps réel.

## Subject catalogue

### JavaScript and the runtime — `fejs.*`

`values-references`, `closures`, `hoisting-scope`, `this-binding`, `call-apply-bind`,
`higher-order-functions`, `rest-spread-defaults`, `equality-coercion`, `null-undefined`,
`classes-prototypes`, `modules`, `memory`, `weak-collections`, `event-loop`, `promises`, `errors`,
`timers`

### DSA — `fedsa.*`

`arrays`, `hashing`, `stack`, `queue`, `trees`, `big-o`

### Browser — `web.*`

`dom-traversal`, `dom-manipulation`, `event-propagation`, `event-delegation`, `fetch-abort`,
`script-loading`, `browser-storage`, `critical-rendering-path`, `layout-paint-composite`,
`http-semantics`, `auth-flows`, `api-pagination`, `rate-limiting`, `websockets`, `file-uploads`,
`api-failures-retries`, `xss-csp`, `csrf-cors`, `token-storage`, `dependency-vulnerabilities`,
`input-validation`, `sensitive-data-exposure`

### HTML and accessibility — `html.*`

`semantic-html`, `forms`, `aria`, `keyboard-interaction`, `focus-management`, `accessibility-testing`

### CSS — `css.*`

`box-model`, `selectors-specificity`, `positioning`, `units`, `flexbox`, `grid`, `custom-properties`,
`responsive-layout`, `stacking-context`, `overflow-scrolling`

### TypeScript — `fets.*`

`narrowing`, `discriminated-unions`, `state-modelling`, `type-predicates`, `generics`, `keyof-indexed`,
`utility-types`, `react-typing`

### React — `fereact.*`

`render-model`, `component-identity`, `reconciliation-keys`, `state-local-derived`, `reducer`,
`context-vs-store`, `effects-and-alternatives`, `layout-effect`, `refs`, `hooks-rules`, `custom-hooks`,
`controlled-inputs`, `forms`, `memoization`, `render-performance`, `composition`, `error-boundaries`,
`portals`, `suspense-code-splitting`, `async-ui-states`, `race-conditions`, `behaviour-tests`

### Next.js — `fenext.*`

`rendering-strategies`, `hydration`, `server-client-components`, `data-fetching`, `caching-invalidation`,
`app-router`, `layouts`, `error-loading-states`, `request-boundaries`, `middleware`, `metadata`,
`bundle-analysis`, `production-resilience`

### Web performance — `perf.*`

`core-web-vitals`, `measuring`, `bundle-size`, `images-fonts`, `list-virtualization`,
`production-observability`

### Tests and debugging — `fetest.*`

`what-to-test`, `behaviour-vs-implementation`, `unit`, `integration`, `end-to-end`, `test-doubles`,
`reproduce`, `debugger`, `root-cause`, `devtools`, `git-history`

### Code structure and boundaries — `struct.*`

`module-boundaries`, `state-ownership`, `feature-slicing`, `shared-code`, `when-not-to-abstract`,
`reading-a-structure`

### JavaScript utilities — `util.*`

`classnames`, `flatten`, `curry`, `deep-equal`, `deep-clone`, `memoize`, `debounce`, `throttle`,
`event-emitter`, `promise-all`, `map-async-limit`

### Interface components — `ui.*`

`todo-list`, `accordion`, `nested-checkboxes`, `contact-form`, `tic-tac-toe`, `image-carousel`,
`job-board`, `file-explorer`, `data-table`, `vanilla-dom`

### Existing codebases — `codebase.*`

`reading-unfamiliar-code`, `feature-in-conventions`, `pull-request-review`, `performance-audit`,
`accessibility-audit`

### Frontend application design — `fedesign.*`

`requirements`, `architecture`, `data-model`, `interfaces`, `optimizations`, `pagination`,
`client-cache`, `infinite-scroll`, `optimistic-updates`, `realtime-transport`, `case-autocomplete`,
`case-news-feed`, `case-pinterest`, `case-ecommerce`, `case-travel-booking`, `case-design-system`,
`case-realtime-dashboard`

### Survey — `fesurvey.*`

`collaborative-editing`, `iterators-generators`, `symbols`, `property-descriptors`, `proxies`, `workers`,
`polyfills`, `strict-mode`

## Question bank

Des questions courantes, telles que GreatFrontEnd les pose, comme repère de ce qu'un frontend senior sait
expliquer. Leurs dépôts n'ont pas de licence : Techne ne recopie jamais ni la question ni la réponse, il
écrit les siennes à partir des sources primaires (MDN, react.dev, les spécifications). Liens vérifiés le
2026-09-22.

| Sujet | Question d'origine |
| --- | --- |
| `fejs.closures` | https://www.greatfrontend.com/questions/quiz/what-is-a-closure-and-how-why-would-you-use-one |
| `fejs.this-binding` | https://www.greatfrontend.com/questions/quiz/explain-how-this-works-in-javascript |
| `fejs.call-apply-bind` | https://www.greatfrontend.com/questions/quiz/whats-the-difference-between-call-and-apply |
| `fejs.call-apply-bind` | https://www.greatfrontend.com/questions/quiz/explain-function-prototype-bind |
| `fejs.higher-order-functions` | https://www.greatfrontend.com/questions/quiz/what-is-the-definition-of-a-higher-order-function |
| `fejs.rest-spread-defaults` | https://www.greatfrontend.com/questions/quiz/what-are-the-benefits-of-using-spread-syntax-and-how-is-it-different-from-rest-syntax |
| `fejs.classes-prototypes` | https://www.greatfrontend.com/questions/quiz/explain-how-prototypal-inheritance-works |
| `fejs.hoisting-scope` | https://www.greatfrontend.com/questions/quiz/what-are-the-differences-between-variables-created-using-let-var-or-const |
| `fejs.hoisting-scope` | https://www.greatfrontend.com/questions/quiz/explain-the-difference-in-hoisting-between-var-let-and-const |
| `fejs.equality-coercion` | https://www.greatfrontend.com/questions/quiz/what-is-the-difference-between-double-equal-and-triple-equal |
| `fejs.null-undefined` | https://www.greatfrontend.com/questions/quiz/whats-the-difference-between-a-variable-that-is-null-undefined-or-undeclared-how-would-you-go-about-checking-for-any-of-these-states |
| `fesurvey.strict-mode` | https://www.greatfrontend.com/questions/quiz/what-is-use-strict-what-are-the-advantages-and-disadvantages-to-using-it |
| `fejs.modules` | https://www.greatfrontend.com/questions/quiz/explain-the-differences-between-commonjs-modules-and-es-modules |
| `fesurvey.polyfills` | https://www.greatfrontend.com/questions/quiz/what-are-javascript-polyfills-for |
| `fesurvey.iterators-generators` | https://www.greatfrontend.com/questions/quiz/what-are-iterators-and-generators-and-what-are-they-used-for |
| `fesurvey.symbols` | https://www.greatfrontend.com/questions/quiz/what-are-symbols-used-for |
| `fesurvey.property-descriptors` | https://www.greatfrontend.com/questions/quiz/what-are-javascript-object-property-flags-and-descriptors |
| `fesurvey.property-descriptors` | https://www.greatfrontend.com/questions/quiz/what-are-javascript-object-getters-and-setters-for |
| `fesurvey.proxies` | https://www.greatfrontend.com/questions/quiz/what-are-proxies-in-javascript-used-for |
| `fejs.event-loop` | https://www.greatfrontend.com/questions/quiz/what-is-event-loop-what-is-the-difference-between-call-stack-and-task-queue |
| `fejs.promises` | https://www.greatfrontend.com/questions/quiz/what-are-the-pros-and-cons-of-using-promises-instead-of-callbacks |
| `web.fetch-abort` | https://www.greatfrontend.com/questions/quiz/what-are-the-differences-between-xmlhttprequest-and-fetch |
| `web.fetch-abort` | https://www.greatfrontend.com/questions/quiz/how-do-you-abort-a-web-request-using-abortcontrollers |
| `fesurvey.workers` | https://www.greatfrontend.com/questions/quiz/what-are-workers-in-javascript-used-for |
| `fedsa.hashing` | https://www.greatfrontend.com/questions/quiz/what-is-the-difference-between-a-map-object-and-a-plain-object-in-javascript |
| `fejs.weak-collections` | https://www.greatfrontend.com/questions/quiz/what-are-the-differences-between-map-set-and-weakmap-weakset |
| `fejs.memory` | https://www.greatfrontend.com/questions/quiz/how-does-javascript-garbage-collection-work |
| `web.script-loading` | https://www.greatfrontend.com/questions/quiz/describe-the-difference-between-script-async-and-script-defer |
| `web.event-propagation` | https://www.greatfrontend.com/questions/quiz/describe-event-bubbling |
| `web.event-propagation` | https://www.greatfrontend.com/questions/quiz/describe-event-capturing |
| `web.event-delegation` | https://www.greatfrontend.com/questions/quiz/explain-event-delegation |
| `web.browser-storage` | https://www.greatfrontend.com/questions/quiz/describe-the-difference-between-a-cookie-sessionstorage-and-localstorage |
| `fereact.render-model` | https://www.greatfrontend.com/questions/quiz/what-does-re-rendering-mean-in-react |
| `fereact.effects-and-alternatives` | https://www.greatfrontend.com/questions/quiz/what-does-the-dependency-array-of-useeffect-affect |
| `fereact.refs` | https://www.greatfrontend.com/questions/quiz/what-is-the-useref-hook-in-react-and-when-should-it-be-used |
| `fereact.reconciliation-keys` | https://www.greatfrontend.com/questions/quiz/what-is-the-purpose-of-the-key-prop-in-react |
| `fereact.reconciliation-keys` | https://www.greatfrontend.com/questions/quiz/what-is-the-consequence-of-using-array-indices-as-the-value-for-key-s-in-react |
| `fereact.controlled-inputs` | https://www.greatfrontend.com/questions/quiz/what-is-the-difference-between-controlled-and-uncontrolled-react-components |
| `fereact.memoization` | https://www.greatfrontend.com/questions/quiz/what-is-the-usememo-hook-in-react-and-when-should-it-be-used |
| `fereact.memoization` | https://www.greatfrontend.com/questions/quiz/what-is-the-usecallback-hook-in-react-and-when-should-it-be-used |
| `fereact.async-ui-states` | https://www.greatfrontend.com/questions/quiz/what-are-some-common-pitfalls-when-doing-data-fetching-in-react |
| `fereact.hooks-rules` | https://www.greatfrontend.com/questions/quiz/what-are-the-rules-of-react-hooks |
| `fereact.reducer` | https://www.greatfrontend.com/questions/quiz/what-is-the-usereducer-hook-in-react-and-when-should-it-be-used |
| `fereact.layout-effect` | https://www.greatfrontend.com/questions/quiz/what-is-the-difference-between-useeffect-and-uselayouteffect-in-react |
| `fereact.reconciliation-keys` | https://www.greatfrontend.com/questions/quiz/what-is-reconciliation-in-react |
| `fereact.reconciliation-keys` | https://www.greatfrontend.com/questions/quiz/how-does-virtual-dom-in-react-work-what-are-its-benefits-and-downsides |
| `fereact.composition` | https://www.greatfrontend.com/questions/quiz/explain-the-composition-pattern-in-react |
| `fereact.composition` | https://www.greatfrontend.com/questions/quiz/what-are-higher-order-components-in-react |
| `fereact.composition` | https://www.greatfrontend.com/questions/quiz/what-are-render-props-in-react-and-what-are-they-for |
| `fereact.error-boundaries` | https://www.greatfrontend.com/questions/quiz/what-are-error-boundaries-in-react-for |
| `fereact.portals` | https://www.greatfrontend.com/questions/quiz/what-are-react-portals-used-for |
| `fereact.suspense-code-splitting` | https://www.greatfrontend.com/questions/quiz/what-is-react-suspense-and-what-does-it-enable |
| `fereact.suspense-code-splitting` | https://www.greatfrontend.com/questions/quiz/what-is-code-splitting-in-a-react-application |
| `fereact.behaviour-tests` | https://www.greatfrontend.com/questions/quiz/how-do-you-test-react-applications |
| `fenext.rendering-strategies` | https://www.greatfrontend.com/questions/quiz/explain-server-side-rendering-of-react-applications-and-its-benefits |
| `fenext.rendering-strategies` | https://www.greatfrontend.com/questions/quiz/explain-static-generation-of-react-applications-and-its-benefits |
| `fenext.hydration` | https://www.greatfrontend.com/questions/quiz/explain-what-react-hydration-is |
| `fereact.context-vs-store` | https://www.greatfrontend.com/questions/quiz/how-do-you-decide-between-using-react-state-context-and-external-state-managers |

## Design readings

Tirées de la liste « awesome-front-end-system-design » de GreatFrontEnd (licence MIT) : uniquement des
ressources gratuites. Liens vérifiés le 2026-09-22.

| Sujet | Lecture |
| --- | --- |
| `fedesign.architecture` | https://www.greatfrontend.com/system-design/framework |
| `fedesign.architecture` | https://www.frontendinterviewhandbook.com/front-end-system-design/ |
| `fedesign.case-news-feed` | https://www.greatfrontend.com/questions/system-design/news-feed-facebook |
| `fedesign.case-news-feed` | https://engineering.fb.com/2020/05/08/web/facebook-redesign/ |
| `fedesign.pagination` | https://slack.engineering/evolving-api-pagination-at-slack |
| `fedesign.case-autocomplete` | https://www.greatfrontend.com/questions/system-design/autocomplete |
| `fedesign.case-autocomplete` | https://engineering.fb.com/2010/05/17/web/the-life-of-a-typeahead-query/ |
| `fedesign.case-autocomplete` | https://adamsilver.io/blog/building-an-accessible-autocomplete-control/ |
| `fedesign.case-pinterest` | https://github.com/pinterest/gestalt/blob/master/packages/gestalt/src/Masonry/README.md |
| `fedesign.case-pinterest` | https://gestalt.pinterest.systems/web/masonry |
| `fedesign.case-ecommerce` | https://web.dev/shopping-for-speed-on-ebay/ |
| `fedesign.case-ecommerce` | https://web.dev/payment-and-address-form-best-practices/ |
| `fedesign.case-travel-booking` | https://web.dev/make-my-trip/ |
| `fesurvey.collaborative-editing` | https://www.figma.com/blog/how-figmas-multiplayer-technology-works/ |
| `fesurvey.collaborative-editing` | https://www.figma.com/blog/realtime-editing-of-ordered-sequences/ |

## Adaptation rules

- Le langage et l'asynchrone viennent avant les utilitaires ; le navigateur et HTTP avant les composants
  et les données ; React avant le rendu, la structure du code et la performance ; les unités de base
  avant le travail dans une base de code existante et la conception.
- Les utilitaires et les composants sont le terrain d'exercice des concepts : après un sujet enseigné,
  choisir celui qui le met en jeu, par exemple Debounce après les minuteries, Nested Checkboxes après la
  délégation d'événements.
- Le travail dans une base de code existante commence dès que le navigateur et React ont leurs bases, et
  revient régulièrement ensuite plutôt que d'attendre son unité.
- C'est là que se fait le transfert : ce programme n'a pas de projet fil rouge. Quand un sujet devient
  autonome, une séance de base de code existante le remet en jeu dans la semaine qui suit, sans annoncer
  lequel : un bug à corriger, une fonctionnalité à ajouter ou une pull request à relire qui le mobilise.
  Réussi sans aide, ce travail vaut transféré.
- Un sujet déjà démontré dans ce programme passe directement à l'exercice qui le mobilise, à difficulté
  plus haute.
- La structure du code s'enseigne sur du code déjà écrit : les composants de ce programme, ou une base de
  code existante, jamais sur un schéma abstrait.
- Les sujets en survol se greffent sur les leçons des unités voisines et n'ont jamais d'unité à eux.
