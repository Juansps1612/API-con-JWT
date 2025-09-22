# 1. Registrar un usuario normal
curl -X POST https://super-duper-parakeet-wr7wqqq9r976fvg6w-5000.app.github.dev/register \
-H "Content-Type: application/json" \
-d '{"username": "usuario1", "password": "1234"}'

# 2. Login usuario normal
curl -X POST https://super-duper-parakeet-wr7wqqq9r976fvg6w-5000.app.github.dev/login \
-H "Content-Type: application/json" \
-d '{"username": "usuario1", "password": "1234"}'


# 3. Ver usuarios (solo admin)
curl -X GET https://super-duper-parakeet-wr7wqqq9r976fvg6w-5000.app.github.dev/usuarios \
-H "Authorization: Bearer <ACCESS_TOKEN_ADMIN>" \
-H "Content-Type: application/json"

# 4. Intentar ver usuarios con usuario normal (debe fallar)
curl -X GET https://super-duper-parakeet-wr7wqqq9r976fvg6w-5000.app.github.dev/usuarios \
-H "Authorization: Bearer <ACCESS_TOKEN_USER>" \
-H "Content-Type: application/json"
