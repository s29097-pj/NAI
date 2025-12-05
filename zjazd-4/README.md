## Analiza jądra SVM — Wpływ parametrów

### Kernel - poly dał najlepszą dokładność

Wpływ parametrów na wyniki SVM:

- `C (Regularization parameter - regulatyzacja)`:
    - Im większa tym bardziej karze błędne dopasowania
    - Za duża morze wpłynąć  na nadmierne dopasowanie (overfitting), czyli bardo dobrze klasyfikować dane, na których 
  model się uczy, ale słabiej rozpoznawać nowe, spoza zbioru treningowego

- `class_weight`:
    - są to wagi klas, które możemy zdefiniować, by określić to jak ważne są

**Eksperyment:**

Zwiększając regularyzacje (C), do wartości 20, sprawiłem, że model stracił na swojej dokładności. Jest to spowodowane overfittingiem.

Ponieważ klasa AB jest rzadsza (20 próbek vs 41 dla NO), zwiększyliśmy jej wagę w parametrze class_weight, np. 
do {'AB': 10, 'NO': 1}. Daliśmy tak dużą wagę przy AB, by widoczna była różnica w ilości pomyłek.
Rzeczywiście źle sklasyfikowanych elementów jako AB jest mniej. Jednocześnie jednak nie wpłyneło to
na ilość poprawnie sklasyfikowanych elementów jako klasy AB.
Widać tutaj, że choć błędna klasyfikacja klasy AB, była bardziej karana, to jednak nie wpłyneło to, na ilość elementów,
ktore zostały sklasyfikowane poprawnie jako klasa AB. Mamy więc mniej sklasyfikowanych elemetów, co do,których jednak
mamy większą pewność, że należą do klasy AB, lecz kosztem elemntów, co do, których pewność ta była mniejsza, mimo, że
rzeczywiście należały do tej klasy.
