import json

# Carregar o arquivo JSON
with open("api_response.json", "r") as file:
    data = json.load(file)

# Inicializar uma lista para armazenar as ofertas
offers = []

# Percorrer os itens no JSON
for key, value in data.items():
    # Verifica se a chave contém informações do produto
    if "Product:" in key and "items" in key:
        product_key = key  # Guarda a chave do produto

        # Extrair o preço da oferta
        offer_price_info = data.get(f"{product_key}.sellers.0.commertialOffer")
        if offer_price_info:
            price = offer_price_info.get("Price")
            spot_price = offer_price_info.get("spotPrice")
        else:
            price = None
            spot_price = None

        # Extrair a imagem do produto
        image_info = data.get(f"Image:{value.get('imageId')}")
        if image_info:
            image_url = image_info.get("imageUrl")
        else:
            image_url = None  # ou uma string vazia, se preferir

        # Adicionar as informações da oferta à lista
        offers.append({
            "offer_link": product_key,
            "image_link": image_url,
            "price": price,
            "title": value.get("title", "Título não disponível")  # Supondo que você tenha o título em algum lugar
        })

# Exibir o resultado
for offer in offers:
    print(f"Título: {offer['title']}")
    print(f"Preço: {offer['price']}")
    print(f"Link da Oferta: {offer['offer_link']}")
    print(f"Link da Imagem: {offer['image_link']}")
    print("-" * 40)
