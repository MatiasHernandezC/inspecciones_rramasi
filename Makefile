# Windows-only Makefile (PowerShell)
SHELL := cmd.exe
.SHELLFLAGS := /C


# Venv paths (venv is a sibling of this repo folder)
VENV_PY := ..\venv\Scripts\python.exe
VENV_PIP := ..\venv\Scripts\pip.exe

define RUN_BACKEND
  if (-Not (Test-Path "$(VENV_PY)")) { Write-Error "No se encontró Python del venv en '$(VENV_PY)'. Ejecuta .\venv\Scripts\Activate.ps1 e instala dependencias."; exit 1 }; \
  Push-Location backend; \
  & "$(VENV_PY)" -m uvicorn app.main:app --reload; \
  Pop-Location
endef

define RUN_ALEMBIC
  if (-Not (Test-Path "$(VENV_PY)")) { Write-Error "No se encontró Python del venv en '$(VENV_PY)'"; exit 1 }; \
  Push-Location backend; \
  & "$(VENV_PY)" -m alembic -c alembic.ini $(1); \
  Pop-Location
endef

define RUN_FRONTEND
  Push-Location frontend; \
  npm start; \
  Pop-Location
endef

.PHONY: help backend frontend up up-new-windows alembic-stamp-base alembic-upgrade alembic-revision install-backend install-frontend install

help:
	@echo "Targets disponibles:"
	@echo "  backend            - Levanta FastAPI con uvicorn (reload)"
	@echo "  frontend           - Levanta React (npm start)"
	@echo "  up                 - Levanta backend y frontend en paralelo (Jobs)"
	@echo "  up-new-windows     - Levanta ambos en nuevas ventanas de PowerShell"
	@echo "  alembic-stamp-base - Marca migraciones como base (recuperación)"
	@echo "  alembic-upgrade    - Ejecuta alembic upgrade head"
	@echo "  alembic-revision   - Crea nueva revisión Alembic (usa name=...)"
	@echo "  install-backend    - Instala dependencias backend (pip)"
	@echo "  install-frontend   - Instala dependencias frontend (npm)"
	@echo "  install            - Instala backend y frontend"

backend:
	@$(RUN_BACKEND)

frontend:
	@$(RUN_FRONTEND)

# Inicia backend y frontend en paralelo usando Jobs de PowerShell
up:
	@$jobs = @(); \
	$jobs += Start-Job -ScriptBlock { $(RUN_BACKEND) }; \
	$jobs += Start-Job -ScriptBlock { $(RUN_FRONTEND) }; \
	Write-Host "Servicios iniciados como Jobs. Usa 'Get-Job' y 'Receive-Job' en PowerShell."; \
	Write-Host "Para detener: 'Get-Job | Stop-Job -Force'"; \
	Receive-Job -Job $$jobs -Wait -AutoRemoveJob

# Abre dos ventanas nuevas de PowerShell (una por servicio)
up-new-windows:
	@Start-Process powershell -ArgumentList "-NoExit","-NoProfile","-Command","cd backend; \"$(VENV_PY)\" -m uvicorn app.main:app --reload"; \
	 Start-Process powershell -ArgumentList "-NoExit","-NoProfile","-Command","cd frontend; npm start"; \
	 Write-Host "Lanzado en nuevas ventanas."

alembic-stamp-base:
	@$(call RUN_ALEMBIC,stamp base)

alembic-upgrade:
	@$(call RUN_ALEMBIC,upgrade head)

# Uso: make alembic-revision name="mi_cambio"
alembic-revision:
	@if (-Not "$(name)") { Write-Error "Falta parámetro name=..."; exit 1 }; \
	$(call RUN_ALEMBIC,revision -m "$(name)")

install-backend:
	@if (-Not (Test-Path "$(VENV_PIP)")) { Write-Error "No se encontró pip del venv en '$(VENV_PIP)'"; exit 1 }; \
	 Push-Location backend; \
	 & "$(VENV_PIP)" install -e .; \
	 Pop-Location

install-frontend:
	@Push-Location frontend; \
	npm install; \
	Pop-Location

install: install-backend install-frontend

