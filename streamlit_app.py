import streamlit as st
import requests
from PIL import Image
import io
import base64

# Função para converter imagem para base64
def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Função para buscar dados do Baserow
def fetch_data_from_baserow(api_url, api_key):
    headers = {
        "Authorization": f"Token {api_key}"
    }
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()

# URL e chave da API do Baserow
api_url = "https://api.baserow.io/api/database/rows/table/343108/?user_field_names=true"
api_key = "FTEYrDSMgSCucx6GY6i3jbBE1lTqhOqC"

# Buscar dados
data = fetch_data_from_baserow(api_url, api_key)

# Título do aplicativo
st.title("Galeria de Cards")

# Loop para criar cards usando dados do Baserow
for item in data['results']:
    # Obter URL da imagem e descrição
    image_url = item['image_url']  # Substitua 'image_url' pelo nome do campo correto
    description = item['description']  # Substitua 'description' pelo nome do campo correto

    # Carregar imagem da URL
    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content))

    # Mostrar imagem e descrição
    st.image(img, caption=description, use_column_width=True)
    st.write(description)

    # Converter a imagem para base64
    img_str = image_to_base64(img)

    # Botão de copiar (usando JavaScript)
    copy_button = f"""
    <button onclick="navigator.clipboard.write([new ClipboardItem({{'image/png': fetch('data:image/png;base64,{img_str}').then(res => res.blob())}})])">
        Copiar Imagem
    </button>
    """
    st.markdown(copy_button, unsafe_allow_html=True)

    st.markdown("---")
