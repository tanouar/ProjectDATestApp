
Concernant la structure du rendu final, je souhaiterai que la structure du dossier soit la suivante (ceci est un exemple vous pouvez avoir plus de notebooks) :

```
projet/
│
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_DataViz.ipynb
│   ├── 03_preProcessing.ipynb
│   └── 04_modelisation.ipynb
│
├── datasets/
│   ├── data.csv
│   └── data_clean.csv
│
├── rapport/
│   ├── rapport_word.docx
│   └── rapport_pdf.pdf
│
└── requirements.txt
```

Dans cette structure, nous avons un dossier notebooks contenant les notebooks numérotés par ordre d'exécution. Les données sont stockées dans le dossier datasets, et les rapports au format Word et PDF sont dans le dossier rapport. Enfin, le fichier requirements.txt contient la liste des dépendances nécessaires pour exécuter les notebooks, voir l'exemple ci-dessous :
```
matplotlib
numpy
pandas
scipy
seaborn
scikit-learn
```

Cela inclut les bibliothèques couramment utilisées pour l'analyse de données et l'apprentissage automatique. Vous pouvez ajouter d'autres bibliothèques spécifiques au projet au fur et à mesure de vos besoins.Enfin veillez à ce que les notebooks s'exécute sans erreurs et définir le chemin relatif des dataset lors du chargement avec pandas, voir exemple ci-dessous :
```python
df = pd.read_csv('../datasets/data.csv')
```