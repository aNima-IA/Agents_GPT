# BBScan

BBScan es un escáner asíncrono de bug bounty orientado a entornos autorizados. Permite cargar un fichero CSV con los objetivos en scope y un fichero JSON exportado de Burp Suite para respetar reglas, proxies y cabeceras. Ejecuta un reconocimiento ligero y una batería de pruebas de vulnerabilidades de severidad media o superior.

## Requisitos

- Python 3.11+
- Dependencias definidas en `pyproject.toml`

## Instalación

```bash
make install
```

## Uso básico

```bash
bbscan run --in-scope data/examples/in_scope.csv --burp data/examples/burp_project.json --out out/ --concurrency 20 --timeout 8 --severity-min MEDIUM --dry-run
```

### Opciones principales

- `--allow-ssrf-probe` habilita pruebas activas de SSRF controladas.
- `--allow-graphql-introspection` permite consultas de introspección GraphQL.
- `--sarif` genera salida SARIF en `findings.sarif`.
- `--include/--exclude` para ajustar rápidamente el scope.
- `--resume` reutiliza la cache previa.

## Formato de entrada

### CSV

Columnas mínimas: `host`, `base_url`, `scope_note`. Ejemplo en `data/examples/in_scope.csv`.

### Burp Project JSON

Exporta el “Project options” de Burp Suite en JSON. El programa utiliza:

- Configuración de proxy.
- Reglas de scope (include/exclude).
- Cabeceras personalizadas y user-agent.
- Timeouts y opciones TLS.

Esquema mínimo en `schemas/burp_project.schema.json` y ejemplo en `data/examples/burp_project.json`.

## Checks implementados

| ID | Descripción | Severidad |
|----|-------------|-----------|
| cors-misconfig | CORS permisivo con credenciales | MEDIUM |
| open-redirect | Redirecciones abiertas | MEDIUM |
| idor | IDOR/BOLA | MEDIUM |
| sensitive-files | Ficheros sensibles expuestos | MEDIUM |
| dir-listing | Directory Listing | MEDIUM |
| ssrf | SSRF heurístico | MEDIUM |
| jwt-misconfig | JWT sin seguridad | MEDIUM |
| csp-weak | CSP ausente o débil | MEDIUM |
| graphql-exposure | GraphQL/OpenAPI expuestos | MEDIUM |
| upload-misconfig | Fallos en uploads | MEDIUM |
| verb-tamper | Métodos HTTP inseguros | MEDIUM |
| cache-poison | Primitivas de cache poisoning | MEDIUM |
| subdomain-takeover | CNAME huérfanos | MEDIUM |
| auth-weak-headers | Cookies sensibles sin flags | MEDIUM |
| rate-limit-missing | Ausencia de rate limit | MEDIUM |

## Ética y legalidad

- **Solo para entornos con autorización explícita.**
- Las PoCs son no destructivas y buscan minimizar el impacto.
- Utiliza `--dry-run` para simular sin enviar tráfico.

## Desarrollo

```bash
make lint
make test
```

## Licencia

MIT
