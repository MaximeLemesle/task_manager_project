# TaskManager Project

## Phase 1: Analyse et conception

**1. Quelles sont les entités principales ?**

- **Task** : représente une tâche (titre, description, priorité, statut, dates, etc.)
- **Project** : regroupe des tâches par projet (optionnel, simple)

**2. Quelles dépendances externes identifiez-vous ?**

- Fichier JSON (sauvegarde/chargement)
- smtplib (simulation email)

**3. Quels cas d'erreur faut-il prévoir ?**

- Titre de tâche vide ou priorité invalide
- Tâche inexistante
- Erreur lecture/écriture fichier
- Email invalide

**4. Comment organiser le code pour faciliter les tests ?**

- Séparation claire du code source et des tests
- Nomenclature en snake_case et camelCase
- Classes et méthodes testables indépendamment
- Services externes isolés pour le mocking

## Phase 4: Qualité et automatisation

### Étape 10: Atteindre 95% de couverture

**Couverture actuelle: 86%**

src/task_manager/**init**.py 100%
src/task_manager/manager.py 69%
src/task_manager/project.py 100%
src/task_manager/services.py 92%
src/task_manager/task.py 100%

- **Quelles lignes ne sont pas testées ?**

  - Certaines exceptions dans `manager.py` (69% seulement, les lignes 30-34, 41-42, 49-56, 59-69 ne sont pas testées)
  - Quelques erreur dans `services.py` (92% de testé)

- **Quels cas d'erreur manquent ?**

  - Tests d'exceptions lors de l'écriture/lecture de fichiers (IOError)
  - Cas d'erreur lors de l'export CSV dans `ReportService`
  - Cas d'erreur lors de la génération de rapport si données invalides

- **Y a-t-il du code mort ?**
  - Non, mais certains blocs ne sont pas testés.

### Ajout des tests manquants

**Nouvelle couverture: 96%**

src/task_manager/**init**.py 100%
src/task_manager/manager.py 91%
src/task_manager/project.py 100%
src/task_manager/services.py 98%
src/task_manager/task.py 100%
