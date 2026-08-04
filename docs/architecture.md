# Architecture cible — BuildSense AI

BuildSense traite les modèles IA comme des interprètes de plan, jamais comme des
moteurs de calcul. Une extraction est d'abord validée par un contrat Pydantic,
puis le moteur Python calcule les métrés, quantités et prix de manière traçable.

## Découpage initial

| Domaine | Responsabilité |
| --- | --- |
| Auth | JWT/OAuth2, tenants et rôles |
| Projects | Projets, versions et audit |
| Upload | Validation de fichiers et objets MinIO |
| Plan analysis | OCR, orchestration de fournisseurs et validation JSON |
| Quantity survey | Longueurs, surfaces, volumes et règles de métré |
| Pricing | Prix unitaires, ratios, taxes et devis |
| Reports | PDF, Excel et Word |
| Notification | Suivi asynchrone via WebSocket/Celery |

## Chemin de traitement

`upload -> stockage MinIO -> tâche Celery -> OCR/vision API -> JSON Pydantic -> validation humaine -> moteur de métrés -> prix locaux -> rapport`

Les appels aux fournisseurs seront isolés derrière une interface d'adaptateur.
L'orchestrateur sélectionnera un fournisseur selon la tâche, le coût, la latence,
la région et le quota, avec cache par empreinte du document + version du prompt,
et bascule vers un autre fournisseur en cas d'échec réessayable.

## Choix de fournisseurs

OpenAI est le choix de départ recommandé pour le contrat JSON/vision et la
robustesse d'intégration. Gemini est un bon second fournisseur pour les très
grands plans et le contexte long. Claude est utile comme second avis visuel,
mais les capacités de sortie structurée et les limites doivent être validées au
moment de l'intégration. Mistral OCR convient en pré-étape OCR économique. Les
prix et limites évoluant fréquemment, ils seront configurés, mesurés et comparés
en environnement de qualification, plutôt que figés dans le code.

## Garde-fous

- clés API uniquement dans le gestionnaire de secrets/environnement ; jamais en base ni dans les logs ;
- validation de schéma, limites de taille et conservation du résultat brut avec sa provenance ;
- calculs en `Decimal`, règles versionnées et résultats explicables ;
- validation/correction humaine obligatoire avant le devis final ;
- isolation par tenant et journal d'audit avant toute ouverture SaaS.
