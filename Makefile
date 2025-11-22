.PHONY: all pi mobile backend clean

all: pi backend mobile

pi:
	cd pi-core && bash scripts/build_pi.sh

mobile:
	echo "Build Android apps bằng Android Studio."

backend:
	cd cloud-backend && pip install -r requirements.txt

clean:
	rm -rf **/__pycache__
	rm -rf cloud-backend/__pycache__
	rm -rf pi-core/build
