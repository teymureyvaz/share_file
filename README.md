1) ilk olaraq django rediis postgres-i qaldırmaq və reqiuirementleri install etmək üşün aşağıdakı komandadan istifadə etmək lazımdır:
 sudo docker-compose up -d --build
2) celery beat -i başlatmaq üçün isə aşağıdakı komanda istifadə ediləcək:
sudo docker-compose exec web celery -A sharefile  beat --loglevel=debug
