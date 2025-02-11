# Système de gestion des API sportives

## **Présentation du projet**
Ce projet illustre la création d'un système de gestion des API conteneurisé pour l'interrogation des données sportives. Il exploite **Amazon ECS (Fargate)** pour l'exécution des conteneurs, **Amazon API Gateway** pour l'exposition des points de terminaison REST et une **API sportive** externe pour les données sportives en temps réel. Le projet présente des pratiques avancées de cloud computing, notamment la gestion des API, l'orchestration des conteneurs et les intégrations AWS sécurisées.

---

## **Features**
- Exposes a REST API for querying real-time sports data
- Runs a containerized backend using Amazon ECS with Fargate
- Scalable and serverless architecture
- API management and routing using Amazon API Gateway
 
---

## **Prérequis**
- **Clé API Sports** : créez un compte et un abonnement gratuits et obtenez votre clé API sur serpapi.com
- **Compte AWS** : créez un compte AWS et ayez une compréhension de base d'ECS, API Gateway, Docker et Python
- **AWS CLI installé et configuré** : installez et configurez AWS CLI pour interagir par programmation avec AWS
- **Bibliothèque Serpapi** : installez la bibliothèque Serpapi dans l'environnement local « pip install google-search-results »
- **Docker CLI et Desktop installés** : pour créer et envoyer des images de conteneur

---

## **Technical Architecture**
![ Diagramme Principale](/img/Diagramme%20sans%20nom.jpg)

---

## **Technologies**
- **Fournisseur de cloud** : AWS
- **Services de base** : Amazon ECS (Fargate), API Gateway, CloudWatch
- **Langage de programmation** : Python 3.x
- **Conteneurisation** : Docker
- **Sécurité IAM** : Politiques de moindre privilège personnalisées pour l'exécution des tâches ECS et API Gateway

---

## **Project Structure**

```bash
sports-api-management/
├── app.py # Application Flask pour interroger les données sportives
├── Dockerfile # Dockerfile pour conteneuriser l'application Flask
├── requirements.txt # Dépendances Python
├── .gitignore
├── /img 
└── README.md # Documentation du projet
```

---

## **Instructions d'installation**

### **Cloner repo**
```bash
git clone  https://github.com/sekedoua/sport-containerized-api-ecs-elb.git
cd sport-containerized-api-ecs-elb
```
### **Créer un dépôt ECR (Repository) **
```bash
aws ecr create-repository --repository-name sports-api --region eu-west-3
```

### **Authentifier, construire et envoyer l'image Docker**
```bash
aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.eu-west-3.amazonaws.com
![ Docker Part](/img/Capture_Login.PNG)

docker build --platform linux/amd64 -t sports-api .
docker tag sports-api:latest <AWS_ACCOUNT_ID>.dkr.ecr.eu-west-3.amazonaws.com/sports-api:sports-api-latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.eu-west-3.amazonaws.com/sports-api:sports-api-latest
```
![ Docker Part](/img/dockerBuild_ag_push.PNG)

### **Configurer le cluster ECS avec Fargate**
1. Créer un cluster ECS :
- Accédez à la console ECS → Clusters → Créer un cluster
- Nommez votre cluster (sports-api-cluster)
- Pour Infrastructure, sélectionnez Fargate, puis créez un cluster

2. Créer une définition de tâche :
- Accédez à Définitions de tâches → Créer une nouvelle définition de tâche
- Nommez votre définition de tâche (sports-api-task)
- Pour Infrastructure, sélectionnez Fargate
- Ajoutez le conteneur :
- Nommez votre conteneur (sports-api-container)
- URI de l'image : <AWS_ACCOUNT_ID>.dkr.ecr.eu-west-3.amazonaws.com/sports-api:sports-api-latest
- Port du conteneur : 8080
- Protocole : TCP
- Nom du port : laissez vide
- Protocole d'application : HTTP
- Définir les Eariables d'environnement :
- Clé : SPORTS_API_KEY
- Valeur : <VOTRE_SPORTSDATA.IO_API_KEY>
- Créer une définition de tâche
3. Exécuter le service avec un ALB
- Accédez à Clusters → Sélectionner Cluster → Service → Créer.
- Fournisseur de capacité : Fargate
- Sélectionnez la famille de configuration de déploiement (sports-api-task)
- Nommez votre service (sports-api-service)
- Tâches souhaitées : 2
- Réseau : Créer un nouveau groupe de sécurité
- Configuration réseau :
- Type : Tout TCP
- Source : N'importe où
- Équilibrage de charge : Sélectionner Application Load Balancer (ALB).
- Configuration ALB :
- Créer un nouvel ALB :
- Nom : sports-api-alb
- Chemin de vérification de l'état du groupe cible : "/sports"
- Créer un service
4. Test the ALB:
- Après avoir déployé le service ECS, notez le nom DNS de l'ALB (par exemple, sports-api-alb-<AWS_ACCOUNT_ID>.eu-west-3.elb.amazonaws.com)
- Confirmez que l'API est accessible en visitant le nom DNS de l'ALB dans votre navigateur et en ajoutant /sports à la fin (par exemple, http://sports-api-alb-<AWS_ACCOUNT_ID>.eu-west-3.elb.amazonaws.com/sports)

![ Docker Part](/img/Service_OK.PNG)

### **Configurer la passerelle API**
1. Créer une nouvelle API REST :
- Accédez à la console de la passerelle API → Créer une API → API REST
- Nommez l'API (par exemple, Passerelle API Sports)

2. Configurer l'intégration :
- Créez une ressource /sports
- Créez une méthode GET
- Choisissez Proxy HTTP comme type d'intégration
- Saisissez le nom DNS de l'ALB qui inclut « /sports » (par exemple, http://sports-api-alb-<AWS_ACCOUNT_ID>.eu-west-3.elb.amazonaws.com/sports

![ Docker Part](/img/API_GatewayOK.PNG)


3. Déployez l'API :
- Déployez l'API sur une étape (par exemple, prod)
- Notez l'URL du point de terminaison

### **Tester le système**
- Utilisez curl ou un navigateur pour tester :
```bash
curl https://<api-gateway-id>.execute-api.eu-west-3.amazonaws.com/prod/sports
```


### **Ce que nous avons appris**
Configuration d'une application évolutive et conteneurisée avec ECS
Création d'API publiques à l'aide d'API Gateway.

### **Améliorations futures**
Ajoutez la mise en cache pour les requêtes API fréquentes à l'aide d'Amazon ElastiCache
Ajoutez DynamoDB pour stocker les requêtes et préférences spécifiques à l'utilisateur
Sécurisez la passerelle API à l'aide d'une clé API ou d'une authentification basée sur IAM
Implémentez CI/CD pour automatiser les déploiements de conteneurs

