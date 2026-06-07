import requests
from django.http import JsonResponse


def buscar_produto_openfoodfacts(request):
    codigo = request.GET.get("codigo", "").strip()

    if not codigo:
        return JsonResponse({"ok": False, "erro": "Código não informado."}, status=400)

    url = f"https://world.openfoodfacts.org/api/v2/product/{codigo}.json"

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "django-starter/1.0"}
        )
        response.raise_for_status()
        data = response.json()
    except Exception:
        return JsonResponse(
            {"ok": False, "erro": "Erro ao consultar Open Food Facts."},
            status=502
        )

    product = data.get("product") or {}
    nome = (product.get("product_name") or "").strip()

    return JsonResponse({
        "ok": True,
        "encontrado": bool(nome),
        "codigo": codigo,
        "nome": nome,
        "marca": (product.get("brands") or "").strip(),
        "categoria": (product.get("categories") or "").strip(),
    })