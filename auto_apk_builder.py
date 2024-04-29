import paramiko
import os

# Configurações de conexão SSH
HOST = '0.tcp.sa.ngrok.io'
PORT = 14469
USERNAME = 'Administrator'
PASSWORD = '123456@Lucas'


LOCAL_DIR = '~/Downloads/codecanyon-xgVfDTjz-6ammart-multivendor-food-grocery-ecommerce-parcel-pharmacy-delivery-app-with-admin-website/user_app_and_web'
REMOTE_DIR = r'C:\Users\Administrator\Dev\flutter_lab'

COMPILATION_COMMAND = 'flutter build apk --release --no-shrink'

# SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)


zip_filename = 'app_to_be_compiled.zip'
os.system(f'zip -r {zip_filename} {LOCAL_DIR}') # Command for WindowsOS

# SFTP connection
sftp = ssh.open_sftp()

sftp.put(zip_filename, os.path.join(REMOTE_DIR, zip_filename))

# Run compilation commando in the VPS
stdin, stdout, stderr = ssh.exec_command(f'cd {REMOTE_DIR} && {COMPILATION_COMMAND}')

# Waiting
stdout.channel.recv_exit_status()

sftp.close()
ssh.close()

# Return apk
try:
    os.makedirs('output', exist_ok=True)
    sftp.get(os.path.join(REMOTE_DIR, 'build', 'app', 'outputs', 'flutter-apk', 'app-release.apk'), 'output/app-release.apk')

except Exception as e:
    print("Erro ao baixar o arquivo APK:", e)

os.remove(zip_filename)

# END OF THE TASK
print("Compilação concluída e arquivo .apk salvo no diretório 'output'")

