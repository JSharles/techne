---
type: llm
weight: 2
---

The response is Techne's message to a learner who asked to resume, in French, and should hand them the exercise described in `exercices/s01-j02-doublons/README.md`.

Pass only if all of these hold:

- it reads as a French-speaking developer would write to a colleague on Slack: complete sentences in short paragraphs, not a form;
- it has no bold label followed by a fragment (« **Maintenant :** … », « **Terminé quand :** … »), no chain of colons, no sentence without a verb, and no machinery word (learner, sonde, borne, preuve, assisté);
- it tells the learner what to do, how they will know they are done, and what to type if they are stuck, each inside a sentence;

The wording may differ freely. This is the reference for the expected tone:

> On passe à l'exercice sur les doublons. Il met en pratique ce que tu viens de voir dans la leçon : parcourir un tableau pour répondre à une question par oui ou par non.
>
> Tu vas écrire deux fonctions dans `duplicates.ts`. La première, `hasDuplicate`, dit si une valeur apparaît au moins deux fois. La seconde, `allWithin`, dit si toutes les valeurs sont comprises entre `min` et `max`. Le détail est dans le README du dossier, que je viens d'ouvrir.
>
> Compte une trentaine de minutes. Tu as fini quand les 10 tests passent avec `node --test duplicates.test.ts`. Si tu bloques, tape `/techne:hint`.

When failing, quote the sentence at fault.
