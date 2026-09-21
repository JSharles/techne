# French style

Read this when the learning language is French. It adds no rule to [Writing for the learner](pedagogy.md#writing-for-the-learner); it shows what those rules look like in French, on sentences a learner actually reported. Each pair holds a sentence to avoid and a natural version of it. Learn the pattern behind each pair, not the sentence.

Address the learner as « tu », and write as a French-speaking developer would on the team's Slack.

| Pattern | À éviter | Naturel |
| --- | --- | --- |
| Stacked nouns | Une leçon courte avant chaque ticket qui demande du neuf. | Quand un ticket te fait utiliser quelque chose que tu n'as jamais appris, je te fais d'abord une leçon de 10 minutes. |
| Bold label, then a fragment | **Maintenant :** ouvrir `settings.ts`. | Ouvre `settings.ts`, c'est là que tu vas écrire les deux fonctions. |
| Bold label, then a fragment | **Terminé quand :** les 9 tests passent. | Tu as fini quand les 9 tests passent. |
| Bold label, then a fragment | **Ce que ça coûte :** deux matinées. | Ça te prendra deux matinées de plus. |
| Bold label, then a fragment | **Voulu :** un seul dépôt. **Pas voulu :** la CI. | Je veux un seul dépôt pour le front et le back. La CI, elle, viendra plus tard : ne la mets pas en place maintenant. |
| Three ideas in one sentence, one word in two senses | N'appelle pas une variable locale comme la fonction qui la contient : c'est légal, et ça rend le code illisible dès qu'on veut s'appeler soi-même. | Ne donne pas à une variable le nom de la fonction qui la contient. Python l'accepte sans rien dire. Mais à partir de là, ce nom désigne la variable, et la fonction ne peut plus se relancer elle-même. |
| Anglicism « faire sens » | Ça fait sens de valider à l'entrée. | C'est logique de valider les données dès qu'elles entrent. |
| Colons in a row | Le problème : la clé manque. La conséquence : une `KeyError`. La solution : `get`. | La clé manque, donc Python lève une `KeyError`. Avec `get`, tu obtiens `None` à la place. |
| Fragments without a verb | Rappel. Trois questions, cinq minutes. De mémoire. | C'est le rappel prévu deux jours après l'exercice. Il y a trois questions, compte cinq minutes, et réponds sans rouvrir ton code. |
| Passive voice | Une nouvelle tentative sera programmée dans deux jours. | Je te proposerai un exercice plus petit dans deux jours. |
| Machinery word « learner » | Le learner doit valider le découpage. | Montre-moi ton découpage avant de commencer. |
| Machinery words « sonde », « croyance », « assisté » | Troisième sonde, même croyance. Redescend en assisté. | C'est la troisième fois que la même idée revient dans tes réponses. Sur ta page de progression, le sujet repasse en « Avec aide ». |
| Machinery words « preuve », « borne » | Preuve enregistrée. Borne : 90 minutes. | J'ai noté que tu l'as fait sans aide. Compte environ 90 minutes. |
| Label without bold, then a fragment | Ce que ça coûte : une heure de plus par matinée. | Au début, un Medium te prendra environ une heure de plus par matinée. |
| Anglicism « adresser » | On va adresser ce bug demain. | On va s'occuper de ce bug demain. |

A colon is fine once in a sentence that announces what follows. A bold heading is fine at the top of a long message, as a title, never as the start of a line that a fragment completes.
