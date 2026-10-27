# Talented DevOps – Hafta 5 CI/CD

GitHub Actions ile çok aşamalı boru hattı: **lint → test → Docker build → GHCR push**.

- Tetikleyiciler: `main`'e push, `main`'e açılan pull request, `vX.Y.Z` tag push
- Matris: Python 3.11 ve 3.12
- İmaj etiketleri (SemVer): `1.0.0`, `1.0`, `1`, `main`, `sha-<kısa sha>`
- PR'larda imaj derlenir ama push edilmez

Yerelde çalıştırma:
    pip install -r requirements-dev.txt
    flake8 app tests && pylint app && pytest -v
    docker build -t talented-cicd:local . && docker run -p 8000:8000 talented-cicd:local
