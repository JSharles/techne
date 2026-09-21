# Deux questions sur un tableau

Tu vas écrire deux fonctions dans `duplicates.ts`, une pour chaque question de la leçon.

- `hasDuplicate(values)` répond à « est-ce qu'il y en a au moins un ? ». Elle renvoie `true` si une valeur apparaît au moins deux fois.
- `allWithin(values, min, max)` répond à « est-ce que c'est vrai pour tout le monde ? ». Elle renvoie `true` si chaque valeur est comprise entre `min` et `max`, bornes incluses.

Pour cet exercice, n'utilise pas `.some()`, `.every()`, `.includes()`, `.indexOf()` ni `new Set(values).size` : c'est la boucle qu'on travaille. Pour `hasDuplicate`, garde en mémoire les valeurs déjà vues dans un `Set`.

Tu as fini quand les 10 tests passent :

```
node --test duplicates.test.ts
```
