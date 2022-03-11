▶폴더 통째로 삭제
rm -rf 폴더명

▶깃에서 소스가져오기
# git clone https://github.com/uminho1/upbit.git #

▶한국 기준으로 서버 시간 설정: 
sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

▶소스편집
vim upbit_auto.py

▶백그라운드 실행 (엔터 연속 2번)
nohup python3 btc_upbit_auto_macd_v20.py > macd_v20_output.log &
