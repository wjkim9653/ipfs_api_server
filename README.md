# ipfs_api_server

```sh
sudo apt update && sudo apt install -y python3 python3-pip python3-venv wget curl unzip
```
```sh
cd ~
git clone https://github.com/wjkim9653/ipfs_api_server.git
cd ~/ifps_api_server
python3 -m venv venv
source venv/bin/activate
```
```sh
pip install Flask requests
```
```sh
# 설치
wget https://dist.ipfs.tech/kubo/v0.29.0/kubo_v0.29.0_linux-amd64.tar.gz
tar -xvzf kubo_v0.29.0_linux-amd64.tar.gz
cd kubo && sudo mv ipfs /usr/local/bin/ && cd ..

# 현재 실행 중인 프로세스 종료 (혹시 남아있다면)
pkill -f "ipfs daemon"
pkill -f "python app.py"

# IPFS 초기화 및 실행
ipfs init
```
```sh
export API_KEY="mysecretkey"
export IPFS_API_URL="http://127.0.0.1:5001/api/v0"
python app.py
```
```sh
nohup ipfs daemon > ipfs.log 2>&1 &
nohup python app.py > app.log 2>&1 &
```
```sh
# 프로세스 확인
ps aux | grep -E "(ipfs|python)"
```