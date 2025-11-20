
---

## `Makefile`

> Lưu ý: trong Makefile các dòng lệnh phải bắt đầu bằng **tab**, không phải space. Khi copy nhớ giữ nguyên.

```make
# Makefile chính cho ai-glasses-system

.PHONY: all protos backend-run backend-venv pi-install pi-run tools-build tools-style clean

ROOT_DIR := $(CURDIR)

all: protos

# ================================
# Shared / Protobuf
# ================================
protos:
	@echo "[MAKE] Generate protobuf (shared/protocol)..."
	bash "$(ROOT_DIR)/shared/tools/generate_protos.sh"

# ================================
# Cloud Backend (FastAPI)
# ================================
backend-venv:
	@echo "[MAKE] Creating backend venv and installing deps..."
	cd "$(ROOT_DIR)/cloud-backend" && python -m venv .venv && .venv/bin/pip install -r requirements.txt

backend-run:
	@echo "[MAKE] Running backend (uvicorn app.main:app)..."
	cd "$(ROOT_DIR)/cloud-backend" && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# ================================
# Pi Core (Raspberry Pi Zero 2W)
# ================================
pi-install:
	@echo "[MAKE] Installing Pi-core dependencies..."
	cd "$(ROOT_DIR)/pi-core/scripts" && bash install_pi.sh

pi-run:
	@echo "[MAKE] Running Pi-core main..."
	cd "$(ROOT_DIR)/pi-core/scripts" && bash run_all.sh

# ================================
# Tools (build & style)
# ================================
tools-build:
	@echo "[MAKE] Running tools/scripts/build_all.sh..."
	cd "$(ROOT_DIR)/tools/scripts" && bash build_all.sh

tools-style:
	@echo "[MAKE] Running tools/scripts/check_style.sh..."
	cd "$(ROOT_DIR)/tools/scripts" && bash check_style.sh

# ================================
# Dọn dẹp nhẹ
# ================================
clean:
	@echo "[MAKE] Cleaning temporary files..."
	find "$(ROOT_DIR)" -name "__pycache__" -type d -prune -exec rm -rf {} +
	find "$(ROOT_DIR)" -name "*.pyc" -delete
