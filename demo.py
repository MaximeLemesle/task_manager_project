#!/usr/bin/env python3
"""
Démonstration du module TaskManager
"""
from src.task_manager.manager import TaskManager
from src.task_manager.task import Priority, Status
from src.task_manager.services import EmailService

def main():
    print("=== Démonstration TaskManager ===\n")

    # Création du gestionnaire
    manager = TaskManager("demo_tasks.json")

    # Ajout de tâches
    id1 = manager.add_task("Préparer le rapport", "Rédiger le rapport final", Priority.HIGH)
    id2 = manager.add_task("Envoyer l'email", "Notifier l'équipe", Priority.MEDIUM)
    id3 = manager.add_task("Nettoyer le bureau", "Avant la réunion", Priority.LOW)

    # Marquer une tâche comme terminée
    task1 = manager.get_task(id1)
    task1.mark_completed()

    # Afficher les statistiques
    stats = manager.get_statistics()
    print("Statistiques :")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    # Sauvegarder dans un fichier
    manager.save_to_file()
    print("\nTâches sauvegardées dans demo_tasks.json")

    # Recharger et vérifier
    manager2 = TaskManager("demo_tasks.json")
    manager2.load_from_file()
    print(f"\nTâches rechargées : {len(manager2.tasks)}")
    for t in manager2.tasks:
        print(f"- {t.title} ({t.status.name})")

    # Simulation d'envoi d'email
    email_service = EmailService()
    email_service.send_task_reminder("test@mail.com", "Préparer le rapport", "2025-01-01")

    print("\nDémo terminée avec succès !")

if __name__ == "__main__":
    main()
