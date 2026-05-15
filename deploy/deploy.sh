#!/bin/bash

apt-get update
apt-get upgrade -y

apt-get install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    mariadb-server \
    mariadb-client \
    nginx \
    curl \
    wget \
    git \
    sudo

if ! id "student" &>/dev/null; then
    useradd -m -s /bin/bash student
    usermod -aG sudo student
    echo "student:student" | chpasswd
fi

if ! id "teacher" &>/dev/null; then
    useradd -m -s /bin/bash teacher
    usermod -aG sudo teacher
    echo "teacher:12345678" | chpasswd
fi

if ! id "app" &>/dev/null; then
    useradd -m -s /bin/bash -U app
fi

if ! id "operator" &>/dev/null; then
    useradd -m -s /bin/bash operator
    echo "operator:12345678" | chpasswd
fi

cat > /etc/sudoers.d/operator << 'EOF'
operator ALL=(ALL) NOPASSWD: /bin/systemctl start mywebapp
operator ALL=(ALL) NOPASSWD: /bin/systemctl stop mywebapp
operator ALL=(ALL) NOPASSWD: /bin/systemctl restart mywebapp
operator ALL=(ALL) NOPASSWD: /bin/systemctl status mywebapp
operator ALL=(ALL) NOPASSWD: /bin/systemctl reload nginx
EOF
chmod 0440 /etc/sudoers.d/operator

systemctl start mariadb
systemctl enable mariadb

mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS task_tracker;
CREATE USER IF NOT EXISTS 'app'@'127.0.0.1' IDENTIFIED BY 'app';
GRANT ALL PRIVILEGES ON task_tracker.* TO 'app'@'127.0.0.1';
FLUSH PRIVILEGES;
EOF

mkdir -p /opt/mywebapp
chown -R app:app /opt/mywebapp
chmod 755 /opt/mywebapp

cp "../mywebapp/app.py" /opt/mywebapp/
cp "../mywebapp/models.py" /opt/mywebapp/
cp "../mywebapp/service.py" /opt/mywebapp/
cp "../mywebapp/migrate.py" /opt/mywebapp/
cp "../mywebapp/requirements.txt" /opt/mywebapp/

chmod +x /opt/mywebapp/migrate.py
chmod +x /opt/mywebapp/app.py
chown -R app:app /opt/mywebapp

python3 -m venv /opt/mywebapp/venv
chown -R app:app /opt/mywebapp/venv

/opt/mywebapp/venv/bin/pip install --upgrade pip
/opt/mywebapp/venv/bin/pip install -r /opt/mywebapp/requirements.txt

/opt/mywebapp/venv/bin/python3 /opt/mywebapp/migrate.py --host=127.0.0.1 --user=app --password=app --database=task_tracker

cp "./mywebapp.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable mywebapp

systemctl start mywebapp

rm -f /etc/nginx/sites-enabled/default
cp "./nginx.conf" /etc/nginx/sites-available/mywebapp
ln -sf /etc/nginx/sites-available/mywebapp /etc/nginx/sites-enabled/mywebapp

systemctl reload nginx

echo "22" > /home/student/gradebook
chown student:student /home/student/gradebook
chmod 644 /home/student/gradebook