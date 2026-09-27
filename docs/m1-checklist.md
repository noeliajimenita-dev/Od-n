# M1 — Checklist de configuración y secretos

## Configuración

- [ ] `.env.example` creado.
- [ ] `settings.py` creado.
- [ ] `constants.py` creado.
- [ ] `validation.py` creado.
- [ ] `status.py` creado.
- [ ] `security.py` creado.
- [ ] `paths.py` creado.

## Seguridad

- [ ] Las credenciales reales no están en el repositorio.
- [ ] `.env` está protegido por `.gitignore`.
- [ ] Las claves no aparecen en los logs.
- [ ] Los tokens no aparecen en mensajes de Telegram.
- [ ] Las credenciales no están escritas directamente en el código.

## Pruebas

- [ ] `test_config.py` creado.
- [ ] `test_security.py` creado.
- [ ] `test_paths.py` creado.
- [ ] `test_constants.py` creado.
- [ ] `test_status.py` creado.
- [ ] `test_environment.py` creado.

## Dependencias

- [ ] `requirements.txt` creado.
- [ ] `pyproject.toml` creado.

## Entornos

- [ ] Development definido.
- [ ] Testing definido.
- [ ] Production definido.

## Credenciales

Durante M1 no se deben introducir claves reales.

Las credenciales de Gemini, Groq, Telegram, GitHub y Oracle Cloud se configurarán únicamente cuando el módulo correspondiente las necesite.

## Criterio para cerrar M1

M1 podrá considerarse terminado cuando:

1. La configuración pueda cargarse mediante variables de entorno.
2. Las credenciales permanezcan fuera del código.
3. La configuración pueda validarse.
4. El estado pueda consultarse sin revelar secretos.
5. Las pruebas correspondientes estén preparadas.
6. No existan credenciales reales dentro del repositorio.

## Siguiente módulo

M2 — Resource Manager.
