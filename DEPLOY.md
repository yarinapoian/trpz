# Інструкція з розгортання

Щоб розгорнути додаток на окремому сервері за допомогою GitHub Actions та self-hosted runner, потрібно виконати наступні кроки:

### Налаштування Self-Hosted Runner

1. Створіть VM для self-hosted runner і налаштуйте SSH

```bash
sudo apt-get update
sudo apt-get install -y curl wget git openssh-server
```

2. Встановіть GitHub Actions Runner
```bash
mkdir runner && cd runner
curl -o actions-runner-linux-arm64-2.334.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.334.0/actions-runner-linux-arm64-2.334.0.tar.gz
tar xzf ./actions-runner-linux-arm64-2.334.0.tar.gz
./config.sh --url https://github.com/yarinapoian/trpz --token YOUR_TOKEN
./run.sh
```

Згенеруйте токен в Settings => Actions => Runners. 

3. Встановіть Docker та Docker Compose
```bash
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
sudo systemctl enable docker
```

### Налаштування Target Node

1. Підготуйте окрему VM для розгортання додатку з Ubuntu 20.04 LTS. Підключиться до неї через SSH. Завантажте вручну через scp директорію deploy.

2. Запустіть автоматичний скрипт розгортання deploy.sh:
```bash
chmod +x deploy/deploy.sh
sudo ./deploy/deploy.sh
```

Цей скрипт налаштовує середовище для розгортання додатку, включаючи Docker, nginx та MySQL.

3. Згенеруйте SSH ключ для runner VM та додайте його до authorized_keys на target node:
```bash
ssh-keygen -N "" -f ~/.ssh/runner_key
cat ~/.ssh/runner_key.pub | ssh ubuntu@target-node "cat >> .ssh/authorized_keys"
```

## Налаштування сікретів

Додайте наступні секрети до вашого репозиторію на GitHub:

```
DEPLOY_HOST          ваша IP адреса target node
DEPLOY_USER          ubuntu
DEPLOY_KEY           SSH приватний ключ (вміст файлу ~/.ssh/runner_key)
DB_HOST              127.0.0.1
DB_USER              app
DB_PASSWORD          password
DB_NAME              task_tracker
```